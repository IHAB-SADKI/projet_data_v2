import pandas as pd
import random
import numpy as np

# 1. Génération de 1200 clients avec des erreurs volontaires
villes = ['paris', 'Lyon', 'MARSEILLE', 'Toulouse', 'Bordeaux']
noms = ['dupont', 'Martin', 'DURAND', 'Bernard', 'thomas']
clients = []

for i in range(1, 1201):
    # On glisse des erreurs dans l'âge
    age = random.choice([25, 34, 45, 'vingt-cinq', np.nan, 50, 60, 'trente']) 
    clients.append([i, random.choice(noms), age, random.choice(villes)])

df_clients = pd.DataFrame(clients, columns=['id', 'nom', 'age', 'ville'])
# On utilise sep=';' pour que l'Excel français fasse de belles colonnes
df_clients.to_csv('clients_1000.csv', index=False, sep=';')

# 2. Génération de 3000 commandes liées à ces clients
commandes = []
for i in range(1, 3001):
    client_id = random.randint(1, 1200)
    montant = round(random.uniform(15.5, 899.9), 2)
    commandes.append([i, client_id, montant])

df_commandes = pd.DataFrame(commandes, columns=['id_commande', 'client_id', 'montant'])
# Idem, sep=';' pour les commandes
df_commandes.to_csv('commandes_1000.csv', index=False, sep=';')

print("Fichiers CSV propres générés avec succès !")