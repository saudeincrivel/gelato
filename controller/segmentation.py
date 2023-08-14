import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


client_response_output_path = 'C:/Users/User/Documents/Programas_Node/dados/output/client_response.json'

# Load JSON data
with open(client_response_output_path, 'r') as json_file:
    data = json_file.read()

clients_data = json.loads(data)
df = pd.DataFrame(clients_data).T

# Selected properties for clustering
selected_properties = ['anual_income', 'avg_transaction', 'weighted_min_buy_ins']

# Z-score normalization
scaler = StandardScaler()
df[selected_properties] = scaler.fit_transform(df[selected_properties])

# Elbow Method to find optimal number of clusters
inertia = []
max_clusters = 10  # You can adjust this range based on your needs

for num_clusters in range(1, max_clusters + 1):
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(df[selected_properties])
    inertia.append(kmeans.inertia_)

# Plotting the elbow curve
plt.figure(figsize=(10, 6))
plt.plot(range(1, max_clusters + 1), inertia, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal Number of Clusters')
plt.xticks(np.arange(1, max_clusters + 1))
plt.grid(True)
plt.show()
