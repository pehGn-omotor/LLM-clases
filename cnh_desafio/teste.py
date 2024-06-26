import pandas as pd
import csv

def format_csv(path):
    df = pd.read_csv(path, encoding='latin-1')
    df.drop(df.columns[[0,1,2,3]], axis=1, inplace=True)
    return df

TXT_FILE = "C:/Users/Pedro/Documents/notas/cnh_desafio/dataset/CNH_Aberta/00000000_gt_ocr.txt"

print(format_csv(TXT_FILE))