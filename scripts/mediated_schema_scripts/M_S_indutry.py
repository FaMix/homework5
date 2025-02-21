import os
import pandas as pd
from utils import *


DEFAULT_INDUSTRY_MAPPINGS = {
    'IndustryName': ("Industry", "Area of Activity", "categories", "company_business"),
    'Sector': ("Sector", "market", "type", "nature_of_business")
}
DEFAULT_INDUSTRY_TARGET_COLUMNS = ("IndustryName", "Sector")

def extract_industry_info_from_csv(
    datasets_folder,           # Carpeta donde se encuentran los datasets (archivos Excel)
    csv_path=None,                  # Ruta del CSV que contiene las columnas CompanyID, Name y Source
    path=None,         # Ruta donde se guardará el Excel final             # Orden deseado de columnas (por ejemplo: ["IndustryID", "CompanyID", "IndustryName", "Sector"])
    possible_name_columns=DEFAULT_NAME_COLUMNS,
    column_mappings=DEFAULT_INDUSTRY_MAPPINGS,
    target_columns=DEFAULT_INDUSTRY_TARGET_COLUMNS,
    logger=print
):
    output_df = pd.DataFrame(columns=["Name", "Source"])
    for filename in os.listdir(datasets_folder):
        try:
            logger(f'Processing file: {filename}') 
            file_path = os.path.join(datasets_folder, filename)
            df = pd.read_excel(file_path)
            matching_column = extract_matching_column(possible_name_columns, df)
            
            if not matching_column:
                logger(f"No matching name column found in {filename}, skipping.")
                continue
                
            df.rename(columns={matching_column: "Name"}, inplace=True)
            df = df.drop_duplicates(subset=['Name'])
            df['Source'] = filename
            output_df = pd.concat([output_df, df[['Name', 'Source']]], ignore_index=True)
            
        except Exception as e:
            logger(f"Error processing {filename}: {e}")
    
    output_df = generate_company_ids(output_df,['IndustryID', 'Name'], None, logger)
    output_df = output_df[['IndustryID', 'Name', 'Source']]

    output_df2 = output_df.set_index(['IndustryID', 'Name', 'Source']).copy()
    
    for filename in os.listdir(datasets_folder):
        try:
            #logger(f'Processing file: {filename}') 
            file_path = os.path.join(datasets_folder, filename)
            df = pd.read_excel(file_path)
            df['Source'] = filename
            
            matching_name = extract_matching_column(possible_name_columns, df)
            if not matching_name:
            #    logger(f"No name column found in {filename}, skipping.")
                continue
                
            df.rename(columns={matching_name: 'Name'}, inplace=True)
            rename_matching_columns(df, column_mappings)
            df = df.drop_duplicates(subset=['Name'])
            
            # Vincular con IDs existentes
            new_data = df.set_index(['Name', 'Source']).reindex(columns=target_columns)
            new_data['IndustryID'] = output_df.set_index(['Name', 'Source'])['IndustryID']
            new_data = new_data.reset_index().set_index(['IndustryID', 'Name', 'Source'])
            
            output_df2 = pd.concat([output_df2, new_data], axis=0)
            
        except Exception as e:
            logger(f"Error processing {filename}: {e}")
    

    output_df2 = output_df2.reset_index()
    output_df2 = output_df2.groupby(['IndustryID', 'Name'], as_index=False).agg(
        lambda x: x.dropna().iloc[0] if not x.dropna().empty else pd.NA
    )
    

    desired_order = ["IndustryID", "Name"] + list(target_columns)
    output_df2 = output_df2[[col for col in desired_order if col in output_df2.columns]]
    
    logger()
    logger('_______________ Finished Industry Schema ___________________')
    output_df2.to_excel(path, index=False)
