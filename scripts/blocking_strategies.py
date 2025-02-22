import recordlinkage
import pandas as pd


company_dataset = pd.read_excel('../Mediated Schema Excels/company_schema.xlsx')

company_dataset['FirstThreeLetters'] = company_dataset['Name'].str[:3]

# Crear índice de Blocking
indexer2 = recordlinkage.Index()
indexer2.block(left_on='FirstThreeLetters')


candidate_links2 = indexer2.index(company_dataset)
indexer3 = recordlinkage.Index()
indexer3.sortedneighbourhood('Name', window=3)  # Ajusta el tamaño de la ventana
candidate_links3 = indexer3.index(company_dataset.loc[list(set(candidate_links2.get_level_values(0)))])

print(f'Total de pares después de combinación de métodos: {len(candidate_links3)}')


compare = recordlinkage.Compare()
compare.string('Name', 'Name', method='jarowinkler', label='name_similarity')

compare_vectors = compare.compute(candidate_links3, company_dataset)

# Filtrar los pares con similitud mayor a 0.85
filtered_pairs = compare_vectors[compare_vectors['name_similarity'] > 0.92]

print(f'Total de pares después del filtrado por similitud (>0.93): {len(filtered_pairs)}')
filtered_pairs_df = pd.DataFrame({
    "row_index_1": filtered_pairs.index.get_level_values(0),
    "row_index_2": filtered_pairs.index.get_level_values(1),
    "name_company_1": company_dataset.loc[filtered_pairs.index.get_level_values(0), "Name"].values,
    "name_company_2": company_dataset.loc[filtered_pairs.index.get_level_values(1), "Name"].values,
    "similarity_score": filtered_pairs["name_similarity"].values
})

# Guardar el resultado en un Excel
filtered_pairs_df.to_excel("filtered_company_pairs.xlsx", index=False)

