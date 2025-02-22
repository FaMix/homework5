import os
import uuid
import pandas as pd
import sys

import M_S_company as company
import M_S_indutry as industry
import M_S_location as location
import M_S_finance as finance
import M_S_socialmedia as socialmedia


from utils import *

#you can change the name, but not the order
output_files = ("company_schema.xlsx", "industry_schema.xlsx", "location_schema.xlsx", "finance_schema.xlsx", "socialmedia_schema.xlsx")

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
class create_excels:

    def __init__(self, dataset_folder):
        self.dataset_folder =  dataset_folder
        self.directory = r"C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\Mediated Schema Excels" 
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
        

        #-------------------------------------------------------------------------------------------------------
        #setting up the correct output
        self.set_output_file(output_files[0])
        output = self.get_output_file()
        if output is None:
            raise Exception("[ERROR] --> No name for the output file. Check what you are doing!")
        
        
        #ask if the user wants or not to create the company schema file or not
        create = question("create the company schema", output)
        try:
            if create.lower() == "y":
                logger()
                logger('_______________ Starting to add all data to Company Schema ___________________')

                company.extract_company_dataframe(self.dataset_folder, name_and_id_dataframe, output)
                logger(f"Company schema saved to {output}")

            else:
                logger()
                logger("_________________Disabled company schema creation___________________")
                
        except Exception as e:
                raise Exception(f"[ERROR] --> Trying to create or not the company file but: {e}")
    
        #-------------------------------------------------------------------------------------------------------
        #setting up the correct output
        self.set_output_file(output_files[1])
        output = self.get_output_file()
        if output is None:
            raise Exception("[ERROR] --> No name for the output file. Check what you are doing!")
        

        #ask if the user wants or not to create the industry schema file or not 
        create = question("create the industry schema", output)
        try:
            if create.lower() == "y":
                logger()
                logger('_______________ Starting to add all data to Industry Schema ___________________')

                industry.extract_industry_info_from_csv(self.dataset_folder, None, output)
                logger(f"Company schema saved to {output}")

            else:
                logger()
                logger("_________________Disabled industry schema creation___________________")
                
        except Exception as e:
                raise Exception(f"[ERROR] --> Trying to create or not the industry file but: {e}")
        


        #setting up the correct output
        self.set_output_file(output_files[2])
        output = self.get_output_file()
        if output is None:
            raise Exception("[ERROR] --> No name for the output file. Check what you are doing!")
        
        create = question("create the location schema", output)
        try:
            if create.lower() == "y":
                logger()
                logger('_______________ Starting to add all data to Location Schema ___________________')
                location.extract_location_info_from_csv(self.dataset_folder, None, output)
                logger(f"Location schema saved to {output}")
            else:
                logger()
                logger("_________________Disabled location schema creation___________________")
        except Exception as e:
            raise Exception(f"[ERROR] --> Trying to create or not the location file but: {e}")
        


        #setting up the correct output
        self.set_output_file(output_files[3])
        output = self.get_output_file()
        if output is None:
            raise Exception("[ERROR] --> No name for the output file. Check what you are doing!")

        create = question("create the finance schema", output)
        try:
            if create.lower() == "y":
                logger()
                logger('_______________ Starting to add all data to Finance Schema ___________________')
                finance.extract_finance_info_from_csv(self.dataset_folder, None, output)
                logger(f"Finance schema saved to {output}")
            else:
                logger()
                logger("_________________Disabled finance schema creation___________________")
        except Exception as e:
            raise Exception(f"[ERROR] --> Trying to create or not the finance file but: {e}")
        


        #setting up the correct output
        self.set_output_file(output_files[4])
        output = self.get_output_file()
        if output is None:
            raise Exception("[ERROR] --> No name for the output file. Check what you are doing!")

        # Preguntar si se desea crear el esquema de Social Media
        create = question("create the social media schema", output)
        try:
            if create.lower() == "y":
                logger()
                logger('_______________ Starting to add all data to Social Media Schema ___________________')
                socialmedia.extract_social_media_info_from_csv(self.dataset_folder, None, output)
                logger(f"Social media schema saved to {output}")
            else:
                logger()
                logger("_________________Disabled social media schema creation___________________")
        except Exception as e:
            raise Exception(f"[ERROR] --> Trying to create or not the social media file but: {e}")


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
        
        output_df = generate_company_ids(output_df,['CompanyID', 'Name'], id_generator, logger)
        output_df = output_df[['CompanyID', 'Name', 'Source']]

        
        self.create_csv(output_df) #We create the csv file for the company, name and source, for later on, use it when doing the rest of the schema
        logger()
        logger('________________ Finished creating the CSV _______________________\n\n')
        logger()

        return 0






if __name__==__name__:
    run = create_excels(r'C:\Users\Dell XPS 9510\Desktop\java\t2\Homework5\homework5\datasets_excel_purified') #put here the directory were the datasets are
    run.create_corresponding_excel()




