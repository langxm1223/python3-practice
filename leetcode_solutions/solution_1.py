#!/usr/bin/env python3

class Solution:
	# problem 1
	def twoSum(self, nums, target):
		"""
		:type nums: List[int]
		:type target: int
		:rtype: List[int]
		"""
		nums_dict = {}
		for i, num in enumerate(nums):
			n = target - num
			if n not in nums_dict:
				nums_dict[num] =  i
			else:
				return [nums_dict[n], i]

	# problem 7
	def reverse(self, x):
		"""
		:type x: int
		:rtype: int
		"""
		if x > 0: x_str = str(x)
		else: x_str = str(-x)
		x_str_r = x_str[::-1]
		if x > 0: result = int(x_str_r)
		else: result = -int(x_str_r)
		if (-1 << 31) < result < ((1 << 31)-1): return result
		else: return 0

	# problem 9
	def isPalindrome(self, x):
		"""
		:type x:int
		:rtype: bool
		"""
		if x < 0: return False
		elif str(x) == str(x)[::-1]: return True
		else: return False

	# problem 13
	def romanToInt(self, s):
		"""
		:type s: str
		:rtype: int
		"""
		roman_dict = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
		result = 0
		if len(s) == 1: return roman_dict[s]
		else:
			for i in range(len(s)-1):
				if roman_dict[s[i]] < roman_dict[s[i+1]]: result += -roman_dict[s[i]]
				else: result += roman_dict[s[i]]
		return result + roman_dict[s[-1]]

	# problem 14
	def longestCommonPrefix(self, strs):
		"""
		:type strs: List[str]
		:rtype: str
		"""
		result = ""
		if len(strs) > 0:
			for i in range(len(strs[0])):
				str_check = strs[0][0:i+1]
				for word in strs:
					if len(word) < len(str_check) or str_check != word[0:i+1] : return result
				result = str_check
		return result

	# problem 20
	def isValid(self, s: str) -> bool:
		while "()" in s or "{}" in s or '[]' in s:
			s = s.replace("()", "").replace('{}', "").replace('[]', "")
		return s == ''

if __name__ == "__main__":	
	sol = Solution()
	# problem 1
	output = sol.twoSum([2, 7, 11, 15], 26)
	print(output)
	# problem 7
	output = sol.reverse(1534236469)
	print(output)
	# problem 9
	output = sol.isPalindrome(153)
	print(output)
	# problem 13
	output = sol.romanToInt("MCMXCIV")
	print(output)
	# problem 14
	output = sol.longestCommonPrefix(["a"])
	print(output)
	# problem 20
	output = sol.isValid("]")
	print(output)