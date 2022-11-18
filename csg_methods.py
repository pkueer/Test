# -*- coding: utf-8 -*-
"""
Created on Sat May 21 05:21:17 2022

@author: lchps
"""

"""
labeling starts with 0
"""

import math
import networkx as nx
import numpy as np
import array
#import causet_io as io
import causet_basic as bs
import random
import csv
from itertools import combinations as itercomb
import matplotlib.pyplot as plt

def random_desc_normalized_array(n):
    arr = np.random.rand(n)
    arr.sort()
    arr /= arr[n-1]
    return arr[::-1]


def one_step_general(g,tVal):
    nmax = nx.number_of_nodes(g)
    gs = set(g.nodes)
    g.add_node(nmax)
    #print(nmax)
    #print(gs)
    size_list = [i for i in range(nmax+1)]
    #print("size_list",size_list)
    prob_list = []
    for i in range(0,nmax+1):
        prob_list.append(tVal[i]*math.comb(nmax,i))
    #print("probs:",prob_list)
    size = random.choices(size_list,weights=prob_list,k=1)
    #print("size",size[0])    
    if size[0] == 0:
        return g
    ancestor_list = random.sample([i for i in range(nmax)],k=size[0])
    #print("node_list",node_list)
    #print("ancestor_list",ancestor_list)
    for nn in ancestor_list:
        g.add_edge(nn,nmax)
        #print("new element edges with:",nn)
    return g

def one_step_original(g,tVal):
    nmax = nx.number_of_nodes(g)
    gs = set(g.nodes)
    g.add_node(nmax)
    #print(nmax)
    #print(gs)
    size_list = [i+1 for i in range(nmax)]
    #print("size_list",size_list)
    prob_list = []
    for i in range(1,nmax+1):
        prob_list.append(tVal[i]*math.comb(nmax,i))
    #print("probs:",prob_list)
    size = random.choices(size_list,weights=prob_list,k=1)
    #print("size",size[0])    
    ancestor_list = random.sample([i for i in range(nmax)],k=size[0])
    #print("node_list",node_list)
    #print("ancestor_list",ancestor_list)
    for nn in ancestor_list:
        g.add_edge(nn,nmax)
        #print("new element edges with:",nn)
    return g

def one_step_transitive(g,t):
    nmax = nx.number_of_nodes(g)
    g.add_node(nmax)
    p = t/(t+1.000)
    for i in range(nmax):
        if np.random.choice(2, p=[1-p,p])==1:
            g.add_edge(i,nmax)
    return g

def one_step_transitive_prob(g,p):
    nmax = nx.number_of_nodes(g)
    g.add_node(nmax)
    for i in range(nmax):
        if np.random.choice(2, p=[1-p,p])==1:
            g.add_edge(i,nmax)
    return g

# def other_originary_one_step_transitive_prob(g,p):
#     nmax = nx.number_of_nodes(g)
#     g.add_node(nmax)
#     no_past = False
#     if nmax == 1:
#         g.add_edge(0,1)
#         return g
#     while !no_past:
#         for i in range(nmax):
#             if np.random.choice(2, p=[1-p,p])==1:
#                 g.add_edge(i,nmax)
#                 no_past = True
#     return g


def classical_sequential_growth(n,model, t=0.1, t_c = 1.0, original = False):
    g = nx.DiGraph()
    g.add_node(0)
    tVal = [1]
    if n==1:
        return g
    if not original:
        for i in range(n-1):
            if model == "dust":
                tVal.append(0)
            if model == "factorial":
                tVal.append(tVal[i]/(i+1))
            if model == "transitive":
                tVal.append(tVal[i]*t)
            if model == "power_factorial":
                tVal.append(tVal[i]*t/(i+1)*t_c)
            one_step_general(g,tVal)
    else:
        for i in range(n-1):
            tVal.append(tVal[i]*t)
            one_step_original(g,tVal)
    return g



def transitive_percolation(n,t):
    g = nx.DiGraph()
    g.add_node(0)
    for i in range(n-1):
        one_step_transitive(g,t)
    return g

def chain_distribution(g,kmax):
    full_g = nx.transitive_closure(g)
    nums = [full_g.number_of_edges()]
    if kmax == 1:
        return nums
    rm = nx.to_numpy_matrix(full_g)
    m = rm
    for k in range(kmax -1):
        m = np.matmul(rm,m)
        nums.append(np.matrix.sum(m))
    return nums

def Minkovski_future_interval(height = 1.0 ,N=100,dim=2):
    coords = np.zeros((N,dim))
    success = 1
    base_g = nx.DiGraph()
    base_g.add_node(0)
    coord = np.zeros((1,dim))
    while success < N:
        coord[0,0] = height * np.random.rand(1,1)
        coord[0,1:] = (2.0 * height * np.random.rand(1,dim-1) - height)
        if np.linalg.norm(coord[0,1:]) > coord[0,0]:
            continue
        coords[success,:] = coord[0,:]
        base_g.add_node(success)
        base_g.add_edge(0,success)
        success += 1
        # print(coord[0,0],coord[0,1])
    srt_coords = coords[np.argsort(coords[:, 0])]
    plt.scatter(srt_coords[:,1], srt_coords[:,0])
    for i in range(1,N-1):
        for j in range(i+1,N):
            t_gap = srt_coords[j,0] - srt_coords[i,0]
            s_gap = np.linalg.norm(srt_coords[j,1:] - srt_coords[i,1:])
            if t_gap > s_gap:
                base_g.add_edge(i,j)
    return base_g

def Minkovski_future_interval(height = 1.0 ,N=100,dim=2):
    coords = np.zeros((N,dim))
    success = 1
    base_g = nx.DiGraph()
    base_g.add_node(0)
    coord = np.zeros((1,dim))
    while success < N:
        coord[0,0] = height * np.random.rand(1,1)
        coord[0,1:] = (2.0 * height * np.random.rand(1,dim-1) - height)
        if np.linalg.norm(coord[0,1:]) > coord[0,0]:
            continue
        coords[success,:] = coord[0,:]
        base_g.add_node(success)
        base_g.add_edge(0,success)
        success += 1
        # print(coord[0,0],coord[0,1])
    srt_coords = coords[np.argsort(coords[:, 0])]
    plt.scatter(srt_coords[:,1], srt_coords[:,0])
    for i in range(1,N-1):
        for j in range(i+1,N):
            t_gap = srt_coords[j,0] - srt_coords[i,0]
            s_gap = np.linalg.norm(srt_coords[j,1:] - srt_coords[i,1:])
            if t_gap > s_gap:
                base_g.add_edge(i,j)
    return base_g

def Minkovski_interval(height = 1.0 ,N=100,dim=2):
    coords = np.zeros((N,dim))
    success = 1
    base_g = nx.DiGraph()
    base_g.add_node(0)
    base_g.add_node(N-1)
    base_g.add_edge(0,N-1)
    coord = np.zeros((1,dim))
    while success < N - 2:
        coord[0,:] = height * np.random.rand(1,dim)
        coord[0,1:] = coord[0,1:] - 0.5 * height * np.ones((1,dim-1))
        if coord[0,0] < 0.5 * height:
            width = coord[0,0]
        else:
            width = height - coord[0,0]
        if np.linalg.norm(coord[0,1:]) > width:
            continue
        coords[success,:] = coord[0,:]
        base_g.add_node(success)
        base_g.add_edge(0,success)
        base_g.add_edge(success,N-1)
        success += 1
        # print(coord[0,0],coord[0,1])
    srt_coords = coords[np.argsort(coords[:, 0])]
    #plt.scatter(srt_coords[:,1], srt_coords[:,0])
    for i in range(1,N-1):
        for j in range(i+1,N):
            t_gap = srt_coords[j,0] - srt_coords[i,0]
            s_gap = np.linalg.norm(srt_coords[j,1:] - srt_coords[i,1:])
            if t_gap > s_gap:
                base_g.add_edge(i,j)
    return base_g