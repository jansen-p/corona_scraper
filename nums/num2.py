from bs4 import BeautifulSoup as bs
import requests
import re
import camelot
import matplotlib.pyplot as plt
import logging
import numpy as np
import pandas as pd

##

logging.getLogger("camelot").setLevel(logging.WARNING)

def ins(x,y):
    i = 0
    while i < len(x):
        if i+1 < len(x) and x[i][0] < y[0] and y[0] < x[i+1][0]:
            x.insert(i+1,y)
        elif i+1 >= len(x) and x[i][0] < y[0]:
            x.insert(i+1,y)
        i = i+1
    return x

def removeDuplicates(x):
    buf = numsLinks[0]
    i = 1

    while i<len(x):
        if x[i][0] == buf[0]:
            x.remove(x[i])
            i = i-1
        elif x[i][0] > buf[0]:
            x.remove(x[i])
            i = i-1
        else:
            buf = x[i]
        i = i+1
    return x

##

path = '/run/Parts/Exch/Sync/swap/pyt/corona/nums/'

#fetch sourcecode for exracting the links
print("Sending request...")
source = requests.get('https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports').text
soup = bs(source, 'lxml')

hits = [x for x in soup.find_all('div', class_='sf-content-block content-block') if x.find(text=re.compile("Situation"))]
links = ['https://www.who.int'+i['href'] for i in hits[0].findAll('a', href=True) if len(i['href']) > 40]
numsLinks = [[int(re.search(r"-[0-9]*-",link).group()[1:-1]),link] for link in links]

##


#clean:
numsLinks = removeDuplicates(numsLinks)

print("Done.\n")


with open(path+'numbers.txt', 'r') as f:
    #numbers = [[int(i[:-1]) for i in f]
    inp = [[int(i[1:-2].split(',')[0]),
            int(i[1:-2].split(',')[1]),
            int(i[1:-2].split(',')[2]),
            int(i[1:-2].split(',')[3])]     for i in f]

#check which reports haven't been processed yet, ignore first 16 reports
todos = [i for i in numsLinks[:-16] if i[0] not in [i[0] for i in inp]]

print("Reports to process: ",todos)

##

#process, if there is something to process
if todos: 
    #fetch the pdf files
    print("New report found, processing...")

    for i in todos:
        num = i[0]
        link = i[1]
        with open(path+'report.pdf','wb') as f:
             f.write(requests.get(link, stream=True).content)
        
        #extract all tabulars from one
        pdfsAllTabs = camelot.read_pdf(path+'report.pdf', pages='1-end')

        total = []
        totalCanada = []
        
        for i,pdf in enumerate(pdfsAllTabs):
            #print(i+30)
            for j in pdf.df[0].iteritems():
                if j[1] == 'Germany':
                    total = pdf.df[1][j[0]]
                    dead = pdf.df[3][j[0]]
                elif j[1] == 'Canada':
                    totalCanada = pdf.df[1][j[0]]
                if total and totalCanada:
                    break

            if total and totalCanada:
                break

        inp = ins(inp,[int(num),int(total),int(totalCanada),int(dead)])

print("Done.\n")

##


step = int(np.divide(inp[-1][1],40))

print("Finished, plots:") 
#days = [i[0] for i in inp]
days = list(range(-len(inp)+1,1,1))
startDay = 20

plt.plot(days[startDay:],[i[1] for i in inp][startDay:],'blue',label="Total cases Germany")
plt.plot(days[startDay:],[i[3] for i in inp][startDay:],'red',label="Total deaths Germany")
plt.plot(days[startDay:],[i[2] for i in inp][startDay:],'green',label="Total cases Canada")

plt.title("Current report number: "+str(inp[-1][0]))
plt.grid('b')
#plt.yscale('log')
plt.legend()
plt.xticks(days[startDay:])
plt.yticks(list(range(0,inp[-1][1],step)))
plt.gcf().set_size_inches((20,14))
plt.savefig(path+'all.png')
#plt.show()

##

plt.plot(days,[i[1] for i in inp],'blue',label="Total cases")
plt.plot(days,[i[2] for i in inp],'green',label="Total cases Canada")
plt.grid('b')
plt.xticks(days)
plt.yscale('log')
plt.legend()
plt.gcf().set_size_inches((20,14))
plt.savefig(path+'log.png')


##

with open(path+'numbers.txt', 'w') as f:
    for item in inp:
        f.write("%s\n" % item)

##

table = pd.read_csv("/run/Parts/Exch/Sync/swap/pyt/corona/nums/numbers.csv")
table.iloc[15:]
table.iloc[-1][0]

table.iloc[startDay:].plot(kind='bar',stacked=True,yticks=list(range(0,table.max().sum(),2*step)),label="Tot cases",grid=True,figsize=(14,8))

