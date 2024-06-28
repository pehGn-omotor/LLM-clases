import os
from openai import OpenAI
import anthropic
import base64
import json

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

import time

# Transformando um arquivo para um arquivo mais legível para o Anthropic
def create_file_anthropic(path):
  with open(path, 'rb') as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

CNH_FILE = "C:/Users/Pedro G/Documents/trabalho/LLM-clases/cnh_desafio/data/foto/cnh_0_rotated_0.jpg"
GABARITO = "C:/Users/Pedro G/Documents/trabalho/LLM-clases/cnh_desafio/respostas/cnh_01.json"
image_media_type = "image/jpeg"

PROMPT = '''You are a document analyst and will be provided with a brazilian driver license. Your task is to transform it in a JSON exaclty like that with every field in lower case: 
        {
          "nome": "",
          "doc_identidade": "",
          "cpf": "",
          "numero_registro": "",
          "data_nascimento": "",
          "filiacao": {
              "pai": "",
              "mae": ""
          },
          "data_emissao": "",
          "nacionalidade": "",
          "numero_espelho": "texto na vertical na lateral da carteira. Existem dois, selecione o mais nítido",
          "primeira_habilitacao": "",
          "permissionario_definitiva": "",
          "acc": "",
          "data_validade_habilitacao": "",
          "cat_hab": "",
          "observacoes": "",
          "codigo_seguranca":"",
          "renach": "inicia com duas letras. Está abaixo do código de segurança"
        }
    If you cannot read something in the image provided by the user you must return the following message: 'Desculpe, poderia mandar uma outra imagem?'
    No need to say anything just return the JSON.
    '''

cnh_file_anth = create_file_anthropic(CNH_FILE)

start_time = time.time()

client_anthropic = anthropic.Anthropic(api_key=os.environ.get("ANTRHOPIC_API_KEY"))

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
            "media_type": image_media_type,
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

print(message_anthropic.content[0].text)
anthropic_response = message_anthropic.content[0].text
anthropic_time = time.time() - start_time
print(f"\nAnthropic: {anthropic_time} seconds")

start_time = time.time()

client_openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Transformando um arquivo para um arquivo mais legível para o GPT
def create_file_openai(path):
  return client_openai.files.create(file = open(path, "rb"),purpose='vision')

cnh_file = create_file_openai(CNH_FILE)

thread = client_openai.beta.threads.create(
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
)

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
else:
  print(run.status)
openai_time = time.time() - start_time
print(f"\nOpenAi: {openai_time} seconds")

def return_json(path):
  with open(path, "r") as json_file:
    data = json.load(json_file)
    return data
  
def compare_json(json1, json2):
  if isinstance(json1, dict) and isinstance(json2, dict):
      common_keys = set(json1.keys()).intersection(set(json2.keys()))
      equal_fields = sum([compare_json(json1[key], json2[key]) for key in common_keys])
      return equal_fields
  elif isinstance(json1, list) and isinstance(json2, list):
      return sum([compare_json(item1, item2) for item1, item2 in zip(json1, json2)])
  else:
      return 1 if json1 == json2 else 0
  
def save_data(openai_response:str, anthropic_response:str):

  with open('./data.json', "r") as json_file:
      data = json.load(json_file)
  content = {
      "anthropic-time": float(format(anthropic_time,".2f")),
      "anthropic-aprox-cost": (len(anthropic_response)/4*15)/1000000,
      "anthropic-aprox-tokens": float(format(len(anthropic_response)/4,".2f")),
      "anthropic-aprox-succes-rate": float(format(compare_json(return_json(GABARITO),json.loads(anthropic_response))/18,".2f")),
      "openai-time": float(format(openai_time,".2f")),
      "openai-aprox-tokens": float(format(len(openai_response)/4,".2f")),
      "openai-aprox-succes-rate": float(format(compare_json(return_json(GABARITO),json.loads(openai_response))/18,".2f")),
      "is_equal_response": openai_response == anthropic_response
  }
  data.append(content)
  with open('./data.json', "w") as json_file:
    json.dump(data, json_file, indent=4)

save_data(openai_response, anthropic_response)