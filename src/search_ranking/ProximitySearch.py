__author__ = 'farshadfahimi'
from src.search_ranking.TitleRanking import TitleRanking
from src.search_ranking.BodyRanking import BodyRanking


#definition was read from wiki page for proximity page and not any packages
class ProximitySearch():

    def __init__(self, search_string):
        self.title_ranking = TitleRanking(search_string)
        self.body_ranking = BodyRanking(search_string)

    def get_all_ranks(self, body, title):
        title_rank, title_has_all_terms = self.get_title_rank(title)
        body_rank, body_has_all_terms = self.get_body_rank(body)
        return title_rank, title_has_all_terms, body_rank, body_has_all_terms

    def get_title_rank(self, title):
        title_rank, title_has_all_terms = self.title_ranking.rank_title(title)
        return title_rank, title_has_all_terms

    def get_body_rank(self, body):
        body_rank, body_has_all_terms = self.body_ranking.rank_body(body)
        return body_rank, body_has_all_terms