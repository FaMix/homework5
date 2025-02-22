import recordlinkage
import pandas as pd


industry_dataset = pd.read_excel('../Mediated Schema Excels/industry_schema.xlsx')

def industry_blocking():
    indexer = recordlinkage.Index()
    indexer.sortedneighbourhood('IndustryName', window=3) 
    candidate_links = indexer.index(industry_dataset)
    
    #eliminates duplicates like x and y, y and x. With this form, only x and y is stored
    candidate_links = candidate_links[~candidate_links.duplicated()]
    
    compare = recordlinkage.Compare()
    compare.string('IndustryName', 'IndustryName', method='jarowinkler', label='industry_similarity')
    compare.string('Sector', 'Sector', method='jarowinkler', label='sector_similarity')
    compare_vectors = compare.compute(candidate_links, industry_dataset)

    
    matched_pairs = compare_vectors[
        (compare_vectors['industry_similarity'] > 0.92) | (compare_vectors['sector_similarity'] > 0.96)
    ]

    
    df = pd.DataFrame({
        "row_index_1": matched_pairs.index.get_level_values(0),
        "row_index_2": matched_pairs.index.get_level_values(1),
        "name_company_1": industry_dataset.loc[matched_pairs.index.get_level_values(0), "Name"].values,
        "name_company_2": industry_dataset.loc[matched_pairs.index.get_level_values(1), "Name"].values,
        "industryname_1": industry_dataset.loc[matched_pairs.index.get_level_values(0), "IndustryName"].values,
        "industryname_2": industry_dataset.loc[matched_pairs.index.get_level_values(1), "IndustryName"].values,
        "sector_1": industry_dataset.loc[matched_pairs.index.get_level_values(0), "Sector"].values,
        "sector_2": industry_dataset.loc[matched_pairs.index.get_level_values(1), "Sector"].values,
        "industry_similarity_score": matched_pairs["industry_similarity"].values,
        "sector_similarity_score": matched_pairs["sector_similarity"].values,
        "is_match": 1
    })

    
    df.to_csv("../blocking_excels/industry_blocking.csv", index=False)


if __name__==__name__:
    industry_blocking()
