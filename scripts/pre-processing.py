import pandas as pd
import numpy as np

# === 1. Chargement des fichiers ===
synop = pd.read_excel("Donnees_journalieres_synop.xls")
trihoraire = pd.read_excel("donnees_trihoraire_vent_Ouahigouya_Po.xlsx")
pluie_voisine = pd.read_excel("Pluie_journalierei_stations.xls")

# ========= Affichage des variables et des noms de colonnes ======
print("Tableau synop : ", synop.columns)         # Pour vérifier si c'est 'Année' ou 'Annee'
print("\n")
print("Tableau trihoraire : ", trihoraire.columns)
print("\n")
print("Tableau pluie voisine : ", pluie_voisine.columns)

# === 2. Nettoyage de base : formats, valeurs manquantes ===
def preprocess(df):
    df = df.drop_duplicates()
    df = df.replace(['NA', '-', '', 'NaN'], np.nan)
    return df

synop = preprocess(synop)
trihoraire = preprocess(trihoraire)
pluie_voisine = preprocess(pluie_voisine)

# === 3. Création d'une colonne Date pour fusion ===
def build_date(df):
    df = df.rename(columns={'Annee': 'year', 'Mois': 'month', 'Jour': 'day'})
    return pd.to_datetime(df[['year', 'month', 'day']])

synop["Date"] = build_date(synop)
trihoraire["Date"] = build_date(trihoraire)
pluie_voisine["Date"] = build_date(pluie_voisine)

# === 4. Moyenne journalière des vitesses de vent ===

# On sélectionne toutes les colonnes après 'Jour' qui contiennent des valeurs numériques
colonnes_numeriques = trihoraire.columns[4:]  # À partir de la 5e colonne
colonnes_numeriques = [col for col in colonnes_numeriques if trihoraire[col].dtype in [np.float64, np.int64, object]]

# Conversion des valeurs en float et moyenne
trihoraire['Vitesse_moy'] = trihoraire[colonnes_numeriques].apply(pd.to_numeric, errors='coerce').mean(axis=1)

vent = trihoraire[['Date', 'Vitesse_moy']]


# === 5. Moyenne journalière des pluies des 4 stations voisines ===
stations = ['Yako', 'Manga', 'Zabré', 'Bitou']
pluie_voisine['Pluie_moy_voisine'] = pluie_voisine[stations].astype(float).mean(axis=1)
pluie_moyenne = pluie_voisine[['Date', 'Pluie_moy_voisine']] # Pluie moyenne sans l'affichage des 4 stations dans le tableau
#pluie_moyenne = pluie_voisine[['Date', 'Pluie_moy_voisine'] + stations]

# === 6. Fusion finale ===
df_final = synop.merge(vent, on="Date", how="left")
df_final = df_final.merge(pluie_moyenne, on="Date", how="left")

# === 7. Nettoyage final : interpoler les valeurs manquantes ===
df_final.interpolate(method='linear', inplace=True)
df_final.fillna(method='bfill', inplace=True)
df_final.fillna(method='ffill', inplace=True)

# === 8. Calcul de l'évaporation estimée ===

# 1. Nettoyage des colonnes nécessaires
df_final = df_final.copy()
df_final['TCM'] = df_final['TCM=(Tmin+Tmax)/2'].astype(float)
df_final['Humidite_moy'] = (
    df_final[['Humidité relative MAX', 'Humidité relative MIN']]
    .astype(float)
    .mean(axis=1)
)

# 2. Formule d’estimation empirique simplifiée
df_final['Evap_estimee'] = (
    0.5 * df_final['Insolation'].astype(float) +
    0.3 * df_final['TCM'] +
    0.2 * df_final['Vitesse_moy'] -
    0.1 * df_final['Humidite_moy']
)

# (Optionnel) Remplacer les valeurs négatives (évaporation ne peut pas être < 0)
df_final['Evap_estimee'] = df_final['Evap_estimee'].clip(lower=0)
print("✅ Colonne 'Evap_estimee' ajoutée avec succès.")

# === 9. Sauvegarde au format CSV ===
df_final.to_csv("donnees_climat_evaporation.csv", index=False)
print("✅ Données nettoyées et sauvegardées dans 'donnees_climat_evaporation.csv'")
