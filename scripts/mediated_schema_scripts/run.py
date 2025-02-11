import os
import uuid
import pandas as pd
import sys

import M_S_company as company
import M_S_indutry as industry


from utils import *


#----------------------------------------------------------------------------------------------------------------------------------------------------------------
class create_excels:

    def __init__(self, dataset_folder):
        self.dataset_folder =  dataset_folder
        self.directory = r"C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\mediates_schema_excels" 
        self.csv_file = os.path.join(self.directory, "c_n_s.csv")
        

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    def set_output_file(self, output):
        self.output_file = os.path.join(self.directory, output) 

    def get_output_file(self):
        return self.output_file




    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    def create_corresponding_excel(self, logger = print):
    
        logger("The CSV is esencial for the creating of the schemas. Without it, it is imposible, and the program will launch an error")
        logger()
        logger("If you answer yes to the next question, then you should answer yes to the rest if a appropied result is desired")
        create = question("create a csv file with the company id, the name, and its corresponding dataset", self.csv_file)
        try:
            if create.lower() == "y":
                logger()
                logger("_________________Creating the csv file, as you command it___________________")
                self.name_and_id_creation(self.dataset_folder)

            else:
                
                if not os.path.exists(self.csv_file):
                    logger("[ERROR] --> You don't have a csv file, please say 'y' now to create it!")
                    self.create_corresponding_excel(logger=print)
                
                logger()
                logger("_________________Function create_csv is disabled___________________")
        except Exception as e:
            raise Exception(f"[ERROR] --> Trying to create or not a csv file but: {e}")
                

        #reading the csv    
        try:
            name_and_id_dataframe = pd.read_csv(self.csv_file)
    
        except Exception as e:
            raise Exception(f"[ERROR] --> Unable to access the csv file when creating the company schema") 
        

        #setting up the correct output
        output = self.get_output_file()
        if output is None:
            raise Exception("[ERROR] --> No name for the output file. Check what you are doing!")
        
        
        #ask if the user wants or not to create the company schema or not file
        create = question("create the company schema", output)
        try:
            if create.lower() == "y":
                logger()
                logger('_______________ Starting to add all data to Company Dataframe ___________________')

                company.extract_company_dataframe(self.dataset_folder, name_and_id_dataframe, output)
                logger(f"Company schema saved to {output}")

            else:
                logger()
                logger("_________________Disabled company schema creation___________________")
                
            
        except Exception as e:
                raise Exception(f"[ERROR] --> Trying to create or not the compant file but: {e}")
    
        sys.exit()

    
    
    


    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    def create_csv(self, output_df=None, logger=print):
        output_file = self.csv_file
        if output_file:
            try:
                if output_file.endswith('.csv'):
                    output_df.to_csv(output_file, index=False)
                    logger(f"DataFrame saved like CSV in: {output_file}")
    
            except Exception as e:
                raise Exception(f"[ERROR] --> Tryin to create a csv but: {e}")

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------
    def name_and_id_creation(self, datasets_folder, possible_name_columns=DEFAULT_NAME_COLUMNS, id_generator=None, logger=print):
        
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
        
        # Generar IDs
        if not output_df.empty:
            if id_generator is None:
                # Comportamiento por defecto: UUID basado en nombre
                unique_names = output_df['Name'].unique()
                uuid_mapping = {name: str(uuid.uuid4()) for name in unique_names}
                output_df['CompanyID'] = output_df['Name'].map(uuid_mapping)
            else:
                output_df['CompanyID'] = id_generator(output_df)
            
            output_df = output_df[['CompanyID', 'Name', 'Source']]
        else:
            output_df = pd.DataFrame(columns=['CompanyID', 'Name', 'Source'])
        
        self.create_csv(output_df) #We create the csv file for the company, name and source, for later on, use it when doing the rest of the schema
        logger()
        logger('________________ Finished creating the CSV _______________________\n\n')
        logger()

        return 0






if __name__==__name__:
    run = create_excels(r'C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\datasets_excel_purified') #put here the directory were the datasets are
    
    #We start by creating the company schema
    run.set_output_file("company_schema.xlsx")
    run.create_corresponding_excel()



