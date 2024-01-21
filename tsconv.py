import torch
import numpy as np
import pandas as pd
from datetime import time


#suppose X, Y are one dimension tensor
def ts_corr(X, Y, d, s): # d: days, s: stride
    corr = []
    for i in range(0, X.size(1)//s):
        x = torch.cat((X[s*i:s*i+d], Y[s*i:s*i+d]), 1)
        corr_matrix = torch.corrcoef(x)
        corr.append(corr_matrix[0,1])    
    return corr


def ts_cov(X, Y, d, s): # s: stride
    cov = []
    for i in range(0, X.size(1)//s):
        x = torch.cat((X[s*i:s*i+d], Y[s*i:s*i+d]), 1)
        cov_matrix = torch.cov(x)
        cov.append(cov_matrix[0,1])
    return cov


def ts_stddev(X, d, s):
    stddev = []
    for i in range(0, X.size(0)//s):
        val = torch.std(X[s*i:s*i+d])
        stddev.append(val)
    return stddev


def ts_zscore(X, d, s):
    zscore = []
    for i in range(0, X.size(0)//s):
        val = torch.std(X[s*i:s*i+d])/torch.mean(X[s*i : s*i+d])
        zscore.append(val)
    return zscore


def ts_return(X, d, s):
    ret = []
    for i in range(0, X.size(0)//s):
        val = (X[s*i+d]-X[s*i])/X[s*i] - 1
        ret.append(val)
    return ret


def ts_decay(X, d, s):
    decay = []
    for i in range(0, X.size(0)//s):
        val = torch.mean(X[s*i:s*i+d] * torch.arange(d, 0, -1) * 2/d/(d+1))
        decay.append(val)
    return decay


def ts_min(X, d, s):
    minval = []
    for i in range(0, X.size(0)//s):
        val = torch.min(X[s*i:s*i+d])
        minval.append(val)
    return minval


def ts_max(X, d, s):
    maxval = []
    for i in range(0, X.size(0)//s):
        val = torch.max(X[s*i:s*i+d])
        maxval.append(val)
    return maxval


def ts_mean(X, d, s):
    meanval = []
    for i in range(0, X.size(0)//s):
        val = torch.mean(X[s*i:s*i+d])
        meanval.append(val)
    return meanval

