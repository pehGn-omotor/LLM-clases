from openai import OpenAI
import os
import anthropic
import base64
import json
import datetime
from dotenv import load_dotenv, find_dotenv
import time
_ = load_dotenv(find_dotenv())

def create_file_anthropic(path):
  with open(path, 'rb') as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
def create_file_openai(path):
  return client_openai.files.create(file = open(path, "rb"),purpose='vision')

def make_anthropic_request():
  message_anthropic = client_anthropic.messages.create(
          model="claude-3-5-sonnet-20240620",
          max_tokens = 1024,
          temperature = 0,
          system = PROMPT,
          messages = [
          {
            "role": "user",
            "content": [
              {
                "type": "image",
                "source": {
                  "type": "base64",
                  "media_type": media_type,
                  "data": cnh_file_anth,
                },
              },
              {
                "type": "text",
                "text": "Here's my driver license"
              }
            ],
          }
        ],
      )
  return message_anthropic.content[0].text

def create_thread(message):
  return client_openai.beta.threads.create(
    messages=message
  )


cnh = 0
rotation = 0
distance = "normal"

CNH_FILE = f"C:/Users/Pedro/Documents/notas/cnh_desafio/dataset/data/cnh_{cnh}_rotated_{rotation}_{distance}.jpg"
GABARITO = f"C:/Users/Pedro/Documents/notas/cnh_desafio/templets/cnh_{cnh}.json"
media_type = "image/jpeg"
DATA_PATH = "C:/Users/Pedro/Documents/notas/cnh_desafio/data.json"

PROMPT = ''

client_anthropic = anthropic.Anthropic(api_key=os.environ.get("ANTRHOPIC_API_KEY"))
client_openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
cnh_file = create_file_openai(CNH_FILE)

cnh_models = [0,1] 
rotats =  [0,1,2,3]
dists =  ["normal", "far"]

for cnh_model in cnh_models:
  cnh = cnh_model
  for rotat in rotats:
    rotation = rotat
    for dist in dists:
      distance = dist

      cnh_file_anth = create_file_anthropic(CNH_FILE)
      start_time = time.time()

      anthropic_response = make_anthropic_request()
      print(anthropic_response)

      anthropic_time = time.time() - start_time
      print(f"\nAnthropic: {anthropic_time} seconds")
      
      start_time = time.time()      
      messages=[
        {
          "role": "user",
          "content": "Aqui está a minha carteira de motorista",
          "content": [
            {
              "type": "image_file",
              "image_file": {"file_id": cnh_file.id}
            },
          ]
        }
      ]
      thread = create_thread(messages)
        
      # Fazendo a requisição para o Chat GPT
      run = client_openai.beta.threads.runs.create_and_poll(
        thread_id = thread.id,
        assistant_id = os.environ.get('ASSISTANT_ID')
      )
      openai_response = ""
      if run.status == 'completed': 
        messages = client_openai.beta.threads.messages.list(
          thread_id=thread.id
        )
        print(messages.data[0].content[0].text.value)
        openai_response = messages.data[0].content[0].text.value
        openai_tokens = run.usage.completion_tokens
      else:
        print(run.status)
      openai_time = time.time() - start_time
      print(f"\nOpenAi: {openai_time} seconds")

      # Deletando a thread para evitar stacking
      client_openai.beta.threads.delete(thread.id)

      # Abrindo o arquivo de dados
      def return_json(path):
        with open(path, "r") as json_file:
          data = json.load(json_file)
          return data
        
      # Comparando o JSON gerado pelas IA com o gabarito
      def compare_json(json1, json2):
        if isinstance(json1, dict) and isinstance(json2, dict):
            common_keys = set(json1.keys()).intersection(set(json2.keys()))
            equal_fields = sum([compare_json(json1[key], json2[key]) for key in common_keys])
            return equal_fields
        elif isinstance(json1, list) and isinstance(json2, list):
            return sum([compare_json(item1, item2) for item1, item2 in zip(json1, json2)])
        else:
            return 1 if json1 == json2 else 0
      
      # Função que sava os dados no arquivo Data
      def save_data(openai_response:str, anthropic_response:str):

        with open(DATA_PATH, "r") as json_file:
            data = json.load(json_file)
        content = {
          "anthropic": {
            "time": float(format(anthropic_time,".2f")),
            "tokens": float(format(len(anthropic_response)/4,".2f")),
            "cost": (len(anthropic_response)/4*15)/1000000,
            "accuracy": float(format(compare_json(return_json(GABARITO),json.loads(anthropic_response))/18,".2f")),
          },
          "openai":{
              "time": float(format(openai_time,".2f")),
              "tokens": float(format(len(openai_response)/4,".2f")),
              "cost": (len(openai_response)/4*15)/1000000,
              "accuracy": float(format(compare_json(return_json(GABARITO),json.loads(openai_response))/18,".2f")),
          },
          "doc-type":{
            "type": media_type,
            "rotations_number": f"{rotation}",
            "distance": f"{distance}",
            "cnh_model": f"{cnh}"
          }, 
          "response_is_equal": openai_response == anthropic_response,
          "day-time": f"{datetime.datetime.now()}",
        }
        data.append(content)
        with open(DATA_PATH, "w") as json_file:
          json.dump(data, json_file, indent=4)

      save_data(openai_response, anthropic_response)