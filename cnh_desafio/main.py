from openai import OpenAI
import anthropic

import os
import base64
import json

import datetime

from dotenv import load_dotenv, find_dotenv
import time
_ = load_dotenv(find_dotenv())

def get_prompt(prompt):
  with open(prompt, "r") as prompt_file:
    return prompt_file.read()

def anthropic_create_file(path):
  with open(path, 'rb') as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def openai_create_file(path):
  return openai_client.files.create(file = open(path, "rb"),purpose='vision')
  
def json_read(path):
  with open(path, "r") as json_file:
    data = json.load(json_file)
    return data

def json_write(path, data):
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=4)
  
def anthropic_make_request(prompt):
  msg = anthropic_client.messages.create(
          model="claude-3-5-sonnet-20240620",
          max_tokens = 1024,
          temperature = 0,
          system = prompt,
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
  return msg.content[0].text, msg.usage.input_tokens, msg.usage.output_tokens

def openai_request(message):

  def create_thread(message):
    return openai_client.beta.threads.create(
      messages=message
  )

  def run_thread(thread):
    run = openai_client.beta.threads.runs.create_and_poll(
      thread_id = thread.id,
      assistant_id = os.environ.get('ASSISTANT_ID')
    )

    if run.status == 'completed': 
      messages = openai_client.beta.threads.messages.list(
        thread_id=thread.id
      )

      return messages.data[0].content[0].text.value, run.usage.prompt_tokens, run.usage.completion_tokens, thread.id

    return run.status
  
  return run_thread(create_thread(message))

def compare_json(templet, generated, model):
    data = json_read(ERRORS_DATA_PATH)
    errors = 0
    for key, value in generated.items():
        if key in templet:
            if value.lower() != templet[key].lower():
                data[model][key.lower()] += 1
                errors += 1
    json_write(ERRORS_DATA_PATH, data)
    return len(templet) - errors

def save_data(openai_response:str, openai_input_tokens, openai_output_tokens, openai_time, anthropic_response:str, anthropic_input_tokens, anthropic_output_tokens, anthropic_time, cnh, rotation, distance):

        with open(DATA_PATH, "r") as json_file:
            data = json.load(json_file)

        content = {
          "anthropic": {
            "time": float(format(anthropic_time,".2f")),
            "tokens": anthropic_input_tokens + anthropic_output_tokens,
            "cost": float(format(anthropic_input_tokens*(3/1000000) + anthropic_output_tokens*(15/1000000), ".4f")),
            "accuracy": float(format(compare_json(json_read(GABARITO),json.loads(anthropic_response), "anthropic")/13,".2f")),
          },
          "openai":{
              "time": float(format(openai_time,".2f")),
              "tokens": openai_input_tokens + openai_output_tokens,
              "cost": float(format(openai_input_tokens*(5/1000000) + openai_output_tokens*(15/1000000), ".4f")),
              "accuracy": float(format(compare_json(json_read(GABARITO),json.loads(openai_response), "openai")/13,".2f")),
          },
          "doc-type":{
            "type": media_type,
            "rotations_number": rotation,
            "distance": f"{distance}",
            "cnh_model": cnh
          }, 
          "response_is_equal": openai_response == anthropic_response,
          "day-time": f"{datetime.datetime.now()}",
        }

        data.append(content)
        with open(DATA_PATH, "w") as json_file:
          json.dump(data, json_file, indent=4)

cnh = 0
rotation = 0
distance = "normal"

CNH_FILE = f"C:/Users/Pedro/Documents/notas/cnh_desafio/dataset/data/cnh_{cnh}_rotated_{rotation}_{distance}.jpg"
GABARITO = f"C:/Users/Pedro/Documents/notas/cnh_desafio/templets/cnh_{cnh}.json"
DATA_PATH = "C:/Users/Pedro/Documents/notas/cnh_desafio/data/data.json"
PROMPT_PATH = 'C:/Users/Pedro/Documents/notas/cnh_desafio/prompt.txt'
ERRORS_DATA_PATH = "C:/Users/Pedro/Documents/notas/cnh_desafio/data/errors.json"

media_type = "image/jpeg"

anthropic_client = anthropic.Anthropic(api_key=os.environ.get("ANTRHOPIC_API_KEY"))
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
cnh_file = openai_create_file(CNH_FILE)

cnh_models = [0,1] 
rotats =  [0,1,2,3]
dists =  ["normal", "far"]

for cnh_model in cnh_models:
  cnh = cnh_model
  for rotat in rotats:
    rotation = rotat
    for dist in dists:
      distance = dist

      cnh_file_anth = anthropic_create_file(CNH_FILE)
      start_time = time.time()

      anthropic_response, anthropic_input_tokens, anthropic_output_tokens = anthropic_make_request(get_prompt(PROMPT_PATH))
      print(f"Anthropic: \n{anthropic_response}")

      anthropic_time = time.time() - start_time
      
      print(f"\n {anthropic_time}")
      start_time = time.time() 

      message=[
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

      openai_response, openai_input_tokens, openai_output_tokens, thread_id = openai_request(message)

      print(f"OpenAi:\n {openai_response}")

      openai_client.beta.threads.delete(thread_id)
      
      openai_time = time.time() - start_time    

      print(f"\n {openai_time}")

      save_data(openai_response, openai_input_tokens, openai_output_tokens, openai_time, anthropic_response, anthropic_input_tokens, anthropic_output_tokens, anthropic_time, cnh, rotation, distance)