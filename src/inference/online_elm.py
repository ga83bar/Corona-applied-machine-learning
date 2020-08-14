# https://github.com/chickenbestlover/Online-Recurrent-Extreme-Learning-Machine/blob/master/algorithms/OS_ELM.py

import numpy as np
from numpy.linalg import pinv
import pandas as pd
from pathlib import Path

"""
Implementation of the online-sequential extreme learning machine
Reference:
N.-Y. Liang, G.-B. Huang, P. Saratchandran, and N. Sundararajan,
“A Fast and Accurate On-line Sequential Learning Algorithm for Feedforward
Networks," IEEE Transactions on Neural Networks, vol. 17, no. 6, pp. 1411-1423
"""

def sigmoidActFunc(features, weights, bias):
    assert features.shape[1] == weights.shape[1]
    (numSamples, numInputs) = features.shape
    (numHiddenNeuron, numInputs) = weights.shape
    V = np.dot(features, np.transpose(weights)) + bias
    H = 1 / (1+np.exp(-V))
    return H



class OSELM(object):
    def __init__(self, inputs, outputs, numHiddenNeurons, activationFunction):

        self.activationFunction = activationFunction
        self.inputs = inputs
        self.outputs = outputs
        self.numHiddenNeurons = numHiddenNeurons

        # input to hidden weights
        self.inputWeights = np.random.rand((self.numHiddenNeurons, self.inputs))
        # bias of hidden units
        self.bias = np.random.rand((1, self.numHiddenNeurons)) * 2 - 1
        # hidden to output layer connection
        self.beta = np.random.rand((self.numHiddenNeurons, self.outputs))

        # auxiliary matrix used for sequential learning
        self.M = None


    def calculateHiddenLayerActivation(self, features):
        """
        Calculate activation level of the hidden layer
        @param features feature matrix with dimension (numSamples, numInputs)
        @return: activation level (numSamples, numHiddenNeurons)
        """
        if self.activationFunction is "sig":
            H = sigmoidActFunc(features, self.inputWeights, self.bias)
        else:
            print ("Unknown activation function type")
            raise NotImplementedError
        return H


    def initializePhase(self, features, targets):
        """
        Step 1: Initialization phase
        @param features feature matrix with dimension (numSamples, numInputs)
        @param targets target matrix with dimension (numSamples, numOutputs)
        """
        assert features.shape[0] == targets.shape[0]
        assert features.shape[1] == self.inputs
        assert targets.shape[1] == self.outputs

        # randomly initialize the input->hidden connections
        self.inputWeights = np.random.rand((self.numHiddenNeurons, self.inputs))
        self.inputWeights = self.inputWeights * 2 - 1

        if self.activationFunction is "sig":
            self.bias = np.random.rand((1, self.numHiddenNeurons)) * 2 - 1
        else:
            print ("Unknown activation function type")
            raise NotImplementedError

        H0 = self.calculateHiddenLayerActivation(features)
        self.M = pinv(np.dot(np.transpose(H0), H0))
        self.beta = np.dot(pinv(H0), targets)


    def train(self, features, targets):
        """
        Step 2: Sequential learning phase
        @param features feature matrix with dimension (numSamples, numInputs)
        @param targets target matrix with dimension (numSamples, numOutputs)
        """
        (numSamples, numOutputs) = targets.shape
        assert features.shape[0] == targets.shape[0]

        H = self.calculateHiddenLayerActivation(features)
        Ht = np.transpose(H)
        try:
            self.M -= np.dot(self.M,
                            np.dot(Ht, np.dot(
                pinv(np.eye(numSamples) + np.dot(H, np.dot(self.M, Ht))),
                np.dot(H, self.M))))

            self.beta += np.dot(self.M, np.dot(Ht, targets - np.dot(H, self.beta)))
        except np.linalg.linalg.LinAlgError:
            print("SVD not converge, ignore the current training cycle")

    def predict(self, features):
        """
        Make prediction with feature matrix
        :param features: feature matrix with dimension (numSamples, numInputs)
        :return: predictions with dimension (numSamples, numOutputs)
        """
        H = self.calculateHiddenLayerActivation(features)
        prediction = np.dot(H, self.beta)
        return prediction


def test():
    '''
    dummy
    '''
    # load data for tests

    nDimInput = 100
    nDimOutput = 1
    numNeurons = 25
    lamb=0.0001
    outputWeightFF = 0.92

    net = OSELM(inputs=nDimInput,
                outputs=nDimOutput,
                numHiddenNeurons=numNeurons,
                forgettingFactor=outputWeightFF)
    net.initializePhase(lamb=lamb)


    predictions= []
    target= []

    for i in range(numLags, len(df)-predictionStep-1):
        root = Path().absolute().parent.parent
        dataset_path = root.joinpath('res', 'all_raw.csv')

        df = pd.read_csv(path)

        net.train(X[[i], :], T[[i], :])
        Y = net.predict(X[[i+1], :])

        predictions.append(Y[0][0])
        target.append(T[i][0])
        # print "{:5}th timeStep -  target: {:8.4f}   |    prediction: {:8.4f} ".format(i, target[-1], predictions[-1])

if __name__ == '__main__':
    test()
