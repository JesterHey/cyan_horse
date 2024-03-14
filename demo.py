from typing import List
class Solution:
    def maxArrayValue(self, nums: List[int]) -> int:
        n = len(nums)
        i = n - 1
        while i > 0 and len(nums) > 1:
            cur = nums[i]
            formal = nums[i - 1]
            if formal <= cur:
                cur += formal
                nums[i] = cur
                nums.pop(i - 1)
                i = len(nums) - 1
            else:
                i -= 1
        return max(nums)

s = Solution()
print(s.maxArrayValue([5,3,3]))
print(s.maxArrayValue([2,3,7,9,3]))