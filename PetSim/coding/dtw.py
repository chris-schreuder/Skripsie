from matplotlib.patches import ConnectionPatch
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance as dist


def dtw(dist_mat):
# Credit to Herman Kamper for his dtw algorithm example

    N, M = dist_mat.shape

    cost_mat = np.zeros((N + 1, M + 1))
    for i in range(1, N + 1):
        cost_mat[i, 0] = np.inf
    for i in range(1, M + 1):
        cost_mat[0, i] = np.inf

    traceback_mat = np.zeros((N, M))
    for i in range(N):
        for j in range(M):
            penalty = [
                cost_mat[i, j],  
                cost_mat[i, j + 1],  
                cost_mat[i + 1, j]]  
            i_penalty = np.argmin(penalty)
            cost_mat[i + 1, j + 1] = dist_mat[i, j] + penalty[i_penalty]
            traceback_mat[i, j] = i_penalty

    i = N - 1
    j = M - 1
    path = [(i, j)]
    while i > 0 or j > 0:
        tb_type = traceback_mat[i, j]
        if tb_type == 0:
            i = i - 1
            j = j - 1
        elif tb_type == 1:
            i = i - 1
        elif tb_type == 2:
            j = j - 1
        path.append((i, j))

    cost_mat = cost_mat[1:, 1:]
    return path[::-1], cost_mat


def splitSearch(q, search, step_size):
    q_length = q
    search_length = search.shape[0]
    step_num = 0
    searches = []
    while (step_num*step_size+q_length < search_length):
        searches.append(search[step_num*step_size:step_num*step_size+q_length])
        step_num+=1
    if step_num == 0:
        searches.append(search[step_num*step_size:step_num*step_size+q_length])
    return searches

def getCosts(q, searches):
    costs=[]
    for i in searches:
        path, cost_mat, cost_mat_normalized = getCost(q, i)
        costs.append(cost_mat_normalized[-1, -1].tolist())
    return costs


def getCost(x_seq, y_seq):
    M = y_seq.shape[0]
    N = x_seq.shape[0]

    dist_mat = dist.cdist(x_seq, y_seq, "cosine")
    path, cost_mat = dtw(dist_mat)
    cost_mat_normalized = cost_mat / (M + N)

    return path, cost_mat, cost_mat_normalized
