import sys
from Adaboost import Adaboost, collect_dataA, predict_dataA
from DecisionTree import DecisionTree, predict_data, collect_data


def main():
    # try:
        DT = DecisionTree(None,None,  None, None, 0,
                          None, None)
        ADA = Adaboost(None, None, None, 0)
        if sys.argv[1] == "train":
            if (sys.argv[4]) == 'ada' or (sys.argv[4]) is None:
                collect_dataA(sys.argv[2], sys.argv[3])
            else:
                collect_data(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "predict":
            if (sys.argv[4]) == 'ada' or (sys.argv[4]) is None:
                predict_dataA(sys.argv[2], sys.argv[3])
            else:
                predict_data(sys.argv[2], sys.argv[3])
    # except:
    #     print('Syntax :train <examples> <hypothesisOut> <learning-type>', '\nor',
    #           '\nSyntax :predict <hypothesis> <file> <testing-type(dt or ada)>')


if __name__ == '__main__':
    main()
