import math
import pickle

from Factors_checking import Factors

def predict_dataA(hypothesis_file, test_file):
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
    hypothesis = pickle.load(open(hypothesis_file, 'rb'))
    indexing = 0
    weight, hypothesisList = hypothesis[1], hypothesis[0]
    for _ in sentence_list:
        total_sum = 0
        for index in range(len(hypothesisList)):  # changed
            if not factor[hypothesisList[index].boolean][indexing]:
                total_sum += weight[index] if hypothesisList[index].prev.boolean == 'nl' else -weight[index]
            else:
                total_sum += weight[index] if hypothesisList[index].next.boolean == 'nl' else -weight[index]

        print(indexing + 1, ': Dutch Sentence') if total_sum <= 0 else print(indexing + 1, ': English Sentence')
        indexing += 1


def collect_dataA(train_file, hypothesis_file):
    """
    Reads the test file and hypothesis file to print the output from prediction
    :param train_file: File to be tested
    :param hypothesis_file: Trained obj File
    :return: trained hypothesis
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
    stumps = []
    no_of_stumps = 100
    weights = []
    for i in range(no_of_stumps):
        weights.append(1)
    total_list = [x for x in range(len(results))]
    weight_new = []
    for i in range(len(sentence)):
        weight_new.append(1 / len(sentence))
    for hypothesis in range(no_of_stumps):
        tree_root = Adaboost(factor, results, total_list, 0)
        stump = Train(weight_new, tree_root, results, total_list, factor, 0)
        error = 0

        for index in range(0, len(sentence)):
            factor_value = stump.boolean
            if factor[factor_value][index]:
                factor_value = stump.prev.boolean
            else:
                factor_value = stump.next.boolean

            if factor_value == results[index]:
                continue
            else:
                error += weight_new[index]

        for index in range(len(sentence)):
            factor_value = stump.boolean
            if factor[factor_value][index]:
                factor_value = stump.prev.boolean
            else:
                factor_value = stump.next.boolean

            if factor_value != results[index]:
                continue
            else:
                weight_new[index] = weight_new[index] * error / (1 - error)

        sum = 0
        for i in weight_new:
            sum += i  # changed parameter
        for index in range(len(weight_new)):
            weight_new[index] = weight_new[index] / sum

        weights[int(hypothesis)] = math.log(((1 - error) / error), 10)
        stumps.append(stump)

    create_hypothesis = open(hypothesis_file, 'wb')
    pickle.dump((stumps, weights), create_hypothesis)
    print("Successfully Trained model")


class Adaboost:
    def __init__(self, factors, results, total_results, depth):
        self.factors = factors
        self.result = results
        self.total_results = total_results
        self.depth = depth
        self.boolean = None
        self.prev = None
        self.next = None

def Train(weights, tree_root, results, total_list, factors, depth):
    """
   Trains the tree using adaboost with help of stumps
   :param weights: weights calculated for the value
   :param tree_root: root of the decision tree
   :param results: output results
   :param depth: depth of the tree
   :param total_result: list of prediction
   :param factors: array of boolean values
   :return: object file of training set
   """
    resultsEng = 0
    resultsDut = 0

    for index in total_list:
        if results[index] == 'nl':
            resultsDut += 1 * weights[index]
        elif results[index] == 'en':
            resultsEng += 1 * weights[index]
        else:
            resultsEng = resultsEng, resultsDut = resultsDut

    temp = 0
    gain = []
    for index_attr in range(0, len(factors)):
        true_en = 0
        false_en = 0
        true_nl = 0
        false_nl = 0
        for index in total_list:
            if factors[index_attr][index] and results[index] == 'nl':
                true_nl += 1 * weights[index]
            elif factors[index_attr][index] and results[index] == 'en':
                true_en += 1 * weights[index]
            elif not factors[index_attr][index] and results[index] == 'nl':
                false_nl += 1 * weights[index]
            elif not factors[index_attr][index] and results[index] == 'en':
                false_en += 1 * weights[index]

        if true_nl == 0:
            rem_true_value = 0
            if (false_nl / (false_nl + false_en)) != 1:
                rem_false_value = ((false_nl + false_en) / (resultsDut + resultsEng)) \
                                  * - ((false_nl / (false_nl + false_en)) * math.log((false_nl /
                                                                                      (false_nl + false_en)), 2.0) + (
                                               1 - (false_nl / (false_nl + false_en))) *
                                       math.log((1 - (false_nl / (false_nl + false_en))), 2.0))
            else:
                rem_false_value = 0

        elif false_nl == 0:
            rem_false_value = 0
            if (true_nl / (true_nl + true_en)) != 1:
                rem_true_value = ((true_nl + true_en) / (resultsDut + resultsEng)) \
                                 * -((true_nl / (true_nl + true_en)) * math.log(
                    (true_nl / (true_nl + true_en)), 2.0) + (1 - (true_nl / (true_nl + true_en))) * math.log(
                    (1 - (true_nl / (true_nl + true_en))), 2.0))
            else:
                rem_true_value = 0
        else:
            if (true_nl / (true_nl + true_en)) != 1:
                rem_true_value = ((true_nl + true_en) / (resultsDut + resultsEng)) \
                                 * -((true_nl / (true_nl + true_en)) * math.log((true_nl / (true_nl + true_en)),
                                                                                2.0) + (
                                             1 - (true_nl / (true_nl + true_en))) * math.log(
                    (1 - (true_nl / (true_nl + true_en))),
                    2.0))
            else:
                rem_true_value = 0

            if (false_nl / (false_nl + false_en)) != 1:
                rem_false_value = ((false_nl + false_en) / (resultsDut + resultsEng)) \
                                  * -((false_nl / (false_nl + false_en)) * math.log((false_nl / (false_nl + false_en)),
                                                                                    2.0) + (
                                              1 - (false_nl / (false_nl + false_en))) * math.log((1 - (false_nl /
                                                                                                       (
                                                                                                               false_nl + false_en))),
                                                                                                 2.0))
            else:
                rem_false_value = 0

        if (resultsDut / (resultsEng + resultsDut)) != 1:
            gain_factor = (-(
                    (resultsDut / (resultsEng + resultsDut)) * math.log((resultsDut / (resultsEng + resultsDut)),
                                                                        2.0) + (
                            1 - (resultsDut / (resultsEng + resultsDut))) * math.log(
                (1 - (resultsDut / (resultsEng + resultsDut))),
                2.0))) - (rem_true_value + rem_false_value)
        else:
            gain_factor = -(rem_true_value + rem_false_value)
        gain.append(gain_factor)

    tree_root.boolean = gain.index(max(gain))
    count_true_en = 0
    count_true_nl = 0
    count_false_en = 0
    count_false_nl = 0

    for gain_temp in range(len(factors[gain.index(max(gain))])):
        if factors[gain.index(max(gain))][gain_temp]:
            if results[gain_temp] == 'nl':
                count_true_nl += 1 * weights[gain_temp]
            else:
                count_true_en += 1 * weights[gain_temp]
        else:
            if results[gain_temp] == 'nl':
                count_false_nl += 1 * weights[gain_temp]
            else:
                count_false_en += 1 * weights[gain_temp]

        prev_data = Adaboost(factors, results, None, depth + 1)
        next_data = Adaboost(factors, results, None, depth + 1)

        prev_data.boolean = 'nl' if count_true_en < count_true_nl else 'en'
        next_data.boolean = "nl" if count_false_en < count_false_nl else 'en'
        tree_root.prev = prev_data
        tree_root.next = next_data
        return tree_root
