import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

DATA_PATH = "C:/Users/Pedro/Documents/notas/cnh_desafio/data.json"

with open(DATA_PATH, 'r') as f:
    data = json.load(f)