# Estimation de l'évaporation de l'eau en environnement semi-aride par Machine Learning

Ce projet a pour objectif de prédire l'évaporation quotidienne d'un plan d'eau (en mm/jour) à partir de données climatiques observées, en s'appuyant sur des techniques de machine learning, dont les réseaux de neurones (ANN).

## Structure du projet

├── data/
│   └── cleaned/donnees_climat_evaporation.csv  # Données prétraitées
├── models/
│   ├── modele_ann.joblib                       # Modèle ANN sauvegardé
│   └── scaler_ann.joblib                       # StandardScaler sauvegardé
├── notebooks/
│   ├── 01_exploration_donnees.ipynb
│   ├── 02_modeles_baselines.ipynb
│   └── 03_ann_prediction_evaporation.ipynb
└── README.md

## Objectif

L'évaporation n'étant pas directement mesurée dans les données, une estimation physique simplifiée basée sur les modèles Penman et Priestley-Taylor a été utilisée comme cible (`Evap_estimee`), à partir des variables suivantes :

* Température (moyenne, min, max)
* Insolation (ensoleillement)
* Vitesse moyenne du vent
* Humidité relative
* Précipitations locales et régionales

## 01 – Exploration des données (`01_exploration_donnees.ipynb`)

L'exploration a permis de :

* Vérifier la distribution des variables,
* Identifier les corrélations fortes avec l’évaporation (`Insolation`, `Température`, `Vent`, `Humidité`),
* Visualiser les relations via des scatterplots.

**Corrélations fortes avec `Evap_estimee` :**

* `Insolation` (≈ +0.8)
* `TCM=(Tmin+Tmax)/2` (≈ +0.6)
* `Humidité relative MIN` (≈ -0.5)

## 02 – Modèles baselines (`02_modeles_baselines.ipynb`)

Deux modèles classiques ont été entraînés :

### Régression linéaire

* **RMSE** : `0.030` mm/j
* **MAE**  : `0.005` mm/j
* **R²**   : `1`

### Forêt aléatoire (Random Forest)

* **RMSE** : `0.235` mm/j
* **MAE**  : `0.170` mm/j
* **R²**   : `0.996`

La forêt aléatoire obtient de meilleurs scores (R² plus proche de 1), indiquant qu’elle capture mieux les non-linéarités.

## 03 – Réseau de neurones artificiel (ANN) (`03_ann_prediction_evaporation.ipynb`)

Un modèle MLP (Multi-Layer Perceptron) a été entraîné après standardisation des données :

* Architecture : `(50, 30)`
* **RMSE** : `0.067` mm/j
* **MAE**  : `0.047` mm/j
* **R²**   : `1.000`

Le modèle ANN surpasse la régression linéaire et rivalise avec la forêt aléatoire.

## Résumé des résultats

| Modèle              | RMSE (↓) | MAE (↓) | R² (↑) |
|---------------------|----------|---------|--------|
| Régression linéaire | 0.030    | 0.005   | 1.000  |
| Random Forest       | 0.235    | 0.170   | 0.996  |
| ANN (MLP)           | 0.067    | 0.047   | 1.000  |

## Interprétation des métriques

- **RMSE (Root Mean Squared Error)** : erreur moyenne entre les prédictions et la vérité. Elle pénalise davantage les grosses erreurs. Plus elle est **proche de 0**, meilleure est la précision.
  
- **MAE (Mean Absolute Error)** : erreur moyenne absolue. Elle indique de combien (en mm/jour) le modèle se trompe **en moyenne**.

- **R² (Coefficient de détermination)** : mesure la part de variance expliquée par le modèle. Une valeur de **1.0** indique une **prédiction parfaite**. Si R² ≈ 0.996, le modèle explique 99.6% de la variabilité de l’évaporation.

Dans notre cas :
- Les modèles atteignent une **très bonne précision**.
- L’ANN et la forêt aléatoire sont capables de généraliser la relation climat → évaporation.
- Le **RMSE < 0.1 mm/j** montre une erreur négligeable.

## Conclusion

- Le projet montre qu’un modèle ML peut prédire avec précision l’évaporation journalière à partir des données climatiques.
- En l’absence de mesures d’évaporation réelles, la cible estimée reste une bonne approximation physique.
- Le réseau de neurones (ANN) et la forêt aléatoire montrent tous deux de très bonnes performances.
