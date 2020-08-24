import numpy as np
import importlib
import subprocess
import random as rnd

def same_class(c1, c2):
    return c1.__name__ == c2.__name__

def get_subject_class(subject_class_string):
    data_type = subject_class_string.split("Subject")[1].lower()
    s = 'braphy.workflows.{}.subject_{}'.format(data_type, data_type)
    return getattr(importlib.import_module(s), subject_class_string)

def get_analysis_class(analysis_class_string):
    data_type = analysis_class_string.split("Analysis")[1].lower()
    s = 'braphy.workflows.{}.analysis_{}'.format(data_type, data_type)
    return getattr(importlib.import_module(s), analysis_class_string)

def analysis_subject_match(analysis, subject):
    if isinstance(analysis, type):
        analysis = analysis.__name__
    if isinstance(subject, type):
        subject = subject.__name__
    analysis_data_type = analysis.split('Analysis')[1].lower()
    subject_data_type = subject.split('Subject')[1].lower()
    return analysis_data_type == subject_data_type

def small_world_graph(N, K = 4, beta = 0.1):
    ''' Watts-Strogatz small world algorithm 
     Returns an undirected graph with N nodes and NK/2 edges, K is the degree 
     This should be fulfiled: 0<=beta<=1, N>>K>>ln N>>1
     beta=1 gives a random graph '''
    #random_sm_graph = np.zeros([N,N])
    ''' Regular ring lattice:'''
    #for i in range(0,N):
    #    for j in range(0,N):
    #        condition = abs(i-j) % (N-1-(K/2))
    #        if (condition > 0 and condition <= (K/2)):
    #            random_sm_graph[i,j] = 1

    ''' Rewire with probability beta'''
    #for i in range(0,N):
    #    for j in range(0,N):
    #        if i < j and j <= (i+(K/2)):
    #            if rnd.uniform(0,1) < beta:
    #                k = int(rnd.uniform(0, N))
    #                while k==i or random_sm_graph[i,k] == 1:
    #                    k = int(rnd.uniform(0, N))
    #                    random_sm_graph[i,k] = 1
    #                    random_sm_graph[i,j] = 0
    #                    '''random_sm_graph[k,i] = 1
    #                       random_sm_graph[j,i] = 0'''

    temp = np.arange(1,N+1)
    temp = temp[:, np.newaxis]
    s = np.repeat(temp, K, axis = 1)

    temp2 = np.arange(1,K+1)
    temp2 = temp2[np.newaxis, :]
    t = s + np.repeat(temp2, N, axis = 0)
    s = s - 1 #changing from matlab to python indexing
    t = t - 1 #changing from matlab to python indexing
    t = np.remainder(t,N) #works only according to python indexing e.g. starts at 0

    #source = 0
    for source in range(0,N):
        #beta = 0.5
        switch_edge = np.random.uniform(0, 1, K) < beta
        new_targets = np.random.uniform(0, 1, N)
        new_targets[source] = 0
        new_targets[s[t==source]] = 0
        new_targets[t[source, np.invert(switch_edge)]] = 0 

        ind = new_targets.argsort()[::-1] # sort in descending order
        
        t[source, switch_edge] = ind[0:(np.count_nonzero(switch_edge))] 
        #compare up to this point with matlab by choosing same random vectors, but should be ok

    # NOTE: not done yet
    #h = corresp Matlab's graph function of s,t
    #random_sm_graph = corresp Matlab's adjacency function of h

    random_sm_graph = np.zeros([N,N]) # for now

    return random_sm_graph
