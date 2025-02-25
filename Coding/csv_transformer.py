import csv

def csv_to_list(filename):
    """Transforme un fichier CSV en une liste de listes"""
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        data = [row for row in reader]
    return data
