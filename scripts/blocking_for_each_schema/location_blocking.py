import recordlinkage
import pandas as pd

location_dataset = pd.read_excel('../Mediated Schema Excels/location_schema.xlsx')

def location_blocking():
    indexer = recordlinkage.Index()
    indexer.sortedneighbourhood('Address', window=3)
    candidate_links = indexer.index(location_dataset)
    
    # Eliminar pares duplicados
    candidate_links = candidate_links[~candidate_links.duplicated()]
    
    compare = recordlinkage.Compare()
    # Comparación para todos los campos relevantes
    compare.string('Address', 'Address', method='jarowinkler', label='address_sim')
    compare.string('City', 'City', method='jarowinkler', label='city_sim')
    compare.string('State', 'State', method='jarowinkler', label='state_sim')  # Nuevo
    compare.string('Country', 'Country', method='jarowinkler', label='country_sim')
    compare.string('Continent', 'Continent', method='jarowinkler', label='continent_sim')  # Comparación añadida
    compare_vectors = compare.compute(candidate_links, location_dataset)
    
    # Regla de matching con continent
    matched_pairs = compare_vectors[
        (compare_vectors['address_sim'] > 0.85) |
        (compare_vectors['city_sim'] > 0.9) | 
        (compare_vectors['country_sim'] > 0.95) |
        (compare_vectors['continent_sim'] > 0.97)  # Umbral alto por ser categoría cerrada
    ]
    
    # Dataframe final con todos los campos
    df = pd.DataFrame({
        "row_index_1": matched_pairs.index.get_level_values(0),
        "row_index_2": matched_pairs.index.get_level_values(1),
        "name_company_1": location_dataset.loc[matched_pairs.index.get_level_values(0), "Name"].values,
        "name_company_2": location_dataset.loc[matched_pairs.index.get_level_values(1), "Name"].values,
        "address_1": location_dataset.loc[matched_pairs.index.get_level_values(0), "Address"].values,
        "address_2": location_dataset.loc[matched_pairs.index.get_level_values(1), "Address"].values,
        "city_1": location_dataset.loc[matched_pairs.index.get_level_values(0), "City"].values,
        "city_2": location_dataset.loc[matched_pairs.index.get_level_values(1), "City"].values,
        "state_1": location_dataset.loc[matched_pairs.index.get_level_values(0), "State"].values,
        "state_2": location_dataset.loc[matched_pairs.index.get_level_values(1), "State"].values,
        "country_1": location_dataset.loc[matched_pairs.index.get_level_values(0), "Country"].values,
        "country_2": location_dataset.loc[matched_pairs.index.get_level_values(1), "Country"].values,
        "continent_1": location_dataset.loc[matched_pairs.index.get_level_values(0), "Continent"].values,
        "continent_2": location_dataset.loc[matched_pairs.index.get_level_values(1), "Continent"].values,
        "is_match": 1
    })
    
    df.to_csv("../blocking_excels/location_blocking.csv", index=False)

if __name__ == "__main__":
    location_blocking()