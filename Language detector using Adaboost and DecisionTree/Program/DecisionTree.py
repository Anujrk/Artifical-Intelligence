import math
import pickle

from Factors_checking import Factors


def predict_data(hypothesis_file, test_file):
    """
   Predict the language of a sentence
   :param hypothesis_file: Trained object file
   :param test_file: File to be tested
   :return: prediction of the sentence
   """
    file = open(test_file)
    sentence = ''
    count_word = 0
    sentence_list = []
    for line in file:
        words = line.split()
        for word in words:
            if count_word == 14:
                sentence += word
                sentence_list.append(sentence)
                sentence = ''
                count_word = 0
            else:
                sentence += word + " "
                count_word += 1
    factor1 = []
    factor2 = []
    factor3 = []
    factor4 = []
    factor5 = []
    factor6 = []
    factor7 = []
    factor8 = []
    factor9 = []
    factor10 = []
    factor11 = []
    factor12 = []
    factor13 = []
    factor14 = []

    fact = Factors()
    for line in sentence_list:
        factor1.append(fact.contains_Q(line))
        factor2.append(fact.contains_X(line))
        factor4.append(fact.word_length(line))
        factor5.append(fact.contains_van(line))
        factor6.append(fact.contains_de_het(line))
        factor7.append(fact.contains_een(line))
        factor8.append(fact.contains_en(line))
        factor9.append(fact.common_dutch_words(line))
        factor10.append(fact.common_english_words(line))
        factor11.append(fact.contains_a_an_the(line))
        factor12.append(fact.contains_and(line))
        factor13.append(fact.contains_voor(line))
        factor14.append(fact.contains_ik(line))
        factor3.append(fact.contains_E(line))
    factor = [factor1, factor2, factor4, factor5, factor6, factor7, factor8, factor9, factor10, factor11, factor12,
              factor13, factor14, factor3]
    hypothesis = pickle.load(open(hypothesis_file,'rb'))
    sentence_Index = 0
    for _ in sentence_list:
        data = hypothesis
        while data.boolean is not None and type(data.boolean) != str:
            value = factor[data.boolean][sentence_Index]
            data = data.next if not value else data.prev
        if data.boolean == 'nl':
            print(sentence_Index + 1, " : Dutch Sentence")
        elif data.boolean == 'en':
            print(sentence_Index + 1, " : English Sentence")
        else:
            print(sentence_Index + 1, " : Unknown Language")
        sentence_Index += 1


def collect_data(train_file, hypothesis_file):
    """
    Trains the Tree from the test_file and creates a hypothesis object file
    :param test_file: File to be predicted
    :param hypothesis_file: Obj file from training
    :return: hypothesis file that has been trained
    """
    file = open(train_file)
    sentence = ""
    for lines in file:
        sentence += lines
    split_sentence = sentence.split()
    sentence = sentence.split("|")
    sentence = sentence[1:]
    for index in range(len(sentence)):
        if index > 0:
            sentence[index] = sentence[index][:-4]
        else:
            continue
    results = []
    for words in split_sentence:
        if words.startswith("en|"):
            results.append("en")
        elif words.startswith("nl|"):
            results.append("nl")
        else:
            continue
    fact = Factors()
    factor1 = []
    factor2 = []
    factor3 = []
    factor4 = []
    factor5 = []
    factor6 = []
    factor7 = []
    factor8 = []
    factor9 = []
    factor10 = []
    factor11 = []
    factor12 = []
    factor13 = []
    factor14 = []
    for line in sentence:
        factor1.append(fact.contains_Q(line))
        factor2.append(fact.contains_X(line))
        factor4.append(fact.word_length(line))
        factor5.append(fact.contains_van(line))
        factor6.append(fact.contains_de_het(line))
        factor7.append(fact.contains_een(line))
        factor8.append(fact.contains_en(line))
        factor9.append(fact.common_dutch_words(line))
        factor10.append(fact.common_english_words(line))
        factor11.append(fact.contains_a_an_the(line))
        factor12.append(fact.contains_and(line))
        factor13.append(fact.contains_voor(line))
        factor14.append(fact.contains_ik(line))
        factor3.append(fact.contains_E(line))
    factor = [factor1, factor2, factor4, factor5, factor6, factor7, factor8, factor9, factor10, factor11, factor12,
              factor13, factor14, factor3]
    total_list = [x for x in range(len(results))]
    tree_root = DecisionTree(factor, results, total_list, 0, None, None, None)
    train(tree_root, results, factor, total_list, 0, None, [])
    hypothesis = open(hypothesis_file, 'wb')
    pickle.dump(tree_root, hypothesis)
    print("Successfully Trained model")


class DecisionTree:
    def __init__(self, factors, results, total_results, depth, seen, prediction, value):
        self.factors = factors
        self.results = results
        self.total_results = total_results
        self.depth = depth
        self.seen = seen
        self.prediction = prediction
        self.value = value
        self.boolean, self.prev, self.next = None, None, None


def train(tree_root, results, factor, total_list, depth, prevPrediction, seen):
    """
    Trains the decision tree to create object hypothesis file
    :param tree_root: root of the decision tree
    :param results: results of the train file
    :param factor: boolean values list
    :param total_list: list of values
    :param prevPrediction: prediction made for last node
    :param depth: depth of the tree
    :param seen: already predicted nodes
    :return: trained object file
    """
    value = results[total_list[0]]
    if value != results[len(results) - 1]:
        tree_root.boolean = value
    elif len(total_list) == 0:
        tree_root.boolean = prevPrediction
    elif depth == len(factor) - 1:
        nl_count = 0
        en_count = 0
        for i in total_list:
            if results[i] == 'nl':
                nl_count += 1
            elif results[i] == "en":
                en_count += 1
        if nl_count > en_count:
            tree_root.boolean = "nl"
        elif en_count > nl_count:
            tree_root.boolean = "en"
        else:
            tree_root.boolean = None
    else:
        resultsEng = 0
        resultsDut = 0

        for index in total_list:
            if results[index] == 'nl':
                resultsDut += 1
            else:
                resultsEng += 1
        temp = 0
        gain = []
        for index_attr in range(0, len(factor)):
            if index_attr not in seen:
                true_en = 0
                false_en = 0
                true_nl = 0
                false_nl = 0
                for index in total_list:
                    if factor[index_attr][index] and results[index] == 'nl':
                        true_nl += 1
                    elif factor[index_attr][index] and results[index] == 'en':
                        true_en += 1
                    elif not factor[index_attr][index] and results[index] == 'nl':
                        false_nl += 1
                    elif not factor[index_attr][index] and results[index] == 'en':
                        false_en += 1

                if true_en == 0 and true_nl == 0:
                    gain.append(temp)
                    continue

                if false_en == 0 and false_nl == 0:
                    gain.append(temp)
                    continue

                if true_nl == 0:
                    rem_true_value = 0
                    if (false_nl / (false_nl + false_en)) != 1:
                        rem_false_value = ((false_nl + false_en) / (resultsDut + resultsEng)) \
                                          * - ((false_nl / (false_nl + false_en)) * math.log((false_nl /
                                             (false_nl + false_en)),2.0) +(1 - (false_nl / (false_nl + false_en))) *
                                               math.log((1 - (false_nl / (false_nl + false_en))),2.0))
                    else:
                        rem_false_value = 0

                elif false_nl == 0:
                    rem_false_value = 0
                    if (true_nl / (true_nl + true_en)) != 1:
                        rem_true_value = ((true_nl + true_en) / (resultsDut + resultsEng)) \
                                         * -((true_nl / (true_nl + true_en)) * math.log(
                            (true_nl / (true_nl + true_en)),2.0) +(1 - (true_nl / (true_nl + true_en))) * math.log(
                                    (1 - (true_nl / (true_nl + true_en))),2.0))
                    else:
                        rem_true_value = 0
                else:
                    if (true_nl / (true_nl + true_en)) != 1:
                        rem_true_value = ((true_nl + true_en) / (resultsDut + resultsEng)) \
                                         * -((true_nl / (true_nl + true_en)) * math.log((true_nl / (true_nl + true_en)),
                            2.0) +(1 - (true_nl / (true_nl + true_en))) * math.log((1 - (true_nl / (true_nl + true_en))),
                                    2.0))
                    else:
                        rem_true_value = 0

                    if (false_nl / (false_nl + false_en)) != 1:
                        rem_false_value = ((false_nl + false_en) / (resultsDut + resultsEng)) \
                                          * -((false_nl / (false_nl + false_en)) * math.log((false_nl /( false_nl + false_en)),
                                             2.0) +(1 - (false_nl / (false_nl + false_en))) * math.log((1 - (false_nl /
                                             (false_nl + false_en))),2.0))
                    else:
                        rem_false_value = 0

                if (resultsDut / (resultsEng + resultsDut)) != 1:
                    gain_factor = (-((resultsDut / (resultsEng + resultsDut)) * math.log((resultsDut / (resultsEng + resultsDut)),
                        2.0) +(1 - (resultsDut / (resultsEng + resultsDut))) * math.log((1 - (resultsDut / (resultsEng + resultsDut))),
                        2.0))) - (rem_true_value + rem_false_value)
                else:
                    gain_factor = -(rem_true_value + rem_false_value)
                gain.append(gain_factor)

            else:
                gain.append(temp)
                continue
        current_prediction = "nl" if resultsDut > resultsEng else "en"
        maximum_gain = max(gain)
        if maximum_gain == temp:
            tree_root.boolean = prevPrediction
            return
        seen.append(gain.index(maximum_gain))
        true = []
        false = []
        undecided = []
        for i in total_list:
            if not factor[gain.index(maximum_gain)][i]:
                false.append(i)
            elif factor[gain.index(maximum_gain)][i]:
                true.append(i)
            else: undecided.append(i)
        tree_root.boolean = gain.index(maximum_gain)
        left_node = DecisionTree(factor,results,true,depth+1,None,current_prediction,True)
        right_node = DecisionTree(factor,results,false,depth+1,None,current_prediction,False)
        tree_root.prev = left_node
        tree_root.next = right_node
        train(left_node,results,factor,true,depth+1,current_prediction,seen)
        train(right_node,results,factor,false,depth+1,current_prediction,seen)
        del seen[-1]

