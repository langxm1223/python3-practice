#!/usr/bin/env python3
import os
import requests
from contextlib import contextmanager

# 1. a tuple of only one member can only be declared by
t = (1,)

# 2. private member, __score is renamed, so it seems like you can still set score, but it does not
class Student(object):
	def __init__(self, name, score):
		self.__name = name
		self.__score = score

	def print_score(self):
		print('%s: %s' % (self.__name, self.__score))

	#no setter means read-only
	@property
	def birth(self):
		return self._birth

	@birth.setter
	def birth(self, value):
		self._birth = value

	@property
	def age(self):
		return 2018 - self._birth

# 3. __slots__: limit attributes of a class, only current class
# 4. __setattr__: pay attention to avoid unlimited recursive call
# 5. os.path.join(), os.path.split(): better deal with different OS
# eg. find out all python scripts in one folder
print([x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py'])

# 6. requests.get can get url, but the header in response is for HTTP protocal, not html page
# so the charset cannot be detected
r = requests.get("https://www.baidu.com")
print(r.encoding)
print(r.apparent_encoding)

# 7. In python, the variable is pass by object reference
# eg. list append does not change object reference, but new assignment does
t1 = [0, 1]
t2 = t1
t1.append(0)
print(t2)
t1 = t1 + [1]
print(t2)

# 8. contextlib, add pre post automatically
@contextmanager
def tag(name):
	print("<%s>" % name)
	yield
	print("</%s>" % name)

with tag("h1"):
	print("hello, world")
