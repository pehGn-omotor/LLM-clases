import pandas as pd
import csv

def format_csv(path):
    df = pd.read_csv(path, encoding='latin-1')
    df.drop(df.columns[[0,1,2,3]], axis=1, inplace=True)
    return df

TXT_FILE = "C:/Users/Pedro/Documents/notas/cnh_desafio/dataset/CNH_Aberta/00000000_gt_ocr.txt"

# print(format_csv(TXT_FILE))

json1 = '''{
    "nome": "LENI OLIVIA DE SOUSA GOIS NUNES",
    "doc_identidade": "23758960 SSP/SP",
    "cpf": "132.410.558-50",
    "numero_registro": "03400654660",
    "data_nascimento": "30/08/1972",
    "filiacao": {
        "pai": "Dionisio de Sousa Gois",
        "mae": "Eugenia Maria de Sousa Gois"
    },
    "data_emissao": "28/12/2019",
    "nacionalidade": "",
    "numero_espelho": "1952930798",
    "primeira_habilitacao": "14/01/1992",
    "permissionario_definitiva": "",
    "acc": "",
    "data_validade_habilitacao": "28/12/2024",
    "cat_hab": "B",
    "observacoes": "",
    "codigo_seguranca":"99351126978",
    "renach": "SP000413921"
}'''

json2= '''{
    "nome": "LENI OLIVIA DE SOUSA GOIS NUNES",
    "doc_identidade": "23758960 SSP/SP",
    "cpf": "132.410.558-50",
    "numero_registro": "03400654660",
    "data_nascimento": "30/08/1972",
    "filiacao": {
        "pai": "Dionisio de Sousa Gois",
        "mae": "Eugenia Maria de Sousa Gois"
    },
    "data_emissao": "28/12/2019",
    "nacionalidade": "",
    "numero_espelho": "1952930798",
    "primeira_habilitacao": "14/01/1992",
    "permissionario_definitiva": "",
    "acc": "",
    "data_validade_habilitacao": "28/12/2024",
    "cat_hab": "B",
    "observacoes": "",
    "codigo_seguranca":"99351126978",
    "renach": "SP000413921"
}'''

print(json1 == json2)