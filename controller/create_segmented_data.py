import pandas as pd
import json
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

client_response_output_path = 'C:/Users/User/Documents/Programas_Node/dados/output/client_response.json'

with open(client_response_output_path, 'r') as json_file:
    data = json_file.read()

clients_data = json.loads(data)
df = pd.DataFrame(clients_data).T

selected_properties = ['anual_income', 'avg_transaction', 'weighted_min_buy_ins']

scaler = StandardScaler()
df[selected_properties] = scaler.fit_transform(df[selected_properties])

num_clusters = 4
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(df[selected_properties])

output_cluster_file_path = './output/cluster_clients.csv'
df.to_csv(output_cluster_file_path, index_label='client_id')

print(f"Clustered data saved to {output_cluster_file_path}")
