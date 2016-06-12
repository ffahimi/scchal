__author__ = 'farshadfahimi'

__author__ = 'farshadfahimi'


class BodyRanking():
    def __init__(self, search_string):
        self.search_terms = search_string.split(' ')
        self.search_string_length = len(search_string)

    def rank_body(self, body):

        # body ranking: the smaller the ranking it means that it is a better match
        #  in terms of distance between words and existence of all terms in the order of search terms
        body_rank = 0
        #a count to keep track of appearances in body
        term_count_appeared = 0
        #indexes of search terms in body if available
        terms_indexes = self.get_terms_indexes(body)
        terms_frequencies, count_of_non_existing_terms, sum_of_term_frequencies = self.get_term_frequencies(terms_indexes)
        # penalty term for non-existence of a term
        #adding a penalty for non-existence of a term
        body_term_non_existence_penalty = count_of_non_existing_terms*self.search_string_length
        #reward for frequent appearance of terms, it will not change anything
        # if not appeared or appeared once
        body_rank = body_rank - sum_of_term_frequencies + 1

        #lets calculate the distance and order to other terms
        #if there are more search terms lets calculate how distance affects the ranking

        for i in range(len(self.search_terms)):

            term_one_indexes = terms_indexes[i]
            #no need to continue the block if there is only one term
            if len(self.search_terms) == 1:
                continue

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
                                body_substring = body[index_one:index_two + len(self.search_terms[j])]
                                #if order is following the order of search terms
                                order = 0
                            else:
                                body_substring = body[index_two:index_one + len(self.search_terms[i])]
                                #if order is not following the order of search terms so it is penalty of 1
                                #the penalties can be improved if there is a good dataset to learn from
                                order = 1

                            distance = body_substring.count(' ') - 1

                            #if distance between words more than 10, skip and not consider as a valid link
                            if distance > 10:
                                continue

                            #adding distance and order for this graph link
                            #if distance of word matches search terms it will be perfect match
                            #if distance between words is less than 5 words consider them as compound (near)
                            if distance < 5 and order == 0:
                                compound_match = True
                                link_rank = 0
                            else:
                                link_rank = link_rank + distance + order

                        if not compound_match:
                            if terms_frequencies[j] > 0:
                                #adding the ranking for the link between two terms (in graph of search terms)
                                body_rank += float(link_rank)/terms_frequencies[j]
                        else:
                            body_rank -= 1.0*len(self.search_terms)

        body_rank += body_term_non_existence_penalty

        #An indicator to see if body has all search terms (0) or some (1) or one (2) or none (3)
        if count_of_non_existing_terms == 0:
            body_has_all_terms = 0.0
        elif (len(self.search_terms) - count_of_non_existing_terms) == 0:
            body_has_all_terms = 3.0
        elif (len(self.search_terms) - count_of_non_existing_terms) == 1:
            body_has_all_terms = 2.0
        else:
            body_has_all_terms = 1.0

        return body_rank, body_has_all_terms

    def get_terms_indexes(self, body):
        terms_indexes = []
        for i in range(len(self.search_terms)):
            terms_indexes.append(self.get_term_indexes(body, i))

        return terms_indexes

    def get_term_indexes(self, body, term_index):

        index = 0
        indexes = []

        while index < len(body):
            index = body.find(self.search_terms[term_index], index)
            if index == -1:
                return indexes
            indexes.append(index)
            index += len(self.search_terms[term_index])

        return indexes

    def get_term_frequencies(self, terms_indexes):

        terms_frequncies = []
        sum_of_term_frequencies = 0
        count_of_non_existing_terms_in_body = 0

        for term_indexes in terms_indexes:
            terms_frequncies.append(len(term_indexes))
            sum_of_term_frequencies += len(term_indexes)
            if len(term_indexes) == 0:
                count_of_non_existing_terms_in_body += 1

        return terms_frequncies, count_of_non_existing_terms_in_body, sum_of_term_frequencies


