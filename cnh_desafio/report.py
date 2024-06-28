import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

# Step 1: Read the JSON file
# Assume the JSON file is named 'data.json' and is in the same directory
DATA_PATH = "C:/Users/Pedro/Documents/notas/cnh_desafio/data.json"

with open(DATA_PATH, 'r') as f:
    data = json.load(f)

""" # Normalize JSON data
df = pd.json_normalize(data)

# Step 2: Calculate the mean of 'time' for 'anthropic' and 'openai'
avg_anthropic_time = df['anthropic.time'].mean()
avg_openai_time = df['openai.time'].mean()

avg_anthropic_accuracy = df['anthropic.accuracy'].mean()
avg_openai_accuracy = df['openai.accuracy'].mean()

filtered_df = df[df['doc-type.rotations_number'] == 1]

# Step 3: Create a bar chart
models = ['Anthropic', 'OpenAI']
avg_times = [avg_anthropic_time, avg_openai_time]

avg_accuracy = [avg_anthropic_accuracy,avg_openai_accuracy]
filtered_df = df[df['doc-type.rotations_number'] == 1] """

""" plt.figure(figsize=(10, 6))
plt.bar(models, avg_times, color=['royalblue', 'orange'])
plt.xlabel('Modelo')
plt.ylabel('Tempo Médio de Resposta (segundos)')
plt.title('Comparação Entre Tempos Médios De Respostas')
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(models, avg_accuracy, color=['royalblue', 'orange'])
plt.xlabel('Modelo')
plt.ylabel('Precisão Média')
plt.title('Comparação Entre a Precisão Geral Entre os Modelos')
plt.show() """

# Step 2: Extract and process the relevant data
rotation_data = {0: {'anthropic': [], 'openai': []},
                 1: {'anthropic': [], 'openai': []},
                 2: {'anthropic': [], 'openai': []},
                 3: {'anthropic': [], 'openai': []}}

for entry in data:
    rotation = int(entry['doc-type']['rotations_number']) if entry['doc-type']['rotations_number'] else 0
    if rotation in rotation_data:
        rotation_data[rotation]['anthropic'].append(entry['anthropic']['accuracy'])
        rotation_data[rotation]['openai'].append(entry['openai']['accuracy'])

# Calculate averages
rotations = [0, 1, 2, 3]
anthropic_avg = [np.mean(rotation_data[r]['anthropic']) if rotation_data[r]['anthropic'] else 0 for r in rotations]
openai_avg = [np.mean(rotation_data[r]['openai']) if rotation_data[r]['openai'] else 0 for r in rotations]

# Step 3: Create the bar plot
width = 0.35
fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(np.array(rotations) - width/2, anthropic_avg, width, label='Anthropic', alpha=0.7)
ax.bar(np.array(rotations) + width/2, openai_avg, width, label='OpenAI', alpha=0.7)

ax.set_xlabel('Number of Rotations')
ax.set_ylabel('Average Accuracy')
ax.set_title('Anthropic vs OpenAI Average Accuracy per Rotation Number')
ax.set_xticks(rotations)
ax.set_xticklabels(rotations)
ax.legend()

# Add a grid for better readability
ax.grid(True, linestyle='--', alpha=0.7, axis='y')

# Show the plot
plt.tight_layout()
plt.show()

# Step 2: Process the data
distances = {"normal": {'anthropic': [], 'openai': []},
             "far": {'anthropic': [], 'openai': []}}

for entry in data:
    distance = entry['doc-type']['distance']
    distances[distance]['anthropic'].append(entry['anthropic']['accuracy'])
    distances[distance]['openai'].append(entry['openai']['accuracy'])

# Calculate averages
avg_accuracies = {distance: {'anthropic': np.mean(values['anthropic']),
                             'openai': np.mean(values['openai'])}
                  for distance, values in distances.items()}

# Step 3: Create a bar plot
distance_types = list(avg_accuracies.keys())
x = np.arange(len(distance_types))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))

anthropic_accuracies = [avg_accuracies[d]['anthropic'] for d in distance_types]
openai_accuracies = [avg_accuracies[d]['openai'] for d in distance_types]

rects1 = ax.bar(x - width/2, anthropic_accuracies, width, label='Anthropic')
rects2 = ax.bar(x + width/2, openai_accuracies, width, label='OpenAI')

ax.set_ylabel('Average Accuracy')
ax.set_xlabel('Distance')
ax.set_title('Average Accuracy by Distance: Anthropic vs OpenAI')
ax.set_xticks(x)
ax.set_xticklabels(distance_types)
ax.legend()

# Add value labels on top of each bar
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
plt.show()

costs = {'anthropic': [], 'openai': []}

for entry in data:
    costs['anthropic'].append(entry['anthropic']['cost'])
    costs['openai'].append(entry['openai']['cost'])

# Calculate average costs
avg_costs = {model: np.mean(cost_list) for model, cost_list in costs.items()}

# Step 3: Create a bar plot
models = list(avg_costs.keys())
avg_cost_values = list(avg_costs.values())

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(models, avg_cost_values)

ax.set_ylabel('Average Cost')
ax.set_title('Average Cost by Model: Anthropic vs OpenAI')
ax.set_ylim(0, max(avg_cost_values) * 1.1)  # Set y-axis limit to 110% of max value

# Add value labels on top of each bar
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'${height:.6f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(bars)

# Color the bars differently
bars[0].set_color('skyblue')
bars[1].set_color('lightgreen')

plt.tight_layout()
plt.show()

# Step 2: Process the data
times = {'anthropic': [], 'openai': []}

for entry in data:
    times['anthropic'].append(entry['anthropic']['time'])
    times['openai'].append(entry['openai']['time'])

# Calculate average times
avg_times = {model: np.mean(time_list) for model, time_list in times.items()}

# Step 3: Create a bar plot
models = list(avg_times.keys())
avg_time_values = list(avg_times.values())

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(models, avg_time_values)

ax.set_ylabel('Average Time (seconds)')
ax.set_title('Average Time per Query by Model: Anthropic vs OpenAI')
ax.set_ylim(0, max(avg_time_values) * 1.1)  # Set y-axis limit to 110% of max value

# Add value labels on top of each bar
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.3f} s',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(bars)

# Color the bars differently
bars[0].set_color('skyblue')
bars[1].set_color('lightgreen')

plt.tight_layout()
plt.show()

accuracies = {'anthropic': [], 'openai': []}

for entry in data:
    accuracies['anthropic'].append(entry['anthropic']['accuracy'])
    accuracies['openai'].append(entry['openai']['accuracy'])

# Calculate average accuracies
avg_accuracies = {model: np.mean(acc_list) for model, acc_list in accuracies.items()}

# Step 3: Create a bar plot
models = list(avg_accuracies.keys())
avg_accuracy_values = list(avg_accuracies.values())

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(models, avg_accuracy_values)

ax.set_ylabel('Average Accuracy')
ax.set_title('Average Overall Accuracy: Anthropic vs OpenAI')
ax.set_ylim(0, 1)  # Set y-axis limit from 0 to 1 for accuracy

# Add value labels on top of each bar
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2%}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(bars)

# Color the bars differently
bars[0].set_color('skyblue')
bars[1].set_color('lightgreen')

plt.tight_layout()
plt.show()