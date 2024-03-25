import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.lines as mlines
file_name = "XInference_Deployment_2024_03_25_03_38"
file_path = f'/home/rudia-agx/Desktop/FYP/node/XInference/analytics/Logs/{file_name}.csv'

df = pd.read_csv(file_path, header=0, names=['Timestmp', 'Event', 'CPU_Util', 'CPU_RAM_Util', 'GPU_Util', 'GPU_RAM_Util', 'Swap_Util'])
print(df.head())

df['Timestmp'] = pd.to_datetime(df['Timestmp'], format="%Y-%m-%d %H:%M:%S.%f")
df['Elapsed'] = (df['Timestmp'] - df['Timestmp'].min()).dt.total_seconds()
plt.figure(figsize=(10, 6))
plt.plot(df['Elapsed'], df['CPU_Util'], label='Total CPU Utilisation %')
plt.plot(df['Elapsed'], df['CPU_RAM_Util'], label='Total CPU RAM Utilisation %')
plt.plot(df['Elapsed'], df['GPU_Util'], label='Total GPU Utilisation %')
plt.plot(df['Elapsed'], df['GPU_RAM_Util'], label='Total GPU RAM Utilisation %')
plt.plot(df['Elapsed'], df['Swap_Util'], label='Total Swap Utilisation %')


deployments_indices = df[df['Event'].str.contains("Total Deployments:")]['Elapsed']
for ts in deployments_indices:
    plt.axvline(x=ts, color='black', linestyle='--', alpha=0.2)
plt.xlim(df['Elapsed'].min(), df['Elapsed'].max())

total_deployments_line = mlines.Line2D([], [], color='black', linestyle='--', alpha=0.2, label='Deployment Initialised')
handles, labels = plt.gca().get_legend_handles_labels()
handles.append(total_deployments_line)

plt.xlabel('Time Elapsed (seconds)')
plt.xticks(rotation=45)
plt.ylabel('Utilisation %')

plt.title('System Utilisation - Initialising 24 Deployments')

plt.legend(handles=handles, loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout(rect=[0, 0, 0.75, 1]) 

 
plt.show()