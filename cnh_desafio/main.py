import os
from openai import OpenAI
import anthropic
import base64
import json

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

import time

CNH_FILE = "C:/Users/Pedro/Documents/notas/cnh_desafio/dataset/foto_arquivo/foto/cnh1_rotated1.jpg"
CRLV_FILE = "C:/Users/Pedro/Documents/notas/cnh_desafio/dataset/foto_arquivo/foto/cnh1_rotated1.jpg"
CNH_E_FILE = "C:/Users/Pedro/Documents/notas/cnh_desafio/dataset/foto_arquivo/arquivo/CNH-e.pdf" 
image_media_type = "image/jpeg"

start_time = time.time()
client_openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Transformando um arquivo para um arquivo mais legível para o GPT
def create_file_openai(path):
  return client_openai.files.create(file = open(path, "rb"),purpose='vision')

# Transformando um arquivo para um arquivo mais legível para o Anthropic
def create_file_anthropic(path):
  with open(path, 'rb') as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

#Arquivos
cnh_file = create_file_openai(CNH_FILE)
crlv_file = create_file_openai(CRLV_FILE)

PROMPT = '''You are a document analyst and will be provided with a brazilian driver license. Your task is to transform it in a JSON exaclty like that: 
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
          "numero_espelho": "texto na vertical na lateral da carteira",
          "primeira_habilitacao": "",
          "permissionario_definitiva": "",
          "acc": "",
          "data_validade_habilitacao": "",
          "cat_hab": "",
          "observacoes": "",
          "codigo_seguranca":"",
          "renach": "inicia com o estado onde o documento foi retirado"
        }
    If you cannot read something in the image provided by the user you must return the following message: 'Desculpe, poderia mandar uma outra imagem?'
    '''

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

start_time = time.time()

cnh_file_anth = create_file_anthropic(CNH_FILE)

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
anthropic_prompt = message_anthropic.content[0].text
anthropic_time = time.time() - start_time
print(f"\nOpenAi: {anthropic_time} seconds")

def compare(openai_response:str,anthropic_response):

  with open('./execution_time.json', "r") as json_file:
      data = json.load(json_file)
  content = {
      "openai-time": openai_time,
      "anthropic-time": anthropic_time,
      "openai-aprox-tokens": len(openai_response)/4,
      "anthropic-aprox-tokens": anthropic_time
  }
  data.append(content)
  with open('./execution_time.json', "w") as json_file:
      json.dump(data, json_file, indent=4)
