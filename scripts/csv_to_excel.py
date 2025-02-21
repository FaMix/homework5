import os
import glob
import pandas as pd
import chardet  # Automatically detect the encoding of the CSV file

def clean_cell(value):
    """
    If the value is a string, remove newline characters and unnecessary spaces;
    otherwise, return it unchanged.
    """
    if isinstance(value, str):
        # Replace newline characters with a space and remove extra spaces at the beginning and end
        value = value.replace('/n', ' ').replace('\r', ' ').replace('\n', ' ').replace('\\n', ' ').replace('\\r', ' ').strip()
        # Optional: replace multiple internal spaces with a single one
        value = ' '.join(value.split())
    return value

def csv_to_excel_for_multiple(input_folder, output_folder, encoding='cp1252'):
    """
    Converts all CSV files in the folder 'input_folder' to Excel files (.xlsx),
    cleans each cell by removing newline characters and unnecessary spaces,
    and saves them in the 'output_folder'.
    """
    # Create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    # Search for all CSV files in the input folder
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

    if not csv_files:
        print("No CSV files found in the specified folder.")
        return

    # Process each CSV file found
    for csv_file in csv_files:
        try:
            # Detect encoding automatically
            with open(csv_file, 'rb') as f:
                result = chardet.detect(f.read())
            detected_encoding = result['encoding']
            #--------------------------------------------

            print(f"Processing: {csv_file}")
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file, encoding=detected_encoding)
            
            # Apply the cleaning function to each cell in the DataFrame
            df = df.map(clean_cell)
            
            # Get the base name of the file without extension
            base_name = os.path.splitext(os.path.basename(csv_file))[0]
            
            # Construct the full path for the output Excel file
            excel_file = os.path.join(output_folder, base_name + ".xlsx")
            
            # Save the DataFrame to an Excel file (without the index)
            df.to_excel(excel_file, index=False)
            print(f"Converted to: {excel_file}\n")
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")

if __name__ == '__main__':
    # Define the input folder where the CSV files are located
    input_folder = r"../csv_files"  # Example: "csv_data"
    
    # Define the output folder where the Excel files will be saved
    output_folder = r"../datasets_excel_purified"  # Example: "excel_data"

    csv_to_excel_for_multiple(input_folder, output_folder, encoding='cp1252')