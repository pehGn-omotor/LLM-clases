import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read the JSON file
# Assume the JSON file is named 'data.json' and is in the same directory
df = pd.read_json('./data.json')

avg_anthropic_time = df['anthropic-time'].mean()
avg_openai_time = df['openai-time'].mean()

# Step 3: Create a bar chart
times = ['Anthropic', 'OpenAI']
avg_times = [avg_anthropic_time, avg_openai_time]

plt.figure(figsize=(10, 6))
plt.bar(times, avg_times, color=['blue', 'green'])
plt.xlabel('Service')
plt.ylabel('Average Time (seconds)')
plt.title('Average Response Time Comparison')
plt.show()