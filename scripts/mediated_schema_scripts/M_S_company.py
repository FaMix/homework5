import os
import uuid
import pandas as pd

datasets_folder = r'C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\datasets_excel_purified'
ownership_columns = ("ownership",)
name_columns = ("brand name", "company", "name")
foundedyear_columns = ("foundation year", "founded", "company_creation_date", "est_of_ownership", "registration date")
website_columns = ("url", "website", "link", "company_website")
employees_columns = ("size", "employees", "number_of_employees")
ceo_columns = ("ceo",)
telephone_columns = ("telephone",)
status_columns = ("company_status",)

actual_company_columns = ("Ownership", "FoundedYear", "Website", "Employees", "CEO", "Telephone", "Status")


#----------------------------------------------------------------------------------------------------------------------------------------------------------------
def name_and_id_creation(datasets_folder):
    output_df = pd.DataFrame(columns=["Name", "Source"])
    
    print('_______________ Starting initial creation of Company Dataframe with ID, Name, and Source fields __________________')
    
    for filename in os.listdir(datasets_folder):
        try:
            print(f'Processing file: {filename}') 
            file_path = os.path.join(datasets_folder, filename)
            df = pd.read_excel(file_path)
            matching_column = extract_matching_column(name_columns, df)
            if not matching_column:
                print(f"No matching name column found in {filename}, skipping.")
                continue
            df.rename(columns={matching_column: "Name"}, inplace=True)
            df = df.drop_duplicates(subset=['Name'])
            df['Source'] = filename
            output_df = pd.concat([output_df, df[['Name', 'Source']]], ignore_index=True)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    # Generate UUIDs based on unique Names
    if not output_df.empty:
        unique_names = output_df['Name'].unique()
        uuid_mapping = {name: str(uuid.uuid4()) for name in unique_names}
        output_df['CompanyID'] = output_df['Name'].map(uuid_mapping)
        # Reorder columns
        output_df = output_df[['CompanyID', 'Name', 'Source']]
    else:
        output_df = pd.DataFrame(columns=['CompanyID', 'Name', 'Source'])
    
    print('________________ Finished creating initial Company Dataframe _______________________\n\n')
    return output_df


#----------------------------------------------------------------------------------------------------------------------------------------------------------------
def extract_matching_column(possible_columns, df):
    for col in df.columns:
        if col.lower() in possible_columns:
            return col
    return None

def rename_matching_columns(df):
    column_mappings = {
        'Website': website_columns,
        'Ownership': ownership_columns,
        'FoundedYear': foundedyear_columns,
        'CEO': ceo_columns,
        'Status': status_columns,
        'Employees': employees_columns,
        'Telephone': telephone_columns
    }
     
    for new_col, possible_cols in column_mappings.items():
        for col in df.columns:
            if col.lower() in [c.lower() for c in possible_cols]:
                #print(f"Renaming column '{col}' to '{new_col}'")  # Debug
                df.rename(columns={col: new_col}, inplace=True)
                break

def extract_company_dataframe(datasets_folder, name_and_id_df):
    output_df = name_and_id_df.set_index(['CompanyID', 'Name', 'Source']).copy()
    
    print('_______________ Starting to add all the data to the Initial Company Dataframe __________________')
    for filename in os.listdir(datasets_folder):
        try:
            print(f'Processing file: {filename}') 
            file_path = os.path.join(datasets_folder, filename)
            df = pd.read_excel(file_path)
            df['Source'] = filename
            
            # Process name column
            matching_name = extract_matching_column(name_columns, df)
            if not matching_name:
                print(f"No name column found in {filename}, skipping.")
                continue
            df.rename(columns={matching_name: 'Name'}, inplace=True)
            
            #print(df)
            # Normalize other columns
            rename_matching_columns(df)
            df = df.drop_duplicates(subset=['Name'])
            
            # Prepare new data
            new_data = df.set_index(['Name', 'Source']).reindex(columns=actual_company_columns)
            new_data['CompanyID'] = name_and_id_df.set_index(['Name', 'Source'])['CompanyID']
            new_data = new_data.reset_index().set_index(['CompanyID', 'Name', 'Source'])
            
            # Merge data
            output_df = pd.concat([output_df, new_data], axis=0)
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    # Reset index and coalesce data
    output_df = output_df.reset_index()
    output_df = output_df.groupby(['CompanyID', 'Name'], as_index=False).agg(
        lambda x: x.dropna().iloc[0] if not x.dropna().empty else pd.NA
    )
    
    # Reorder columns
    desired_order = ["CompanyID", "Name"] + list(actual_company_columns)
    output_df = output_df[[col for col in desired_order if col in output_df.columns]]
    
    print('_______________ Finished adding all data for the Company Dataframe __________________')
    return output_df



#----------------------------------------------------------------------------------------------------------------------------------------------------------------
def create_company_excel(datasets_folder):
    name_and_id_dataframe = name_and_id_creation(datasets_folder)
    if not name_and_id_dataframe.empty:
        df = extract_company_dataframe(datasets_folder, name_and_id_dataframe)
        #print(df)
        output_path = r'C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\mediates_schema_excels\company_schema.xlsx'
        df.to_excel(output_path, index=False)
        print(f"Company schema saved to {output_path}")
    else:
        print("No data processed. Output file not created.")

create_company_excel(datasets_folder)