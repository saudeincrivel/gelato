import pandas as pd
import math
import json
from utils import convert_numbers_to_strings
from utils import NpEncoder


dados_absolute_path = "C:/Users/User/Documents/Programas_Node/dados"
offer_types_output_path = "C:/Users/User/Documents/Programas_Node/dados/output/offer_events_map.json"
offer_performance_output_path = 'C:/Users/User/Documents/Programas_Node/dados/output/total_offer_performance.json'
campaign_performance_output_path = 'C:/Users/User/Documents/Programas_Node/dados/output/campaign_performance.json'
client_response_output_path = 'C:/Users/User/Documents/Programas_Node/dados/output/client_response.json'

correlation_matrix_output_path = 'C:/Users/User/Documents/Programas_Node/dados/output/correlation_matrix.csv'


def get_all_offer_events():
    offer_events_file = "./data/eventos_ofertas.csv"
    df = pd.read_csv(offer_events_file, index_col=0)
    json_data = df.reset_index().to_json(orient='records')
    return json.loads(json_data)


def get_offer_events_from(client_id, offer_id):
    offer_events_file = "./data/eventos_ofertas.csv"
    df = pd.read_csv(offer_events_file, index_col=0)

    filtered_df = df[(df['cliente'] == client_id) &
                     (df['id_oferta'] == offer_id)]
    json_data = filtered_df.reset_index().to_json(orient='records')

    return json.loads(json_data)


def create_offertypes_map_data_set():
    offer_types_file = f'{dados_absolute_path}/data/portfolio_ofertas.csv'
    types_df = pd.read_csv(offer_types_file, index_col=0)

    offer_events_file = f'{dados_absolute_path}/data/eventos_ofertas.csv'
    events_df = pd.read_csv(offer_events_file, index_col=0)

    print("Processing offer map...")
    print("Creating offer_Id to offer_events data_set..")
    type_event_map = []

    for _, offer_type_row in types_df.iterrows():
        offer_id = offer_type_row['id']
        offer_events = events_df[events_df['id_oferta']
                                 == offer_id].to_dict('records')
        type_event_map.append({offer_id: offer_events})

    print('[offer_id] : [] : events_array ... Map Finished built!')
    saveDataToFile(offer_types_output_path, type_event_map)
    return None


def saveDataToFile(file_path, data):
    print(f'writting data to {file_path}')
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return None


def readFile(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        data_list = json.load(file)
    return data_list


def create_offer_id_performance_numbers():
    print("Creating total offer_id performance data set..")
    lista = readFile(offer_types_output_path)
    mapa = {}

    for item in lista:
        for id_oferta, eventos_array in item.items():
            for evento in eventos_array:
                tipo = evento['tipo_evento']
                if id_oferta not in mapa:
                    mapa[id_oferta] = {}
                if tipo not in mapa[id_oferta]:
                    mapa[id_oferta][tipo] = 0

                mapa[id_oferta][tipo] += 1
            break
    saveDataToFile(offer_performance_output_path, mapa)
    return None


def create_campaign_sucess_data_set():
    print("Creating campaign stats sucess data_set...")
    offer_events_file = f'{dados_absolute_path}/data/eventos_ofertas.csv'
    events_df = pd.read_csv(offer_events_file, index_col=0)

    offer_received = 'oferta recebida'
    transaction_event = 'transacao'
    all_campaigns = []

    i = 0
    while i < len(events_df):
        row = events_df.iloc[i]
        tipo = row['tipo_evento']

        if tipo == offer_received:
            campaign = {}
            characteristics = {'offers_sent': {}}

            j = i
            while j < len(events_df) and events_df.iloc[j]['tipo_evento'] == offer_received:
                event_type = events_df.iloc[j]['tipo_evento']
                offer_id = events_df.iloc[j]['id_oferta']

                characteristics['total'] = characteristics.get('total', 0) + 1
                characteristics['offers_sent'][offer_id] = characteristics['offers_sent'].get(
                    offer_id, 0) + 1
                j += 1

            campaign['characteristics'] = characteristics

            stats = {'oferta_stats': {}}
            while j < len(events_df) and events_df.iloc[j]['tipo_evento'] != offer_received:
                offer_id = events_df.iloc[j]['id_oferta']
                event_type = events_df.iloc[j]['tipo_evento']
                stats[event_type] = stats.get(event_type, 0) + 1

                if event_type == transaction_event:
                    value = events_df.iloc[j]['valor']
                    stats['soma_valor'] = stats.get('soma_valor', 0) + value

                if event_type != transaction_event:
                    if offer_id not in stats['oferta_stats']:
                        stats['oferta_stats'][offer_id] = {}

                    stats['oferta_stats'][offer_id][event_type] = stats['oferta_stats'][offer_id].get(
                        event_type, 0) + 1

                j += 1

            campaign['stats'] = stats
            all_campaigns.append(campaign)

            i = j

    print('Number of campaigns: ', len(all_campaigns))
    print('saving campaigns performance pie graph information to file')
    saveDataToFile(campaign_performance_output_path, all_campaigns)
    return None


def create_client_response_data_set():
    print("creating client response data_set...")
    offer_events_file = f'{dados_absolute_path}/data/eventos_ofertas.csv'
    events_df = pd.read_csv(offer_events_file, index_col=0)

    clients_file = f'{dados_absolute_path}/data/dados_clientes.csv'
    clients_df = pd.read_csv(clients_file, index_col=0)

    offer_types_file = f'{dados_absolute_path}/data/portfolio_ofertas.csv'
    offer_types_df = pd.read_csv(offer_types_file, index_col=0)

    clients_response = {}
    i = 0

    def is_nan_value(value):
        return math.isnan(value)

    def get_all_offer_ids():
        offer_list = offer_types_df['id'].unique()
        return offer_list

    def get_clients_anual_income(client_id):
        row = clients_df.loc[clients_df['id'] == client_id]
        renda = row['renda_anual'].values[0]
        return renda if not is_nan_value(renda) else 0

    def get_minimum_value_for_offer(offer_id):
        row = offer_types_df.loc[offer_types_df['id'] == offer_id]
        return row['valor_minimo'].values[0] if not row.empty else 0

    def get_reward_for_offer(offer_id):
        row = offer_types_df.loc[offer_types_df['id'] == offer_id]
        return row['recompensa'].values[0] if not row.empty else 0

    def saveToFileWithEnconder(file_path, data):
        print(f'writting data to {file_path}')
        with open(file_path, 'w') as file:
            json.dump(data, file, cls=NpEncoder, indent=4)
        return None

    all_clients = []
    all_offer_ids = get_all_offer_ids()

    while (i < len(events_df)):
        row = events_df.iloc[i]
        client_id = row['cliente']
        offer_id = str(row['id_oferta'])
        event_type = row['tipo_evento']

        if client_id not in clients_response:
            all_clients.append(client_id)
            anual_income = get_clients_anual_income(client_id)
            clients_response[client_id] = {
                'frequency': 0,
                'total_spending': 0,
                'anual_income': anual_income,
                'avg_transaction': 0,
                'customer_value': 0,
                'concluded_offers': 0,
                'total_rewards': 0,
                'vis_rate': 0,
                'freq_min_value': {
                    '5': 0,
                    '7': 0,
                    '10': 0,
                    '20': 0,
                },
                'total_received': 0,
                'weighted_min_buy_ins': 0,
                'offer_received': {},
                'offer_visualized': {}
            }
            for offer_id in all_offer_ids:
                clients_response[client_id]['offer_received'][offer_id] = 0
                clients_response[client_id]['offer_visualized'][offer_id] = 0

        if (event_type == 'transacao'):
            value = row['valor']
            clients_response[client_id]['total_spending'] += value
            clients_response[client_id]['frequency'] += 1

        if (event_type == 'oferta concluida'):
            min_value = get_minimum_value_for_offer(offer_id)
            min_value_str = str(min_value)
            reward = get_reward_for_offer(offer_id)
            clients_response[client_id]['freq_min_value'][min_value_str] += 1
            clients_response[client_id]['concluded_offers'] += 1
            clients_response[client_id]['total_rewards'] += reward

        if (event_type == 'oferta recebida'):
            clients_response[client_id]['offer_received'][offer_id] += 1
            clients_response[client_id]['total_received'] += 1

        if (event_type == 'oferta visualizada'):
            clients_response[client_id]['offer_visualized'][offer_id] += 1

        i += 1

    # TODO: check grouping with variables (avg_transaction, customer_value, anual_income, concluded_offers, total_rewards, freq_min_value)
    print("Finished buildiong clients_response dataframe!")
    for client_id in all_clients:
        client_data = clients_response[client_id]
        freq = client_data['frequency']
        total_spending = client_data['total_spending']

        vis_sum = 0
        rec_sum = 0
        for offer_id in all_offer_ids:
            vis_cnt = client_data['offer_visualized'][offer_id]
            rec_cnt = client_data['offer_received'][offer_id]
            vis_sum += vis_cnt
            rec_sum += rec_cnt

        weighted_sum = 0
        for key, value in client_data['freq_min_value'].items():
            weighted_sum += int(key) * value
        client_data['weighted_min_buy_ins'] = weighted_sum

        if (rec_sum != 0):
            client_data['vis_rate'] = vis_sum / rec_sum
        else:
            client_data['vis_rate'] = 0

        if freq != 0:
            avg_transaction = total_spending / freq
            client_data['avg_transaction'] = avg_transaction
        else:
            client_data['avg_transaction'] = 0

    print("Saving data_response data set into file..")
    saveToFileWithEnconder(client_response_output_path, clients_response)
    return None


def load_clients_response_into_mem():
    print("Creating correlatio matrix..")
    json_data = readFile(client_response_output_path)
    data_list = [{'client_id': key, **value}
                 for key, value in json_data.items()]
    data_frame = pd.DataFrame(data_list)
    data_frame = data_frame[(data_frame['total_spending'] != 0) & (
        data_frame['anual_income'] != 0)]

    columns_to_drop = ['freq_min_value', 'offer_received',
                       'offer_visualized', 'client_id', 'customer_value']
    data_frame = data_frame.drop(columns=columns_to_drop)
    correlation_matrix = data_frame.corr()
    correlation_matrix.to_csv(correlation_matrix_output_path, index=True)
    return None

 

def add_cluster_to_clients_data():
    # Load the clients data
    def get_clients_data():
        clients_file = "./data/dados_clientes.csv"
        df = pd.read_csv(clients_file, index_col=0)
        return df

    clients_data = get_clients_data()

    # Read the cluster data
    cluster_file = "./output/cluster_clients.csv"
    cluster_df = pd.read_csv(cluster_file)

    # Iterate through clients_data and update cluster information
    for index, row in clients_data.iterrows():
        client_id = row['id']
        cluster_row = cluster_df[cluster_df['id'] == client_id]
        
        if not cluster_row.empty:
            cluster_value = cluster_row.iloc[0]['cluster']
            clients_data.at[index, 'cluster'] = cluster_value

    return clients_data

# def call():
 
#     clients_data_with_cluster = add_cluster_to_clients_data()

#     # Save the updated data to a new CSV file
#     output_file = "./output/clients_data_with_cluster.csv"
#     clients_data_with_cluster.to_csv(output_file)

#     print("Data with cluster information saved to", output_file)
 

#     print("finished!")
#     return None


# call()
