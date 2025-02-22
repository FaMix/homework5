import recordlinkage
import pandas as pd

company_dataset = pd.read_excel('../Mediated Schema Excels/company_schema.xlsx')


def company_blocking():
    indexer = recordlinkage.Index()
    indexer.sortedneighbourhood('Name', window=3)
    candidate_links = indexer.index(company_dataset)
    compare = recordlinkage.Compare()
    compare.string('Name', 'Name', method='jarowinkler', label='name_similarity')
    compare_vectors = compare.compute(candidate_links, company_dataset)
    
    matched_pairs = compare_vectors[compare_vectors['name_similarity'] > 0.91]

    
    df = pd.DataFrame({
        "row_index_1": company_dataset.index.get_indexer(matched_pairs.index.get_level_values(0)) + 2,
        "row_index_2": company_dataset.index.get_indexer(matched_pairs.index.get_level_values(1)) + 2,
        "name_company_1": company_dataset.loc[matched_pairs.index.get_level_values(0), "Name"].values,
        "name_company_2": company_dataset.loc[matched_pairs.index.get_level_values(1), "Name"].values,
        "similarity_score": matched_pairs["name_similarity"].values,
        "is_match": 1
    })

    df.to_excel("../blocking_excels/company_blocking.xlsx", index=False)

if __name__==__name__:
    company_blocking()