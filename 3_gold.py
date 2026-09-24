import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# 1. Connexion
moteur = create_engine('postgresql://postgres:admin@localhost:5432/postgres')

# 2. LECTURE : On prend nos données propres (Silver V2)
df_clients = pd.read_sql('clients_silver_v2', con=moteur)
df_commandes = pd.read_sql('commandes_silver_v2', con=moteur)

# 3. CROISEMENT (La jointure)
# On relie les commandes à chaque client
df_fusion = pd.merge(df_commandes, df_clients, left_on='client_id', right_on='id')

# 4. CRÉATION DU TABLEAU 1 : SEGMENTATION CLIENTS (Pour l'équipe de fidélisation)
df_segmentation = df_fusion.groupby(['client_id', 'nom', 'ville']).agg(
    nombre_achats=('id_commande', 'count'),
    chiffre_affaires_total=('montant', 'sum'),
    panier_moyen=('montant', 'mean') # On calcule la dépense moyenne par commande
).reset_index()

# On arrondit à 2 chiffres après la virgule
df_segmentation['chiffre_affaires_total'] = df_segmentation['chiffre_affaires_total'].round(2)
df_segmentation['panier_moyen'] = df_segmentation['panier_moyen'].round(2)

# On ajoute une logique "Métier" : Création de la catégorie VIP
# np.where fonctionne comme un =SI() sur Excel : SI le CA > 1000 ALORS "VIP" SINON "Standard"
df_segmentation['categorie_client'] = np.where(df_segmentation['chiffre_affaires_total'] > 1000, 'VIP', 'Standard')


# 5. CRÉATION DU TABLEAU 2 : ANALYSE DÉMOGRAPHIQUE (Pour l'équipe Marketing)
# On crée des tranches d'âge (les "0" iront dans la première catégorie)
limites_age = [-1, 1, 30, 50, 150] # -1 à 1, 1 à 30, etc.
noms_tranches = ['Âge inconnu', 'Moins de 30 ans', '30 à 50 ans', 'Plus de 50 ans']
df_fusion['tranche_age'] = pd.cut(df_fusion['age'], bins=limites_age, labels=noms_tranches)

# On calcule les revenus générés par ville ET par tranche d'âge
df_demographie = df_fusion.groupby(['ville', 'tranche_age'], observed=True).agg(
    chiffre_affaires=('montant', 'sum')
).reset_index()

df_demographie['chiffre_affaires'] = df_demographie['chiffre_affaires'].round(2)


# 6. CHARGEMENT DANS POSTGRESQL (Tables prêtes pour Tableau ou PowerBI)
df_segmentation.to_sql('gold_segmentation_clients_v2', con=moteur, if_exists='replace', index=False)
df_demographie.to_sql('gold_analyse_demographique_v2', con=moteur, if_exists='replace', index=False)

print("Succès : Les tableaux de bord avancés Gold V2 sont générés !")