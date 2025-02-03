import os
import glob
import pandas as pd
import chardet #detect automatically the encoding of the csv

def limpiar_celda(valor):
    """
    Si el valor es una cadena, elimina los saltos de línea y espacios
    innecesarios; en caso contrario, lo retorna sin cambios.
    """
    if isinstance(valor, str):
        # Reemplaza saltos de línea por un espacio y elimina espacios en exceso al inicio y al final
        valor = valor.replace('/n', ' ').replace('\r', ' ').replace('\n', ' ').replace('\\n', ' ').replace('\\r', ' ').strip()
        # Opcional: reemplazar múltiples espacios internos por uno solo
        valor = ' '.join(valor.split())
    return valor

def csv_a_excel_para_varios(entrada_carpeta, salida_carpeta, encoding='cp1252'):
    """
    Convierte todos los archivos CSV de la carpeta 'entrada_carpeta' a archivos Excel (.xlsx),
    limpia cada celda eliminando saltos de línea y espacios innecesarios, y los guarda en la
    carpeta 'salida_carpeta'.
    """
    # Crear la carpeta de salida si no existe
    if not os.path.exists(salida_carpeta):
        os.makedirs(salida_carpeta)
        print(f"Se creó la carpeta de salida: {salida_carpeta}")

    # Buscar todos los archivos CSV en la carpeta de entrada
    archivos_csv = glob.glob(os.path.join(entrada_carpeta, "*.csv"))

    if not archivos_csv:
        print("No se encontraron archivos CSV en la carpeta especificada.")
        return

    # Procesar cada archivo CSV encontrado
    for archivo_csv in archivos_csv:
        try:
            #Detect encoding automatically
            with open(archivo_csv, 'rb') as f:
                resultado = chardet.detect(f.read())
            encoding_detectado = resultado['encoding']
            #--------------------------------------------
            
            print(f"Procesando: {archivo_csv}")
            # Leer el archivo CSV en un DataFrame
            df = pd.read_csv(archivo_csv, encoding=encoding_detectado)
            
            # Aplicar la función de limpieza a cada celda del DataFrame
            df = df.map(limpiar_celda)
            
            # Obtener el nombre base del archivo sin extensión
            nombre_base = os.path.splitext(os.path.basename(archivo_csv))[0]
            
            # Construir la ruta completa para el archivo Excel de salida
            archivo_excel = os.path.join(salida_carpeta, nombre_base + ".xlsx")
            
            # Guardar el DataFrame en un archivo Excel (sin índice)
            df.to_excel(archivo_excel, index=False)
            print(f"Convertido a: {archivo_excel}\n")
        except Exception as e:
            print(f"Error procesando {archivo_csv}: {e}")

if __name__ == '__main__':
    # Definir la carpeta de entrada donde se encuentran los archivos CSV
    carpeta_entrada = r"C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\csv_files"  # Ejemplo: "datos_csv"
    
    # Definir la carpeta de salida donde se guardarán los archivos Excel
    carpeta_salida = r"C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\datasets_excel_purified"  # Ejemplo: "datos_excel"

    csv_a_excel_para_varios(carpeta_entrada, carpeta_salida, encoding='cp1252')
