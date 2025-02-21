import os
import uuid
import pandas as pd

from utils import *

# Valores por defecto (originales)
DEFAULT_COLUMN_MAPPINGS = {
    'Website': ("url", "website", "link", "company_website"),
    'Ownership': ("ownership",),
    'FoundedYear': ("foundation year", "founded", "company_creation_date", "est_of_ownership", "registration date"),
    'CEO': ("ceo",),
    'Status': ("company_status",),
    'Employees': ("size", "employees", "number_of_employees"),
    'Telephone': ("telephone",)
}
DEFAULT_TARGET_COLUMNS = ("Ownership", "FoundedYear", "Website", "Employees", "CEO", "Telephone", "Status")


def extract_company_dataframe(datasets_folder, name_and_id_df, path=None, possible_name_columns=DEFAULT_NAME_COLUMNS, column_mappings=DEFAULT_COLUMN_MAPPINGS, target_columns=DEFAULT_TARGET_COLUMNS, logger=print):
    
    output_df = name_and_id_df.set_index(['CompanyID', 'Name', 'Source']).copy()
    
    for filename in os.listdir(datasets_folder):
        try:
            logger(f'Processing file: {filename}') 
            file_path = os.path.join(datasets_folder, filename)
            df = pd.read_excel(file_path)
            df['Source'] = filename
            
            matching_name = extract_matching_column(possible_name_columns, df)
            if not matching_name:
                logger(f"No name column found in {filename}, skipping.")
                continue
                
            df.rename(columns={matching_name: 'Name'}, inplace=True)
            rename_matching_columns(df, column_mappings)
            df = df.drop_duplicates(subset=['Name'])
            
            # Vincular con IDs existentes
            new_data = df.set_index(['Name', 'Source']).reindex(columns=target_columns)
            new_data['CompanyID'] = name_and_id_df.set_index(['Name', 'Source'])['CompanyID']
            new_data = new_data.reset_index().set_index(['CompanyID', 'Name', 'Source'])
            
            output_df = pd.concat([output_df, new_data], axis=0)
            
        except Exception as e:
            logger(f"Error processing {filename}: {e}")
    

    output_df = output_df.reset_index()
    output_df = output_df.groupby(['CompanyID', 'Name'], as_index=False).agg(
        lambda x: x.dropna().iloc[0] if not x.dropna().empty else pd.NA
    )
    

    desired_order = ["CompanyID", "Name"] + list(target_columns)
    output_df = output_df[[col for col in desired_order if col in output_df.columns]]
    
    logger()
    logger('_______________ Finished Company Schema ___________________')
    output_df.to_excel(path, index=False)