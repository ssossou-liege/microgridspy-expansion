import pandas as pd

# 1. Charger les données du premier CSV
# (Remplacez 'premier_fichier.csv' par le vrai chemin de votre fichier)
df_long = pd.read_csv("premier_fichier.csv")

# 2. Pivoter la table
# On garde 'cluster', 'n_users' et 'appliance' en index (lignes)
# On transforme les modalités de 'parameter' en nouvelles colonnes
df_wide = df_long.pivot_table(
    index=["cluster", "n_users", "appliance"],
    columns="parameter",
    values="value",
    aggfunc="first",
).reset_index()

# 3. Renommer les colonnes pour correspondre exactement à la deuxième image
df_wide = df_wide.rename(columns={"n_users": "num_users", "appliance": "name"})

# 4. Insérer la colonne 'user_name' (qui semble vide dans votre exemple)
df_wide["user_name"] = ""

# 5. Définir l'ordre exact des colonnes de la seconde image
colonnes_ordonnees = [
    "cluster",
    "user_name",
    "num_users",
    "name",
    "number",
    "power",
    "func_time",
    "func_cycle",
    "occasional_use",
    "w1_start",
    "w1_end",
]

# On réorganise en s'assurant de ne pas planter si un paramètre est absent
colonnes_finales = [col for col in colonnes_ordonnees if col in df_wide.columns]
df_final = df_wide[colonnes_finales]

# 6. [Optionnel] Recréer l'effet "visuel" d'Excel où le numéro du cluster 
# et le nombre d'utilisateurs ne s'affichent que sur la première ligne du groupe :
df_final.loc[df_final.duplicated(subset=["cluster"]), ["cluster", "num_users"]] = ""

# 7. Sauvegarder le résultat dans le second CSV
df_final.to_csv("second_fichier.csv", index=False)

print("Transformation réussie ! Le second fichier a été généré.")
