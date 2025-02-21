import os
import pandas as pd
from utils import *

# Mapeos y columnas objetivo para el esquema de Finance
DEFAULT_FINANCE_MAPPINGS = {
    'Revenue': ("Revenue", "annual_revenue_in_usd"),
    'MarketCap': ("MarketCap", "market_cap"),
    'Valuation': ("Valuation", "totalRaised", "valuation")
}
DEFAULT_FINANCE_TARGET_COLUMNS = ("Revenue", "MarketCap", "Valuation")

def extract_finance_info_from_csv(
    datasets_folder,           # Carpeta donde se encuentran los datasets (archivos Excel)
    csv_path=None,             # Ruta del CSV que contiene las columnas CompanyID, Name y Source (si se desea usar)
    path=None,                 # Ruta donde se guardará el Excel final
    possible_name_columns=DEFAULT_NAME_COLUMNS,
    column_mappings=DEFAULT_FINANCE_MAPPINGS,
    target_columns=DEFAULT_FINANCE_TARGET_COLUMNS,
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
    
    
    output_df = generate_company_ids(output_df, ['FinanceID', 'Name'], None, logger)
    output_df = output_df[['FinanceID', 'Name', 'Source']]

    
    output_df2 = output_df.set_index(['FinanceID', 'Name', 'Source']).copy()
    
    
    for filename in os.listdir(datasets_folder):
        try:
            file_path = os.path.join(datasets_folder, filename)
            df = pd.read_excel(file_path)
            df['Source'] = filename
            
            matching_name = extract_matching_column(possible_name_columns, df)
            if not matching_name:
                continue
                
            df.rename(columns={matching_name: 'Name'}, inplace=True)
            
            rename_matching_columns(df, column_mappings)
            df = df.drop_duplicates(subset=['Name'])
            
            
            new_data = df.set_index(['Name', 'Source']).reindex(columns=target_columns)
            new_data['FinanceID'] = output_df.set_index(['Name', 'Source'])['FinanceID']
            new_data = new_data.reset_index().set_index(['FinanceID', 'Name', 'Source'])
            
            output_df2 = pd.concat([output_df2, new_data], axis=0)
            
        except Exception as e:
            logger(f"Error processing {filename}: {e}")
    
    
    output_df2 = output_df2.reset_index()
    output_df2 = output_df2.groupby(['FinanceID', 'Name'], as_index=False).agg(
        lambda x: x.dropna().iloc[0] if not x.dropna().empty else pd.NA
    )
    
    
    desired_order = ["FinanceID", "Name"] + list(target_columns)
    output_df2 = output_df2[[col for col in desired_order if col in output_df2.columns]]
    
    logger()
    logger('_______________ Finished Finance Schema ___________________')
    try:
        output_df2.to_excel(path, index=False)
        logger(f"Información financiera guardada en: {path}")
    except Exception as e:
        logger(f"[ERROR] Al guardar el Excel: {e}")
