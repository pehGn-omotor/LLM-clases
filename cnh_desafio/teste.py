import json
""" new_thread = client_openai.beta.threads.create(
    messages = [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": f"{openai_response}\n{anthropic_response}"
          }
        ],
      }
    ],
  )
  run = client_openai.beta.threads.runs.create_and_poll(
  thread_id = new_thread.id,
  assistant_id = os.environ.get('JSON_PARSER_ID'),
  instructions= Your job is to transfer info from an txt file into an json, following this json template: 
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
  Dont want no coordinates, only the last info present in each line
  )

  if run.status == 'completed': 
    messages = client_openai.beta.threads.messages.list(
    thread_id=new_thread.id
  )
    print(messages.data[0].content[0].text.value)
  else:
    print(run.status) """

def compare_json(json1, json2):
  if isinstance(json1, dict) and isinstance(json2, dict):
      common_keys = set(json1.keys()).intersection(set(json2.keys()))
      equal_fields = sum([compare_json(json1[key], json2[key]) for key in common_keys])
      return equal_fields
  elif isinstance(json1, list) and isinstance(json2, list):
      return sum([compare_json(item1, item2) for item1, item2 in zip(json1, json2)])
  else:
      return 1 if json1 == json2 else 0

def count_equal_fields(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        json1 = json.load(f1)
        json2 = json.load(f2)

    equal_fields_count = compare_json(json1, json2)
    return equal_fields_count

def to_dict(path):
  with open(path, "r") as json_file:
    data = json.load(json_file)
    return data

json2 ="""{
    "nome": "leni olivia de sousa gois nunes",
    "doc_identidade": "23758960 ssp/sp",
    "cpf": "132.410.558-50",
    "numero_registro": "03400654660",
    "data_nascimento": "30/08/1972",
    "filiacao": {
        "pai": "dionisio de sousa gois",
        "mae": "eugenia maria de sousa gois"
    },
    "data_emissao": "28/12/2019",
    "nacionalidade": "",
    "numero_espelho": "1952930798",
    "primeira_habilitacao": "14/01/1992",
    "permissionario_definitiva": "",
    "acc": "",
    "data_validade_habilitacao": "28/12/2024",
    "cat_hab": "b",
    "observacoes": "",
    "codigo_seguranca":"99351126978",
    "renach": "sp000413921"
}"""

print(to_dict("C:/Users/Pedro G/Documents/trabalho/LLM-clases/cnh_desafio/respostas/cnh_01.json"))


print(compare_json(to_dict("C:/Users/Pedro G/Documents/trabalho/LLM-clases/cnh_desafio/respostas/cnh_01.json"),json.loads(json2)))