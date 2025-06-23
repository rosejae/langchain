import meilisearch
import pandas as pd

client = meilisearch.Client('http://localhost:7700', 'aSampleMasterKey')

def bootstrap_stocks():
    df_stocks = pd.read_csv('nasdaq_screener_1750649212989.csv', na_filter=False)

    # df[df['Symbol'].str.contains(r'[^a-zA-Z0-9-_/^ ]', regex=True)]
    df_stocks['id'] = df_stocks['Symbol'].str.strip().replace(r'[/^]', '_', regex=True)
    dict_stocks = df_stocks.to_dict(orient='records')
    client.index('stocks').add_documents(dict_stocks, primary_key='id')

def search_stocks(query):
    return client.index('stocks').search(query)

def delete_stocks():
    client.delete_index('stocks')
    
if __name__ == '__main__':
    delete_stocks()
    bootstrap_stocks()