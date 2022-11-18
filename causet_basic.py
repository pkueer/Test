# -*- coding: utf-8 -*-
"""
Created on Sun May 23 08:40:25 2021

@author: lchpsp
"""
import numpy
import networkx as nx

def relation_to_link(rM):
    rM2 = numpy.matmul(rM,rM)
    lM = rM
    nn = len(rM)
    for i in range(nn):
        for j in range(nn-i-1):
            k = j + 1;
            if rM[i,k]==1 and rM2[i,k] > 0:
                lM[i,k] = 0
    return lM

def num_of_k_chains(rM,k):
    m = numpy.linalg.matrix_power(rM,k)
    return numpy.matrix.sum(m)

def num_of_k_paths(lM,k):
    m = numpy.linalg.matrix_power(lM,k)
    return numpy.matrix.sum(m)

def num_of_k_intervals(g,k):
    nn = g.number_of_nodes()
    if nn < 3:
        return -1
    if k == 0:
        l = nx.to_numpy_matrix(nx.transitive_reduction(g))
        return numpy.sum(l)
    nK = 0
    r = nx.to_numpy_matrix(nx.transitive_closure(g))
    r2 = numpy.linalg.matrix_power(r,2)
    l = nx.to_numpy_matrix(nx.transitive_reduction(g))
    l2 = numpy.linalg.matrix_power(l,2)
    # print(r2)
    # print(l2)
    for i in range (nn):
        for j in range(i+1,nn):
            if l2[i,j] == k:
                nK += 1
    return nK

# def fast_BD_intervals(g,k):
#     nn = g.number_of_nodes()
#     nks = [0] * (k+1)
#     if nn < 3:
#         return -1]
#     if k == 0:
#         l = nx.to_numpy_matrix(nx.transitive_reduction(g))
#         nks[0] = numpy.sum(l)
#         return nks
#     nK = 0
#     r = nx.to_numpy_matrix(nx.transitive_closure(g))
#     r2 = numpy.linalg.matrix_power(r,2)
#     l = nx.to_numpy_matrix(nx.transitive_reduction(g))
#     l2 = numpy.linalg.matrix_power(l,2)
#     # print(r2)
#     # print(l2)
#     for i in range (nn):
#         for j in range(i+1,nn):
#             if l2[i,j] == k:
#                 nK += 1
#     return nK