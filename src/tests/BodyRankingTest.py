__author__ = 'farshadfahimi'


class BodyRankingTest():
    def __init__(self, body, search_string):
        self.body = body
        self.search_terms = search_string.split(' ')
        self.search_string_length = len(search_string)

    def body_ranking(self):

        # body ranking: the smaller the ranking it means that it is a better match
        # parameters taken to consideration
        # 1. distance between search terms
        # 2. order of appearance of search terms
        # 3. existance of search terms (in form of a penalty)
        # 4. there is a reward term added if compound terms appear more than one time.
        # therefore it if possible for body_rank to be negative

        body_rank = 0
        # penalty term for non-existence of a term
        body_term_non_existence_penalty = 0

        for i in range(len(self.search_terms)):
            term_one_indexes = self.term_indexes(self.search_terms[i])
            # graph node frequency for this term
            term_node_frequency = len(term_one_indexes)

            if term_node_frequency == 0:
                #adding a penalty for non-existence of a term
                body_term_non_existence_penalty += self.search_string_length
            else:
                #reward for frequent appearance of terms, it will not change anything
                # if not appeared or appeared once
                body_rank = body_rank - term_node_frequency + 1
                #lets calculate the distance and order to other terms
                #if there are more search terms lets calculate how distance affects the ranking
                if i < len(self.search_terms):
                    for j in range(i + 1, len(self.search_terms)):
                        #indexes of the another search term (second node of the graph to create the links)
                        term_two_indexes = self.term_indexes(self.search_terms[j])

                        link_rank = 0
                        for index_one in term_one_indexes:
                            for index_two in term_two_indexes:
                                if index_one < index_two:
                                    body_substring = self.body[index_one:index_two]
                                    #if order is following the order of search terms
                                    order = 0
                                else:
                                    title_substring = self.body[index_two:index_one]
                                    #if order is not following the order of search terms so it is penalty of 1
                                    #the penalties can be improved if there is a good dataset to learn from
                                    order = 1

                                term_two_frequency = len(term_one_indexes)
                                print(body_substring)
                                distance = body_substring.count(' ') - 1
                                # print(distance)
                                #adding distance and order for this graph link
                                #if distance of word matches search terms it will be perfect match
                                if distance == j-i-1 and order == 0:
                                    link_rank = 0
                                    break
                                else:
                                    link_rank = link_rank + distance + order

                            if link_rank == 0:
                                break

                            #adding the ranking for the link between two terms (in graph of search terms)
                            body_rank += float(link_rank)/term_two_frequency

        body_rank += body_term_non_existence_penalty

        return body_rank


    def term_indexes(self, term):

        index = 0
        indexes = []

        while index < len(self.body):
            index = self.body.find(term, index)
            if index == -1:
                return indexes
            indexes.append(index)
            index += len(term)

        return indexes


if __name__ == "__main__":
    body = "A great power is a nation or state that is able to influence other states in most of the world. That is possible because it has great economic, political and military strength. Its opinions are taken into account by other nations before taking diplomatic or military action. Characteristically, they have the ability to intervene militarily almost anywhere, and they also have soft, cultural power, often in the form of economic investment in less developed portions of the world. Great powers. The great powers today are:"
    search_string = 'great tower'
    # search_string = 'blabla'

    body_ranking = BodyRankingTest(body, search_string)
    body_ranking.body_ranking()