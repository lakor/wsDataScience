
# coding: utf-8

# In[17]:

import numpy as np
import csv


# In[18]:

#read dictionary File into dictionary DataStruct
with open("Data/DataForBar/barFile.csv") as f:
    dictdata = list(csv.reader(f))
    f.close

    dictdata.reverse
headline=dictdata.pop(0)
i=0
for title in headline:
    if title=='Host':
        hostplace=i
    if title =='URL':
        urlplace=i
    if title=='MinDuration':
        durplace=i
    i+=1
dict = {}
for line in dictdata:
    hostname=line[hostplace]
    urlname=line[urlplace]
    dur=float(line[durplace])
    urldict={urlname:dur}
    if hostname not in dict: #update new host
        dict.update({hostname:urldict})
    else:
        allurls=dict[hostname] #the current host url's list
        if urlname not in allurls: #update new url
            dict[hostname].update(urldict)


# In[19]:

#read the file intended to be labeled into DataStructure
def readFileToList(filepath,newpath):
    with open(filepath) as f:
        with open(newpath,'w') as f2:
            writer=csv.writer(f2)
            for row in csv.reader(f):
                writer.writerow(row+["Label"])
            f2.close
        f.close
    with open(newpath,'r') as f2:
        data = list(csv.reader(f2))
        f2.close
    return data


# In[20]:

#function for deciding busy row or not
def isBusy(lineDur,minDur):
    if lineDur>=(2*minDur): #twice as minimum duration
        return True
    else:
        return False


# In[21]:

#save labeled data to file
def labeledDataToFile(filepath,data):
    with open(filepath,'w') as f2:
        for line in data:
            for word in line:
                f2.write('%s,' % word)
            f2.write('\n')
        f2.close()


# In[22]:

def labelTheData (dict,data):
    data.reverse
    headline=data.pop(0)
    i=0
    #find indexes
    for title in headline:
        if title=='Host':
            hostplace=i
        if title =='UrlBase':
            urlplace=i
        if title=='ReqDuration':
            durplace=i
        if title=='Label':
            labelplace=i
        i+=1
    #label the rows
    for line in data:
        lineHost=line[hostplace]
        lineUrl=line[urlplace]
        lineDur=float(line[durplace])
        minDur=(dict[lineHost])[lineUrl]
        if isBusy(lineDur,minDur): #check if busy row
            line[labelplace]=1
        else:
            line[labelplace]=0
    data.insert(0,headline)


# In[23]:

#label all the files in the list
def labelAllFiles (dict,allfiles):
    for filepath in allfiles:
        newpath=filepath
        newpath="Data/labeledData/"+newpath.split("Data/DataToLabel/", 1)[1]
        newpath=newpath.split(".csv", 1)[0]+"_labeled.csv"
        data=readFileToList(filepath,newpath)
        #label the data of the file
        labelTheData (dict,data)
        #save data to file
        labeledDataToFile(newpath,data)


# In[24]:

#label all files in the list
import os
allfiles=list()
dirpath="Data/DataToLabel"
for filename in os.listdir(dirpath): #add all requests files in the diractory
    if "day" in filename:
        allfiles.append("Data/DataToLabel/"+filename)
labelAllFiles (dict,allfiles)


# In[ ]:


