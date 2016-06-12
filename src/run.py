__author__ = 'farshadfahimi'

from src.configuration.Constants import Constants
from src.search_ranking.ProximitySearch import ProximitySearch
import csv
import pandas as pd

dataset_name = 'simplewiki.tsv'
dataset_path = Constants.dataset_path

search_string = input("Please enter the search term(s):")
proximity_search = ProximitySearch(search_string)

articles = []
article_numbers = []

with open(dataset_path + dataset_name, 'r') as file:

    reader = csv.reader(file, delimiter='\t')
    for article_number, article_title, article_body in reader:

        title_rank, title_has_all_terms, body_rank, body_has_all_terms = proximity_search.get_all_ranks(article_body.lower(), article_title.lower())
        article_numbers.append(article_number)
        articles.append([article_title, article_body, title_has_all_terms, title_rank, body_rank, body_has_all_terms])

    columns = ['title', 'body', 'title_has_all_terms', 'title_rank', 'body_rank', 'body_has_all_terms']
    articles_df = pd.DataFrame(articles, index=article_numbers, columns=columns)
    articles_df = articles_df.sort_values(['body_has_all_terms', 'body_rank', 'title_rank', 'title_has_all_terms'])
    # articles_df = articles_df.sort_values(['body_rank'])
    print(articles_df)




