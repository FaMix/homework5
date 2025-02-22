import recordlinkage
import pandas as pd

finance_dataset = pd.read_excel('../Mediated Schema Excels/finance_schema.xlsx')

def finance_blocking():
    indexer = recordlinkage.Index()
    indexer.sortedneighbourhood('Name', window=3)
    candidate_links = indexer.index(finance_dataset)
    compare = recordlinkage.Compare()
    compare.string('Name', 'Name', method='jarowinkler', label='name_similarity')
    compare_vectors = compare.compute(candidate_links, finance_dataset)
    
    matched_pairs = compare_vectors[compare_vectors['name_similarity'] > 0.91]

    df = pd.DataFrame({
        "row_index_1": finance_dataset.index.get_indexer(matched_pairs.index.get_level_values(0)) + 2,
        "row_index_2": finance_dataset.index.get_indexer(matched_pairs.index.get_level_values(1)) + 2,
        "name_company_1": finance_dataset.loc[matched_pairs.index.get_level_values(0), "Name"].values,
        "name_company_2": finance_dataset.loc[matched_pairs.index.get_level_values(1), "Name"].values,
        "similarity_score": matched_pairs["name_similarity"].values,
        "is_match": 1
    })

    df.to_excel("../blocking_excels/finance_blocking.xlsx", index=False)


if __name__==__name__:
    finance_blocking()