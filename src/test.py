import numpy as np
from read_data import get_data
import sys
sys.path.append("network/")
from NN import NeuralNet

#X, Y = get_data(normalized = False, standardized = False)
X, Y = get_data()
print(np.count_nonzero(Y == 1))

nn = NeuralNet(X, Y.flatten(), nodes = [23, 50, 50, 2], activations = ['tanh', 'tanh', None], cost_func = 'log')
nn.split_data(frac = 0.5, shuffle = True)
nn.TrainNN(epochs = 10000, batchSize = 200, eta0 = 0.01, n_print = 100)