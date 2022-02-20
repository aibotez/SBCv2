from django.test import TestCase
import os,json,time,random

# Create your tests here.

RangeNums0 = [i for i in range(10)]
RangeNums1 = [i for i in range(65, 91)]
RangeNums2 = [i for i in range(97, 123)]

RangeNums = RangeNums0+RangeNums1+RangeNums2


print(random.choice(RangeNums))
# for i in RangeNums0:
    # print(i)