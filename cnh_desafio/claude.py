import anthropic
import base64
import httpx
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

IMG_FILE = "C:/Users/Pedro/Documents/notas/cnh_desafio/dataset/foto_arquivo/foto/cnh1_rotated1.jpg"
image_media_type = "image/jpeg"

with open(IMG_FILE, 'rb') as image_file:
    # Read the image file and encode it to Base64
    image_data = base64.b64encode(image_file.read()).decode('utf-8')

client = anthropic.Anthropic(api_key=os.environ.get("ANTRHOPIC_API_KEY"))

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    temperature=0,
    system='''You will be provided with a brazilian driver license and your task is to transform it in a JSON file exaclty like that: 
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
          "numero_espelho": "",
          "primeira_habilitacao": "",
          "permissionario_definitiva": "",
          "acc": "",
          "data_validade_habilitacao": "",
          "cat_hab": "",
          "observacoes": "",
          "codigo_seguranca":"",
          "renach": ""
        }
    If you cannot read something in the image you must return to the user the following message: 'Desculpe, poderia mandar uma outra imagem?' 
    Answer only in brasilian portuguese.
    ''',
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_data,
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
print(message.content[0].text)