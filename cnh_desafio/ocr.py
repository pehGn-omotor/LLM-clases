import easyocr
import numpy as np

cnh = 0
rotation = 0
distance = "normal"

CNH_FILE = f"C:/Users/Pedro/Documents/notas/cnh_desafio/dataset/data/cnh_{cnh}_rotated_{rotation}_{distance}.jpg"

reader = easyocr.Reader(['pt'])
result = reader.readtext(CNH_FILE, detail=0)

print(result)
