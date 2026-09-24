import pandas as pd
from sqlalchemy import create_engine

# 1. Connexion à ta base de données locale
moteur = create_engine('postgresql://postgres:admin@localhost:5432/postgres')

# 2. Lecture des fichiers CSV 
df_clients = pd.read_csv('clients_1000.csv', sep=';')
df_commandes = pd.read_csv('commandes_1000.csv', sep=';')

# 3. Chargement avec de NOUVEAUX noms pour protéger ton ancien projet
df_clients.to_sql('clients_bronze_v2', con=moteur, if_exists='replace', index=False)
df_commandes.to_sql('commandes_bronze_v2', con=moteur, if_exists='replace', index=False)

print("Succès : Les données brutes ont été ingérées dans les tables V2 de la couche Bronze !")