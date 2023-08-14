from pprint import pprint
import pandas as pd
import json

dados_absolute_path = "C:/Users/User/Documents/Programas_Node/dados"
offer_types_output_path = "C:/Users/User/Documents/Programas_Node/dados/output/offer_events_map.json"
offer_performance_output_path = 'C:/Users/User/Documents/Programas_Node/dados/output/total_offer_performance.json'
campaign_performance_output_path = 'C:/Users/User/Documents/Programas_Node/dados/output/campaign_performance.json'
client_response_output_path = 'C:/Users/User/Documents/Programas_Node/dados/output/client_response.json'
correlation_matrix_output_path = 'C:/Users/User/Documents/Programas_Node/dados/output/correlation_matrix.csv'

# 
def readFile(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        data_list = json.load(file)
    return data_list

# 
def get_campaign_performance_data():
    data = readFile(campaign_performance_output_path)
    return data;

# 
def get_offer_events_from(client_id, offer_id):
    offer_events_file = "./data/eventos_ofertas.csv"
    df = pd.read_csv(offer_events_file, index_col=0)
    filtered_df = df[(df['cliente'] == client_id) &
                     (df['id_oferta'] == offer_id)]
    json_data = filtered_df.reset_index().to_json(orient='records')
    return json.loads(json_data)

# clients
def get_clients_data():
    clients_file = "./output/clients_with_cluster.csv"
    df = pd.read_csv(clients_file, index_col=0)
    df['membro_desde'] = df['membro_desde'].astype(str)
    json_data = df.reset_index().to_json(orient='records')
    return json.loads(json_data)