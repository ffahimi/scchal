__author__ = 'farshadfahimi'


class TitleRankingTest():
    def __init__(self, search_string):
        self.search_terms = search_string.split(' ')
        self.search_string_length = len(search_string)

    def rank_title(self, title):

        # title ranking: the smaller the ranking it means that it is a better match
        #  in terms of distance between words and existence of all terms in the order of search terms
        title_rank = 0
        #a count to keep track of appearances in title
        term_count_appeared = 0
        #indexes of search terms in title if available
        terms_indexes = self.get_terms_indexes(title)
        terms_frequencies, count_of_non_existing_terms, sum_of_term_frequencies = self.get_term_frequencies(terms_indexes)
        # penalty term for non-existence of a term
        #adding a penalty for non-existence of a term
        title_term_non_existence_penalty = count_of_non_existing_terms*self.search_string_length
        #reward for frequent appearance of terms, it will not change anything
        # if not appeared or appeared once
        title_rank = title_rank - sum_of_term_frequencies + 1

        #lets calculate the distance and order to other terms
        #if there are more search terms lets calculate how distance affects the ranking

        for i in range(len(self.search_terms)):
            term_one_indexes = terms_indexes[i]

            if i < len(self.search_terms):
                for j in range(i + 1, len(self.search_terms)):
                    #indexes of the another search term (second node of the graph to create the links)
                    term_two_indexes = terms_indexes[j]
                    #flag for compound search term match
                    compound_match = False
                    link_rank = 0
                    for index_one in term_one_indexes:
                        for index_two in term_two_indexes:
                            if index_one < index_two:
                                title_substring = title[index_one:(index_two - 1)]
                                #if order is following the order of search terms
                                order = 0
                            else:
                                title_substring = title[index_two:(index_one - 1)]
                                #if order is not following the order of search terms so it is penalty of 1
                                #the penalties can be improved if there is a good dataset to learn from
                                order = 1

                            distance = title_substring.count(' ') - 1
                            #adding distance and order for this graph link
                            #if distance of word matches search terms it will be perfect match
                            if distance == (j-i-1) and order == 0:
                                compound_match = True
                                link_rank = 0
                            else:
                                link_rank = link_rank + distance + order

                        if not compound_match:
                            if terms_frequencies[j] > 0:
                                #adding the ranking for the link between two terms (in graph of search terms)
                                title_rank += float(link_rank)/terms_frequencies[j]
                        else:
                            title_rank -= len(self.search_terms)

        title_rank += title_term_non_existence_penalty

        #An indicator to see if title has all search terms (0) or some (1) or one (2) or none (3)
        if count_of_non_existing_terms == 0:
            title_has_all_terms = 0
        elif (len(self.search_terms) - count_of_non_existing_terms) == 0:
            title_has_all_terms = 3
        elif (len(self.search_terms) - count_of_non_existing_terms) == 1:
            title_has_all_terms = 2
        else:
            title_has_all_terms = 1

        return title_rank, title_has_all_terms

    def get_terms_indexes(self, title):
        terms_indexes = []
        for i in range(len(self.search_terms)):
            terms_indexes.append(self.get_term_indexes(title, i))

        return terms_indexes

    def get_term_indexes(self, title, term_index):

        index = 0
        indexes = []

        while index < len(title):
            index = title.find(self.search_terms[term_index], index)
            if index == -1:
                return indexes
            indexes.append(index)
            index += len(self.search_terms[term_index])

        return indexes

    def get_term_frequencies(self, terms_indexes):

        terms_frequncies = []
        sum_of_term_frequencies = 0
        count_of_non_existing_terms_in_title = 0

        for term_indexes in terms_indexes:
            terms_frequncies.append(len(term_indexes))
            sum_of_term_frequencies += len(term_indexes)
            if len(term_indexes) == 0:
                count_of_non_existing_terms_in_title += 1

        return terms_frequncies, count_of_non_existing_terms_in_title, sum_of_term_frequencies




if __name__ == "__main__":
    # title = 'great tower of africa in desert tower for example great'
    title = 'nihilism'
    # search_string = 'great power'
    search_string = 'nihilism'

    title_ranking = TitleRankingTest(search_string)
    print(title_ranking.rank_title(title))