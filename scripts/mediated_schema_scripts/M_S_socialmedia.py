import os
import pandas as pd
from utils import *

# Mapeos y columnas objetivo para el esquema de Social Media
DEFAULT_SOCIAL_MEDIA_MAPPINGS = {
    'Platform': ("Facebook", "Twitter", "Instagram", "Pinterest"),
    'Url': ("link", "website")
}
DEFAULT_SOCIAL_MEDIA_TARGET_COLUMNS = ("Platform", "Url")

def extract_social_media_info_from_csv(
    datasets_folder,           # Carpeta donde se encuentran los datasets (archivos Excel)
    csv_path=None,             # Ruta del CSV (no se usa en este ejemplo, pero se deja por coherencia)
    path=None,                 # Ruta donde se guardará el Excel final
    possible_name_columns=DEFAULT_NAME_COLUMNS,
    column_mappings=DEFAULT_SOCIAL_MEDIA_MAPPINGS,
    target_columns=DEFAULT_SOCIAL_MEDIA_TARGET_COLUMNS,
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
            df = df.drop_duplicates(subset=["Name"])
            df["Source"] = filename
            output_df = pd.concat([output_df, df[["Name", "Source"]]], ignore_index=True)
        except Exception as e:
            logger(f"Error processing {filename}: {e}")
    
   
   
    output_df = generate_company_ids(output_df, ['SocialMediaID', 'Name'], None, logger)
    output_df = output_df[['SocialMediaID', 'Name', 'Source']]
    
   
    output_df2 = output_df.set_index(['SocialMediaID', 'Name', 'Source']).copy()
    
    
    for filename in os.listdir(datasets_folder):
        try:
            file_path = os.path.join(datasets_folder, filename)
            df = pd.read_excel(file_path)
            df["Source"] = filename
            matching_name = extract_matching_column(possible_name_columns, df)
            if not matching_name:
                continue
            df.rename(columns={matching_name: "Name"}, inplace=True)
            
            rename_matching_columns(df, column_mappings)
            df = df.drop_duplicates(subset=["Name"])
            
            
            new_data = df.set_index(["Name", "Source"]).reindex(columns=target_columns)
            new_data["SocialMediaID"] = output_df.set_index(["Name", "Source"])["SocialMediaID"]
            new_data = new_data.reset_index().set_index(["SocialMediaID", "Name", "Source"])
            
            output_df2 = pd.concat([output_df2, new_data], axis=0)
        except Exception as e:
            logger(f"Error processing {filename}: {e}")
    
    
    output_df2 = output_df2.reset_index()
    output_df2 = output_df2.groupby(["SocialMediaID", "Name"], as_index=False).agg(
        lambda x: x.dropna().iloc[0] if not x.dropna().empty else pd.NA
    )
    
    
    desired_order = ["SocialMediaID", "Name"] + list(target_columns)
    output_df2 = output_df2[[col for col in desired_order if col in output_df2.columns]]
    
    logger()
    logger('_______________ Finished Social Media Schema ___________________')
    try:
        output_df2.to_excel(path, index=False)
        logger(f"Social Media information saved to: {path}")
    except Exception as e:
        logger(f"[ERROR] Saving Excel: {e}")
