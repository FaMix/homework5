import os
import glob
import pandas as pd


# Combine all the excels datasets into one big dataset xlsx
def combinar_excels_en_uno(carpeta_excels, archivo_salida):

    archivos_excel = glob.glob(os.path.join(carpeta_excels, "*.xlsx"))
    
    if not archivos_excel:
        print("[Error]: No excel found in the passed directory")
        return
    
    
    with pd.ExcelWriter(archivo_salida, engine='openpyxl') as writer:
        for archivo in archivos_excel:
            try:
                # Same name for the sheet as for the excel file
                nombre_hoja = os.path.splitext(os.path.basename(archivo))[0]
                print(f"Procesing: {archivo} in the sheet: {nombre_hoja}")
                
                
                df = pd.read_excel(archivo)
                df.to_excel(writer, sheet_name=nombre_hoja, index=False)
            
            except Exception as e:
                print(f"[Error]: Not able to proccess --> {archivo}: {e}")
    
    print(f"Big dataset xlsx created: {archivo_salida}")

if __name__ == '__main__':
    # Initial directory
    carpeta_excels = r"C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\datasets_excel_purified"
    
    # Final directory
    archivo_salida = r"C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\big_dataset.xlsx"
    
    combinar_excels_en_uno(carpeta_excels, archivo_salida)
