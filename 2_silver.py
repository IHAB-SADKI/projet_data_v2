import pandas as pd
from sqlalchemy import create_engine

# 1. Connexion
moteur = create_engine('postgresql://postgres:admin@localhost:5432/postgres')

# 2. EXTRACTION
df_clients = pd.read_sql('clients_bronze_v2', con=moteur)
df_commandes = pd.read_sql('commandes_bronze_v2', con=moteur)

# 3. TRANSFORMATION (Le grand nettoyage)

# a. Gérer les doublons (On supprime les lignes strictement identiques)
df_clients = df_clients.drop_duplicates()
df_commandes = df_commandes.drop_duplicates()

# b. Texte : Majuscules
df_clients['nom'] = df_clients['nom'].str.capitalize()
df_clients['ville'] = df_clients['ville'].str.capitalize()

# c. Forcer l'âge en nombre (le texte devient NaN)
df_clients['age'] = pd.to_numeric(df_clients['age'], errors='coerce')

# d. Valeurs manquantes : Remplacer les valeurs vides par 0 (Ton choix)
df_clients['age'] = df_clients['age'].fillna(0)

# 4. CHARGEMENT
df_clients.to_sql('clients_silver_v2', con=moteur, if_exists='replace', index=False)
df_commandes.to_sql('commandes_silver_v2', con=moteur, if_exists='replace', index=False)

print("Succès : Couche Silver V2 générée (Doublons supprimés et âges vides mis à 0) !")