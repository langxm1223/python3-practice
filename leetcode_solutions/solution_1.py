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

if __name__ == "__main__":	
	sol = Solution()
	# problem 1
	output = sol.twoSum([2, 7, 11, 15], 26)
	print(output)
	# problem 7
	output = sol.reverse(1534236469)
	print(output)