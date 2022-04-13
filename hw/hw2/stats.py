#!/usr/bin/env python
# coding: utf-8

# In[66]:


import sys
import lxml
from lxml import etree
import json

#input file name, output file name 
xmlname = sys.argv[1]
jsonname = sys.argv[2]

# xmlname = 'fsimage564.xml'
# jsonname = 'stats.json'


# In[67]:


#open xml file
f = open(xmlname)
tree = etree.parse(f)

#set min and min default value
minfile = sys.maxsize

maxfile = -sys.maxsize

#count number of file by checking the type elemnet
filecount = len([element for element in tree.xpath("//inode[type='FILE']")])
#count number of directory by checking the type elemnet
directoryCount = len([element for element in tree.xpath("//inode[type='DIRECTORY']")])


# In[68]:


#find the max and min file
for element in tree.xpath("//inode[type='FILE']//blocks//block//numBytes"):
    if(int(element.text) < minfile):
        minfile = int(element.text)
    if( int(element.text) > maxfile ):
        maxfile = int(element.text)
#     print(element.text)


# In[69]:


#size of all directory that has a sub-directory
partentsize = len([element for element in tree.xpath("//INodeDirectorySection//directory//parent")])


# In[70]:


#parent node
part=[]
#child node
c = []

i = 0
for element in tree.xpath("//INodeDirectorySection//directory"):
    for x in element.getchildren():
        if(x.tag == 'parent'):
            part.append(x.text)
            
        
#         print(x.tag, '-', x.text)
        
for elements in tree.xpath("//INodeDirectorySection//directory"):
    for xs in elements.getchildren():
#         print(xs.tag, '-', xs.text)
        if(xs.tag == 'child'):
            c.append(xs.text)


            


# In[72]:


#vv states how many child does a parent have
vv = [0]*partentsize

chi = []
lst = {}
i = -1

ps=0
cs=0
# count number of children for every parent
for element in tree.xpath("//INodeDirectorySection//directory"):
    for x in element.getchildren():
#         print(x.getnext())
        if(x.tag == 'parent'):
           i = i +1
            
            
            
        else:
            vv[i] = vv[i]+1
            cs = cs +1


# In[73]:


lst={}
ch = []
i = 0
b = 0
# put parent and children into a object, that key is a parent node and value is a array of its chidren nodes
for h in vv:
    
    for n in range(h):
        ch.append(c[b])
        lst[part[i]] = ch
       
        b=b+1
    i = i+1
    ch = []    


# In[74]:


#dictree maks a tree of directory. 
#(check every node, every node is key and value is a array of its chidren nodes, 
#if no children then value is a empty array)
dictree = {}
for ea in lst.items():
    dictree[ea[0]] = ea[1]
    for chi in ea[1]:
        if(chi not in part):
            dictree[chi] = []
        
            
#     print(ea)


# In[75]:



#find tree height by dfs
def maxDepth(node,cp):
    
    checkpoint = dictree[node] 
    
#     print('cp: '+ str(checkpoint))
    if checkpoint is None:
        return -1 ;
 
    else :
        cp = cp +1
        for ea in checkpoint:
#             print('ea: '+ea)
            maxDepth(ea,cp)
#             print('ea: '+ea)
            deptharray.append(cp)
#             print(cp)
        
#         if(len(checkpoint))
#         return cp + 1


# In[76]:


#array of every tree branch size
deptharray = []
#find the max size of all branch
if(len(part) !=0):
    maxDepth(part[0],1)
    maxdepth = max(deptharray)
else:
    maxdepth = 0


# In[77]:


#if no file exists, no file size information should be print
if(filecount !=0):
    data = {"number of files": filecount, "number of directories": directoryCount, "maximum depth of directory tree": maxdepth, "file size": {"max": maxfile , "min" :minfile}}
else:
    data = {"number of files": filecount, "number of directories": directoryCount, "maximum depth of directory tree": maxdepth}


# In[78]:


#data


# In[79]:



# Serializing json

json_obj = json.dumps(data, indent = 4)

# Writing to stats.json

with open(jsonname, "w") as outfile:

    outfile.write(json_obj)


# In[ ]:





# In[ ]:





# In[ ]:




