import os
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

import time
start_time = time.time()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def create_file(path):
  return client.files.create(file = open(path, "rb"),purpose='assistants')

IMG_FILE = "C:/Users/Pedro/Documents/notas/cnh_desafio/dataset/CNH_Aberta/00000030_in.jpg"
user_file = create_file(IMG_FILE)

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions=
    '''You will be provided with a brazilian driver license and your task is to transform it in a JSON, exaclty like that: 
        {
          "nome": "",
          "identidade": "",
          "cpf": "",
          "numero_registro": "",
          "data_nascimento": "",
          "filiacao": "",
          "data_emissao_habilitacao": "",
          "nacionalidade": "",
          "numero_espelho_habilitacao": "",
          "tipos_veiculo_habilitados": "",
          "registro_habilitacao": "",
          "primeira_habilitacao": "",
          "permissionario_definitiva": "",
          "acc": "",
          "data_validade_habilitacao": "",
          "categoria_habilitacao": "",
          "observacoes": "",
          "codigo_seguranca": "",
          "numero_renach": ""
        }
    If you cannot read something in the image you must answer only the following message: 'Desculpe, poderia mandar uma outra imagem?' ''',
    tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
    model="gpt-4o",
)

thread = client.beta.threads.create(
   messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Esta é a minha habilitação"
        },
        {
          "type": "image_file",
          "image_file": {"file_id": user_file.id}
        },
      ],
    }
  ]
)
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)
 
with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  event_handler=EventHandler(),
) as stream:
  stream.until_done()
  
print("\n %s seconds" % (time.time() - start_time))

'''
with open(EXEC_TIME_JSON_PATH, "w") as json_file:
    data = json.dumps(json_file)
    content = {
        "execution_time": f"{(time.time() - start_time)} seconds",
        "accuracy": f"{accuracy}"
    }
'''