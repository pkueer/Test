# -*- coding: utf-8 -*-
"""
Created on Sat May 22 23:04:24 2021
Causet input and output functions.
@author: lchps
"""
import graphviz
import numpy

def causet_info(lM,nameStr):
    plotFile = open(nameStr,"w")
    plotFile.write('digraph "causet" {\n')
    plotFile.write('rankdir=BT; concentrate=true;\n')
    nn = len(lM)
    for i in range(nn):
        slist = numpy.sum(lM[i,:])
        if i == 0:
            #plotFile.write(str(i)+' '+'[shape=plaintext, fontsize=28];\n')
            plotFile.write(str(i)+' '+'[shape=plaintext, fontsize=28, fontcolor=red];\n')
        elif i == nn-1:
            #plotFile.write(str(i)+' '+'[shape=plaintext, fontsize=28];\n')
            plotFile.write(str(i)+' '+'[shape=plaintext, fontsize=28, fontcolor=blue];\n')
        else:
            plotFile.write(str(i)+' '+'[shape=plaintext, fontsize=28];\n')
            #plotFile.write('o'+' '+'[shape=plaintext, fontsize=28];\n')
        if slist>0 :
            linkStr = ''
            for j in range(nn):
                if lM[i,j]==1 :
                    linkStr = linkStr+(str(i)+'->'+str(j)+'; ')
            plotFile.write(linkStr+'\n')
    plotFile.write('}')
    return 0;

def causet_visual(dataF,outF):
    dot = graphviz.Source.from_file(dataF)
    dot.render(outF,view = True)
    return 0;
