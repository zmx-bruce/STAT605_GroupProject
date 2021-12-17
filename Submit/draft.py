#!/usr/bin/env python
# coding: utf-8

# In[13]:


import networkx as nx
import json
import numpy as np
import random 
import pandas as pd
import sys
import itertools
import pickle
import sys


# In[3]:



with open("reddit_edges.json", 'rb') as f:
    data= json.load(f)


# In[14]:

param=int(sys.argv[1])
#param=3
value=np.array_split(range(len(data)), 1000)[param]
G=[]
for x in value:
    g=nx.from_edgelist(data[str(x)])
    G.append(g)

# In[8]:

motifs = {
    'M3_1': nx.Graph([(1,2),(2,3)]),
    'M3_2': nx.Graph([(1,2),(1,3),(2,3)]),
    'M4_1': nx.Graph([(1,2),(1,3),(1,4)]),
    'M4_2': nx.Graph([(1,2),(1,3),(1,4),(2,3)]),
    'M4_3': nx.Graph([(1,2),(2,3),(3,4)]),
    'M4_4': nx.Graph([(1,2),(2,3),(3,4),(4,1)]),
    'M4_5': nx.Graph([(1,2),(2,3),(3,4),(1,3),(2,4)]),
    'M4_6': nx.Graph([(1,2),(2,3),(3,4),(1,3),(2,4),[4,1]])}


# In[10]:


V=[]
for g in G:
    m3_1=0;m3_2=0
    for sub_nodes in itertools.combinations(g.nodes(),3):# choose 3 from n, where n is number of nodes of network
        subg = g.subgraph(sub_nodes)
        if nx.is_connected(subg):
            if nx.is_isomorphic(subg, motifs['M3_1']):
                m3_1+=1
            if nx.is_isomorphic(subg, motifs['M3_2']):
                m3_2+=1
    s_3=m3_1+m3_2

    m4_1=0;m4_2=0;m4_3=0;m4_4=0;m4_5=0;m4_6=0           
    for sub_nodes in itertools.combinations(g.nodes(),4):
        subg = g.subgraph(sub_nodes)
        if nx.is_connected(subg):
            if nx.is_isomorphic(subg, motifs['M4_1']):
                m4_1+=1
            if nx.is_isomorphic(subg, motifs['M4_2']):
                m4_2+=1
            if nx.is_isomorphic(subg, motifs['M4_3']):
                m4_3+=1
            if nx.is_isomorphic(subg, motifs['M4_4']):
                m4_4+=1
            if nx.is_isomorphic(subg, motifs['M4_5']):
                m4_5+=1
            if nx.is_isomorphic(subg, motifs['M4_6']):
                m4_6+=1
    s_4=m4_1+m4_2+m4_3+m4_4+m4_5+m4_6
    if s_3!=0 and s_4!=0:
        v=[m3_1/s_3,m3_2/s_3,m4_1/s_4,m4_2/s_4,m4_3/s_4,m4_4/s_4,m4_5/s_4,m4_6/s_4]
    if s_3==0 and s_4!=0:
        v=[0,0,m4_1/s_4,m4_2/s_4,m4_3/s_4,m4_4/s_4,m4_5/s_4,m4_6/s_4]
    if s_3!=0 and s_4==0:
        v=[m3_1/s_3,m3_2/s_3,0,0,0,0,0,0]
    if s_3==0 and s_4==0:
        v=[0,0,0,0,0,0,0,0]
    V.append(v)
with open(f"{param}.pkl", 'wb') as f:
    pickle.dump(V,f)


# In[ ]:




