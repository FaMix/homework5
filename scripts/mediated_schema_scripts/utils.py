import os
import uuid
import pandas as pd

# Constantes compartidas
DEFAULT_NAME_COLUMNS = ("brand name", "company", "name")

# Funciones compartidas
def extract_matching_column(posible_columnas, df):
    """Encuentra la primera columna que coincida (case-insensitive) con posible_columnas."""
    posibles_lower = [col.lower() for col in posible_columnas]
    for col in df.columns:
        if col.lower() in posibles_lower:
            return col
    return None

def rename_matching_columns(df, column_mappings):
    """Renombra columnas según los mapeos proporcionados."""
    for new_col, posibles in column_mappings.items():
        for col in df.columns:
            if col.lower() in [p.lower() for p in posibles]:
                df.rename(columns={col: new_col}, inplace=True)
                break


def question(parameter, path):
    print(f"Do you want to {parameter}? (y/n)")
    check_file(path)  
    answer = input().strip().lower()  

    try:
        if answer == "y":
            return "y"
        elif answer == "n":
            return "n"
        else:
            print("[ERROR] --> Did you answer correctly? Try again")
            return question(parameter, path)  
    except Exception as e:
        raise Exception(f"[ERROR] --> {e}")  

def check_file(path):
    try:
        if os.path.exists(path):
            print("[WARNING] --> You already have that file. If 'y' then you are going to overwrite it")
        else:
            print("[INFO] --> The file does not exist.") 
    except Exception as e:
        raise Exception(f"[ERROR] --> Unable to check whether the file exists in this path: {path}")
