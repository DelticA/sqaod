import numpy as np
import utils

# dense graph

def dense_graph_calculate_hJc(W) :
    if (not utils.is_symmetric(W)) :
        raise Exception('W is not symmetric.')

    N = W.shape[0]
    h = np.ndarray((N), dtype=np.float64)
    W4 = np.ndarray((N, N), dtype=np.float64)
    W4 = 0.25 * W

    for i in range(N) :
        h[i] = 0.5 * np.sum(W[i])
    c = np.sum(W4) + np.sum(W4.diagonal())

    J = W4
    for i in range(0, N) :
        J[i][i] = 0

    return h, J, c


def dense_graph_calculate_E(W, x) :
    if len(x.shape) != 1 :
        raise Exception('Wrong dimention of x')
    return np.dot(x, np.matmul(W, x.T))

def dense_graph_batch_calculate_E(W, x) :
    y = x.reshape(x.shape[0], -1)
    return np.sum(y * np.matmul(W, x.T).T, 1)

def dense_graph_calculate_E_from_qbits(h, J, c, q) :
    if len(q.shape) != 1 :
        raise Exception('Wrong dimention of q')
    return c + np.dot(h, q) + np.dot(q, np.matmul(J, q.T))

def dense_graph_batch_calculate_E_from_qbits(h, J, c, q) :
    return c + np.matmul(h, q.T) + np.sum(q.T * np.matmul(J, q.T), 0)



# rbm

def rbm_calculate_hJc(b0, b1, W) :
    N0 = W.shape[1]
    N1 = W.shape[0]
    
    c = 0.25 * np.sum(W) + 0.5 * (np.sum(b0) + np.sum(b1))
    J = 0.25 * W
    h0 = [(1. / 4.) * np.sum(W[:, i]) + 0.5 * b0[i] for i in range(0, N0)]
    h1 = [(1. / 4.) * np.sum(W[j]) + 0.5 * b1[j] for j in range(0, N1)]
    hlist = [h0, h1]

    return h0, h1, J, c

def rbm_calculate_E(b0, b1, W, x0, x1) :
    # FIXME: not tested
    return - np.dot(b0, x0) - np.dot(b1, x1) - np.dot(x1, np.matmul(W, x0))

def rbm_batch_calculate_E(b0, b1, W, x0, x1) :
    # FIXME: not tested
    nBatch0, nBatch1 = x0.shape[0], x1.shape[0]
    return - np.matmul(b0.T, x0.T).reshape(1, nBatch0) - np.matmul(b1.T, x1.T).reshape(nBatch1, 1) \
        - np.matmul(x1, np.matmul(W, x0.T))

def rbm_calculate_E_from_qbits(h0, h1, J, c, q0, q1) :
    return - np.dot(h0, q0) - np.dot(h1, q1) - np.dot(q1, np.matmul(J, q0)) - c

def rbm_batch_calculate_E_from_qbits(h0, h1, J, c, q0, q1) :
    return - np.matmul(h0, q0.T).T.reshape(1, -1) \
        - np.matmul(h1, q1.T).reshape(-1, 1) - np.dot(q1, np.matmul(J, q0.T)) - c