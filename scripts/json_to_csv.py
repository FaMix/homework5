import json
import csv


"""
CODE FOR CONVERTING FROM JSONL TO CSV
"""
# # File paths
# jsonl_file = r"C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\carpeta\dataset19.jsonl"
# csv_file = r"C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\carpeta\dataset19.csv"

# # Open the JSONL file and CSV file
# with open(jsonl_file, 'r') as jfile, open(csv_file, 'w', newline='') as cfile:
#     # Load the first line to get the keys for the CSV header
#     first_line = json.loads(jfile.readline())
#     fieldnames = first_line.keys()

#     # Write the CSV header
#     writer = csv.DictWriter(cfile, fieldnames=fieldnames)
#     writer.writeheader()

#     # Write the first line
#     writer.writerow(first_line)

#     # Process remaining lines
#     for line in jfile:
#         record = json.loads(line)
#         writer.writerow(record)

# print(f"JSONL has been converted to CSV and saved as {csv_file}")


"""
CODE FOR COVERTING FROM JSON TO CSV
"""

# Rutas de los archivos
json_file = r"C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\carpeta\dataset17.json"
csv_file = r"C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\carpeta\dataset17.csv"

# Abrir el archivo JSON y cargar los datos
with open(json_file, 'r', encoding='utf-8') as jfile:
    data = json.load(jfile)

# Verificar que el JSON no esté vacío
if not data:
    print("El archivo JSON está vacío.")
    exit()

# Obtener los nombres de las columnas a partir del primer registro
fieldnames = data[0].keys()

# Abrir el archivo CSV para escribir los datos
with open(csv_file, 'w', newline='', encoding='utf-8') as cfile:
    writer = csv.DictWriter(cfile, fieldnames=fieldnames)
    writer.writeheader()

    # Escribir cada registro en el CSV
    for record in data:
        writer.writerow(record)

print(f"El archivo JSON se ha convertido a CSV y se ha guardado como {csv_file}")
