# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:58:15 2019

@author: WT
"""

import networkx as nx
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import matplotlib.pyplot as plt
import pickle
import os
from text_GCN import gcn
from sklearn.metrics import confusion_matrix

def load_pickle(filename):
    completeName = os.path.join("./data/",\
                                filename)
    with open(completeName, 'rb') as pkl_file:
        data = pickle.load(pkl_file)
    return data

def save_as_pickle(filename, data):
    completeName = os.path.join("./data/",\
                                filename)
    with open(completeName, 'wb') as output:
        pickle.dump(data, output)
        
if __name__=="__main__":
    base_path = "./data/"
    ### Loads graph data
    G = load_pickle("text_graph.pkl")
    A = nx.to_numpy_matrix(G, weight="weight"); A = A + np.eye(G.number_of_nodes())
    degrees = []
    for d in G.degree(weight=None):
        if d == 0:
            degrees.append(0)
        else:
            degrees.append(d[1]**(-0.5))
    degrees = np.diag(degrees)
    X = np.eye(G.number_of_nodes()) # Features are just identity matrix
    A_hat = degrees@A@degrees
    f = X # (n X n) X (n X n) x (n X n) X (n X n) input of net
    
    ### Loads labels
    test_idxs = load_pickle("test_idxs.pkl")
    selected = load_pickle("selected.pkl")
    labels_selected = load_pickle("labels_selected.pkl")
    labels_not_selected = load_pickle("labels_not_selected.pkl")
    
    ### Loads best model ###
    checkpoint = torch.load(os.path.join(base_path,"model_best.pth.tar"))
    net = gcn(X.shape[1], A_hat)
    net.load_state_dict(checkpoint['state_dict'])