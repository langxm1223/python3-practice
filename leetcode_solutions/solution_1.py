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
		# for i in range(len(nums)):
		# 	for j in range(len(nums) - i - 1):
		# 		if nums[i] + nums[i + j + 1] == target: return [i, i + j + 1]

if __name__ == "__main__":	
	sol = Solution()
	output = sol.twoSum([2, 7, 11, 15], 26)
	print(output)