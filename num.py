from bs4 import BeautifulSoup as bs
from tkinter import *
master = Tk()
var1 = IntVar()
Checkbutton(master, text="male", variable=var1).grid(row=0, sticky=W)
var2 = IntVar()
Checkbutton(master, text="female", variable=var2).grid(row=1, sticky=W)

mainloop()
import requests
import re
import numpy as np
import pandas as pd
import camelot
import matplotlib.pyplot as plt
import os

#fetch sourcecode for exracting the links
class corona:
    def __init__(self):
        self.source = requests.get('https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports').text
        self.soup = bs(self.source, 'lxml')

        self.hits = [x for x in self.soup.find_all('div', class_='sf-content-block content-block')
                       if x.find(text=re.compile("Situation"))]
        self.links = ['https://www.who.int'+i['href'] for i in self.hits[0].findAll('a', href=True)]

        #fetch the pdf files
        self.repFound = [(int)(file[6:-4]) for file in os.listdir('./') if file[:6] == 'report']
        for i in self.links:
            num = re.split('-',i)[4]
            if (int)(num) not in self.repFound and (int)(num) > 29:
                with open('report'+num+'.pdf','wb') as f:
                    f.write(requests.get(i, stream=True).content)

        #self.pdfsAllTabs = [camelot.read_pdf('report'+(str)(i)+'.pdf', pages='1-end') for i in self.repFound]
        #self.pdfsAllTabs = [camelot.read_pdf('report'+(str)(i)+'.pdf', pages='1-end') for i in self.repFound]

        #self.lst = [33,35,38,39]
        #self.ger = []
        #for i,pdf in enumerate(self.pdfsAllTabs):
        #    #print(i+30)
        #    if i+30 in self.lst:
        #        tmp = [[pdf[2].df[1][i],pdf[2].df[2][i]] for i,j in pdf[2].df[0].iteritems() if j == "Germany"]
        #        self.ger.append(tmp.pop())
        #    else:
        #        tmp = [[pdf[1].df[1][i],pdf[1].df[2][i]] for i,j in pdf[1].df[0].iteritems() if j == "Germany"]
        #        self.ger.append(tmp.pop())

        #self.gerClean = [[x[0].split()[0],x[1].split()[0]] for x in self.ger]
        #self.gerInf = [(int)(x[0]) for x in self.gerClean]

        #plt.plot(self.repFound,self.gerInf)
        #plt.grid('b')
        #plt.show()


    def something(self):
        rest = tabs[1].append(tabs[2]) # rest der welt
        totalCases = [[x[0], x[1].split().pop()] for y,x in rest.T.iteritems() if x[1] != ""][:-3]
        newCases = [[x[0], x[1].split()[-1:].pop()[1:-1]] for y,x in rest.T.iteritems() if x[1] != ""][:-3]
        totalCases

    def printBarh(self):
        totalCases.reverse()
        tot = totalCases

        y_pos = np.arange(len(objects))
        objects = [i[0] for i in tot]
        performance = [(int)(i[1]) for i in tot]

        plt.barh(y_pos, performance, align='center', alpha=0.5)
        plt.yticks(y_pos, objects)
        plt.gcf().set_size_inches((8,10))

        plt.show()

    def printBarhTest(self):
        objects = ('Malaysia', 'Australia', 'Singapore', 'Japan', 'Korea')
        y_pos = np.arange(len(objects))
        performance = [24,25,102,239,3736]

        plt.barh(y_pos, performance, align='center', alpha=0.5)
        plt.yticks(y_pos, objects)
        plt.xlabel('Usage')
        plt.title('Programming language usage')

        plt.show()

    def printPie(self):
        plt.pie([i[1] for i in tot], labels=[i[0] for i in tot], autopct='%1.1f%%', shadow=True)
        plt.show()

c = corona()
