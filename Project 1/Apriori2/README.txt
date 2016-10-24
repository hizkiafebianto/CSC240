"""
Created on Sun Oct 23 11:59:07 2016

@author: Hizkia
Description: Improving the efficiency of Apriori algorithm by
transaction reduction. This method is implemented based on the 
following premise:
A transaction that does not contain any frequent k-itemsets 
cannot contain any frequent (k+1)-itemsets. 
This method can be found on page 255 in the book "Data Mining
Concepts and Techniques 3rd Edition", Han Jiawei, et al.

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