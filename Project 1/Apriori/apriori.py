# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 11:59:07 2016

@author: Hizkia
Description: Python Implementation of the Apriori Algorithm
This code implements an apriori algorithm to find interesting 
patterns in a census data set retrieved from the following link:
http://archive.ics.uci.edu/ml/datasets/Adult

"""
# LIBRARIES
from itertools import combinations
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import os
import urllib2

##################################################################
# SUPPORTING FUNCTIONS
##################################################################

def age_bins(age):
    '''Return the category of input age. 
       Return missing value as it is
    '''
    try:
        int(age)
    except ValueError:
        return age
    else:
        if int(age) < 45:
            return 'young-adult'
        elif 45 <= int(age) <= 65:
            return 'middle-age'
        elif int(age) > 65:
            return 'senior'
    
def caploss_bins(cap_loss):
    '''Return the category of capital loss. 
       Return missing value as it is
    '''
    try:
        int(cap_loss)
    except ValueError:
        return cap_loss
    else:
        if int(cap_loss) == 0:
            return '$0'
        elif 1 <= int(cap_loss) <= 1700:
            return '$1-$1700'
        elif 1701 <= int(cap_loss) > 2000:
            return '$1701-$2000'
        elif int(cap_loss) > 2000:
            return '>2000'

def capgain_bins(cap_gain):
    '''Return the category of capital gain. 
       Return missing value as it is
    '''
    try:
        int(cap_gain)
    except ValueError:
        return cap_gain
    else:
        if int(cap_gain) == 0:
            return '$0'
        elif 1 <= int(cap_gain) <= 4000:
            return '$1-$4000'
        elif 4001 <= int(cap_gain) > 7700:
            return '$4001-$7700'
        elif int(cap_gain) > 7700:
            return '>7700'

def workhour_bins(workhour):
    '''Return the category of workhour. 
       Return missing value as it is
    '''
    try:
        int(workhour)
    except ValueError:
        return workhour
    else:
        if int(workhour) == 40:
            return 'full-time'
        elif int(workhour) < 40:
            return 'part-time'
        elif int(workhour) > 40:
            return 'overtime'

def has_infrequent_subset(a_set,itemsets):
    '''Checking if there is a subset of an itemset a_set that is 
    infrequent
    
    param: 
    a_set: the set being examined
    itemsets: list of frequent (k-1)-itemsets
    '''
    val = False
    for combination in combinations(a_set,len(a_set)-1):
        if set(combination) not in itemsets:
                val = True
    return val
        
    
def apriori_gen(itemsets):
    ''' Generate frequent (k+1)-itemsets
    
    param:
    itemsets: frequent k-itemsets
    '''
    sets = itemsets.keys()
    new_itemsets = []
    k = len(sets[0])  # length of the itemsets
    # making sure all the itemsets have the same length
    assert(all(len(itemset) == k for itemset in sets))
    for idx, itemset in enumerate(sets):
        k_minus_one = sorted(itemset)[:k-1]
        for i in range(idx+1,len(sets)):
            if k_minus_one == sorted(sets[i])[:k-1]:
                union = set(sets[idx]).union(set(sets[i]))
                #prune itemsets
                if not(has_infrequent_subset(union,sets)):
                    new_itemsets.append(union)
                
    return new_itemsets


def prune_itemsets(itemsets,min_sup,transactions):
    ''' Remove itemsets that do not meet the min_sup
    
    param:
    itemsets: itemset being examined
    transaction: list of all transactions
    min_sup: minimum support value of a frequent itemset 
    '''
    for itemset, f in itemsets.items():
        if float(f)/len(transactions) < min_sup:
            del itemsets[itemset] 
    
def generate_itemsets(itemsets_list, min_sup, transactions):
    ''' Generate all frequent itemsets with length more than 1
    in the apriori algoritm 
    
    param:
    itemsets_list: a list of 1-itemsets, 2-itemsets, ... , k-itemsets
    min_sup: minimum support value of a frequent itemset
    transactions: transaction data base
    '''
    L = itemsets_list[0]
    k = len(itemsets_list)
    while(len(L) != 0): 
        try:
            next_itemsets = apriori_gen(L)
        except IndexError:
            return
        
        temp = defaultdict(int)
        for itemset in next_itemsets:
            for transaction in transactions:
                if itemset.issubset(transaction):
                    temp[frozenset(itemset)] += 1
                
        prune_itemsets(temp,min_sup,transactions)
        
        itemsets_list.append(temp)
        k += 1
        L = itemsets_list[k-1]
        
def calc_conf(x,transactions,support):
    '''Calculate support of an itemset x in the transaction
    '''
    i = 0
    for transaction in transactions:
        if x.issubset(set(transaction)):
            i += 1;
    return support/(float(i)/len(transactions))

def generate_rules(itemset,min_conf,support,transactions):
    '''Generates rules from a frequent itemset. 
    
    param:
    support = support value of the itemset. 
    itemset = a frequent itemset 
    min_conf = minimum confidence
    transactions = transaction data set
    '''
    rules = defaultdict(set)
    k = {}
    n = len(itemset)
    while n > 0:
        for combination in combinations(itemset,n-1):
            if (len(combination)!=0):
                if calc_conf(set(combination),transactions,support) >= min_conf:
                    k = itemset - set(combination)
                    rules[frozenset(combination)] = (frozenset(k))
        n += -1;       
    return rules
    
generate_rules(set(itemsets_list[4].keys()[0]),min_conf,float(10283)/len(transactions),transactions)
 
##################################################################
# DATA PROCESSING
##################################################################
# Load data into the program and discretize quantitative         #
# attributes                                                     #
##################################################################

data_url = "https://raw.githubusercontent.com/hizkiafebianto/CSC240/master/Project%201/Apriori/adult.data"
raw_data = []
f = urllib2.urlopen(data_url) # create connection with the URL
for line in f.readlines():
    temp = []    
    for item in line.split(','): # split each line by comma
        temp.append(item.strip()) # strip whitespace from each item
    raw_data.append(temp)
del raw_data[len(raw_data)-1]

# Discretize continuous attributes: age, capital-gain, capital-loss,
# and hours-per-week. Remove insignificant attributes: fnlwgt and 
# education-num. 

#see value distribution
age = []
cap_gain =[]
cap_loss = []
hours_perweek = []
for row in range(0,len(raw_data)-1):
    age.append(int(raw_data[row][0]))
    cap_gain.append(int(raw_data[row][10]))
    cap_loss.append(int(raw_data[row][11]))
    hours_perweek.append(int(raw_data[row][12]))
    
# From the following histogram, we determine the classification of age
plt.hist(age,10)

# From the following histogram, we know the distribution of cap_loss. 
# Cap_gain = 0 is ignored here since it is too frequent
plt.hist(cap_loss,bins=10,range=(1,max(cap_loss)))

# From the following histogram, we might think that cap_gain = 99999 is 
# a default value so we will eliminate records that has cap_gain = 99999
plt.hist(cap_gain,bins=10,range=(1,max(cap_gain)))
cap_gain.count(99999) # There are 159 records 

# Remove records with cap_gain = 99999 and calculate missing values. 
data = []
missing_val = 0
for item in raw_data:
    if int(item[10]) != 99999:
        data.append(item[:])
    if '?' in item:
        missing_val += 1;
 
# Categorization of capital loss using similar frequency bins
# $0
# $1-$1700
# $1701-$2000
# >$2000
temp = []
for row in range(0,len(data)-1):
    temp.append(int(data[row][11]))
np.array_split(np.sort(np.array(filter(lambda a:a != 0,temp))),3)

# Categorization of capital gain using similar frequency bins
# $0
# $1-$4000
# $4001-$7700
# >7700
temp = []
for row in range(0,len(data)-1):
    temp.append(int(data[row][10]))
np.array_split(np.sort(np.array(filter(lambda a:a != 0,temp))),3)

# Categories for age
# senior: > 65
# middle-age: 45 - 65
# young-adult: < 45

data1 = []
for row in data:
    temp = row[:]
    # Discretize age
    temp[0] = age_bins(row[0])
    # Discretize capital gain
    temp[10] = capgain_bins(row[10])
    # Discretize capital loss
    temp[11] = caploss_bins(row[11])
    # Discretize workhour
    temp[12] = workhour_bins(row[12])
    # Delete education_num
    del temp[4]
    # Delete fnlwgt
    del temp[2]
    data1.append(temp)

keys = ['age','workclass','education','marital','occupation',\
'relationsip','race','sex','gain','loss','hours','country','salary']

##################################################################
# APRIORI IMPLEMENTATION
##################################################################

# Prompts user for minimum support and minimum confidence
min_sup = input("Input minimum support = ")
min_conf = input("Input minimum confidence = ")


# Each row in the data set will be treated as a transaction
transactions = []
for row in data1:
    temp = []
    for i, item in enumerate(row):   
        temp.append('%s=%s'%(keys[i],item))
    transactions.append(temp[:])

# List of itemsets
itemsets_list = [defaultdict(int)]

# Generate a list of frequent 1-itemsets
for transaction in transactions:
    for item in transaction:
        itemsets_list[0][frozenset([item])] += 1;

# Remove 1-itemsets that have smaller support than minimum support
for itemset, f in itemsets_list[0].items():
    if float(f)/len(transactions) < min_sup:
        del itemsets_list[0][itemset]

# Generate itemsets for k>2
generate_itemsets(itemsets_list,min_sup,transactions)

# Generating Rules
rules = []
for itemsets in (reversed(itemsets_list)):
    if len(itemsets) != 0:  
        for item in itemsets.keys():
            rules.append(generate_rules(item, min_conf, itemsets[item],transactions))

# Print frequent itemsets
for idx, item in enumerate(itemsets_list):
    if len(item) != 0:
        print "Itemsets of size %d:\n"%(idx + 1)
        for a, freq in item.items():
            print "{0}  support:{1:.1%}\n".format(list(a),float(freq)/len(transactions))
        print "\n"

# Print rules

for idx, item in enumerate(rules):
    if len(item) != 0:
        for a, b in item.items():
            print "{0} ==> {1}\n".format(list(a),list(b))
        

##################################################################
# A TEST USING TRANSACTION DATA FROM THE TEXTBOOK
##################################################################

print "#######################################################\n"
print "### A TEST USING TRANSACTION DATA FROM THE TEXTBOOK ###\n"
print "#######################################################\n"

T = [['I1','I2','I5'],['I2','I4'],['I2','I3'],['I1','I2','I4'],\
['I1','I3'],['I2','I3'], ['I1','I3'],['I1','I2','I3','I5'],['I1','I2','I3']]

print "T = {0}\n".format(T)

# minimum support
ms = float(2)/9
# minimum confidence
mc = 0.7

# 1-itemsets
C_list = [defaultdict(int)]

# Generate a list of frequent 1-itemsets
for t in T:
    for item in t:
        C_list[0][frozenset([item])] += 1;

# Remove 1-itemsets that have smaller support than minimum support
for itemset, f in C_list[0].items():
    if float(f)/len(T) < ms:
        del C_list[0][itemset]

# Generate itemsets for k>2
generate_itemsets(C_list,ms,T)

# Generating Rules
rules = []
for itemsets in (reversed(C_list)):
    if len(itemsets) != 0:  
        for item in itemsets.keys():
            rules.append(generate_rules(item, mc, itemsets[item],T))

# Print frequent itemsets
for idx, item in enumerate(C_list):
    if len(item) != 0:
        print "Itemsets of size %d:\n"%(idx + 1)
        for a, freq in item.items():
            print "{0}  support:{1:.1%}\n".format(list(a),float(freq)/len(T))
        print "\n"

# Print rules

for idx, item in enumerate(rules):
    if len(item) != 0:
        for a, b in item.items():
            print "{0} ==> {1}\n".format(list(a),list(b))



    
