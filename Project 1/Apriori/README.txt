"""
Created on Fri Oct 14 11:59:07 2016

@author: Hizkia
Description: Python Implementation of the Apriori Algorithm
This code implements an apriori algorithm to find interesting 
patterns in a census data set retrieved from the following link:
http://archive.ics.uci.edu/ml/datasets/Adult

"""

Apriori Algorithm from the following book:
Han, Jiawei, Micheline K., Jian Pei. "Data Mining Concept and Techniques: 3rd Edition". pg.253.

Code inspiration:
https://github.com/arturhoo

Data set:
http://archive.ics.uci.edu/ml/datasets/Adult

HOW TO RUN THE FILE:
- Download apriori.py
- Open it in an IDE, such as Spyder
- Run the code
- You will be prompted the value of minimum support and minimum confidence
minimum support and minimum confidence are in the range between 0 and 1