import csv

def csv_to_list(filename):
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data_list = [row for row in reader]
    return data_list

# Exemple d'utilisation
filename = 'votre_fichier.csv'  # Remplacez par le nom de votre fichier CSV
data = csv_to_list(filename)

# Affichage des données
for row in data:
    print(row)
