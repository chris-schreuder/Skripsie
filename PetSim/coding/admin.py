import os
import time
import pandas as pd
from coding.feature_extraction import extract_features
from coding.dtw import getCost

class BaseValidation:

    def loadTrainingData(self):
        seq = []
        clusters = []
        for folder in os.listdir('./training'):
            if 'wav' not in folder:
                cluster = folder
                for file in os.listdir('./training/' + folder):
                    signal_seq = extract_features('./training/' + folder + '/' + file)
                    seq.append(signal_seq)
                    clusters.append(cluster)
        data = {'features': seq, 'names': clusters}
        return data

    def loadTestinggData(self):
        seq = []
        clusters = []
        for folder in os.listdir('./testing'):
            if 'wav' not in folder:
                cluster = folder
                for file in os.listdir('./testing/' + folder):
                    signal_seq = extract_features('./testing/' + folder + '/' + file)
                    seq.append(signal_seq)
                    clusters.append(cluster)
        data = {'features': seq, 'names': clusters}
        df = pd.DataFrame.from_dict(data)
        df.to_csv('./data/test.csv', index=False)
        return data

    def __init__(self):
        self.training = self.loadTrainingData()
        self.testing = self.loadTestinggData()
        self.testTime = 0
        self.allCosts = {'test': [], 'train': [], 'cost': [], 'costNorm': []}
        self.results = {'test': [], 'cost': [], 'costNorm': [], 'pred': []}
        self.accuracy = {'testNum':[], 'numTrain':[], 'numTest':[], 'totalComp': [], 'correct': [], 'incorrect': [], 'accuracy': [], 'time': []} 

    def genResults(self):
        start = time.time()
        allCosts_test = []
        allCosts_train = []
        allCosts_cost = []
        allCosts_costNorm = []
        allCosts_testSeq = []
        allCosts_trainSeq = []

        results_test = []
        results_cost = []
        results_costNorm = []
        results_pred = []
        results_testSeq = []
        results_trainSeq = []

        i = 0
        for testSeq, testName in zip(self.testing['features'], self.testing['names']):
            i += 1
            min_cost = 10
            min_costNorm = 10
            min_name = ''
            min_seq = []
            j = 0
            for trainSeq, trainNname in zip(self.training['features'], self.training['names']):
                j += 1
                print('Test: '+str(i)+'  Train: '+str(j))
                path, cost_mat, cost_mat_normalized = getCost(testSeq, trainSeq)
                allCosts_test.append(testName)
                allCosts_testSeq.append(testSeq)
                allCosts_train.append(trainNname)
                allCosts_trainSeq.append(trainSeq)
                allCosts_cost.append(cost_mat[-1, -1].tolist())
                allCosts_costNorm.append(cost_mat_normalized[-1, -1].tolist())
                cost= cost_mat_normalized[-1, -1].tolist()
                if cost < min_costNorm:
                    min_costNorm = cost_mat_normalized[-1, -1].tolist()
                    min_cost = cost_mat[-1, -1].tolist()
                    min_name = trainNname
                    min_seq = trainSeq
            results_test.append(testName)
            results_testSeq.append(testSeq)
            results_cost.append(min_cost)
            results_costNorm.append(min_costNorm)
            results_pred.append(min_name)
            results_trainSeq.append(min_seq)
        stop = time.time()
        self.testTime = (stop - start)

        self.allCosts = {'test': allCosts_test, 'train': allCosts_train, 'cost': allCosts_cost, 'costNorm': allCosts_costNorm, 'testSeq': allCosts_testSeq, 'trainSeq': allCosts_trainSeq}
        self.results = {'test': results_test, 'cost': results_cost, 'costNorm': results_costNorm, 'pred': results_pred, 'testSeq': results_testSeq, 'trainSeq': results_trainSeq}

    def getAccuracy(self):
        testNum = []
        numTrain = []
        numTest = []
        numComp = []
        correct = []
        incorrect = []
        accuracy = []
        testTime = []

        self.genResults()

        testNum.append(1)
        numTest.append(len(self.testing['names']))
        numTrain.append(len(self.training['names']))
        numComp.append(len(self.testing['names'])*len(self.training['names']))
        numCorrect = 0
        numIncorrect = 0
        for test, pred in zip(self.results['test'], self.results['pred']):
            if test == pred:
                numCorrect += 1
            else:
                numIncorrect += 1
        correct.append(numCorrect)
        incorrect.append(numIncorrect)
        accuracy.append((numCorrect)/(numCorrect+numIncorrect))
        testTime.append(self.testTime/60.00)

        self.accuracy = {'testNum': testNum, 'numTrain': numTrain, 'numTest': numTest, 'totalComp': numComp, 'correct': correct, 'incorrect': incorrect, 'accuracy': accuracy, 'time(min)': testTime} 

    def getAlCostDf(self):
        df = pd.DataFrame.from_dict(self.allCosts)
        df.to_csv('./data/base_allCosts.csv', index=False)
        return df

    def getResultsDf(self):
        df = pd.DataFrame.from_dict(self.results)
        df.to_csv('./data/base_results.csv', index=False)
        return df

    def getAccuracyDf(self):
        df = pd.DataFrame.from_dict(self.accuracy)
        df.to_csv('./data/base_accuracy.csv', index=False)
        return df

class Visualization:

    def __init__(self):
        self.allCosts = pd.read_csv('./data/base_allCosts1.csv')
        self.results =  pd.read_csv('./data/base_results1.csv')

    def getCosts(self):
        df = self.allCosts
        df.drop(['testSeq', 'trainSeq'], inplace=True, axis=1)
        return df

    def getResults(self):
        df = self.results
        df.drop(['testSeq', 'trainSeq'], inplace=True, axis=1)
        return df