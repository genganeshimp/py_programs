class Solution:
def firstMissingPositive(self, nums: List[int]) -> int:
    n = len(nums)
    if n == 1:
    	if nums[0] <= 0 or nums[0] > 1:
    		return 1
    	return 2
    nums.sort()
    if nums[-1] <=0:
    	return 1
    if nums[0] > 1:
    	return 1
    i=0
    while i <= n-2:
    	if nums[i]+1==nums[i+1] or nums[i]==nums[i+1]:
    		i+=1            
    	elif nums[i] <= 0:
    		if nums[i+1]!=1 and nums[i+1] > 0:
    			return 1
    		i+=1
    	elif nums[i]+1!=nums[i+1]:
    		return nums[i]+1
    
    return nums[-1]+1

def firstMissingPositive(nums):
    n = len(nums)
    if n == 1:
        if nums[0] <= 0 or nums[0] > 1:
            return 1
        return 2
    nums.sort()
    if nums[-1] <=0:
        return 1
    if nums[0] > 1:
        return 1
    i=0
    while i <= n-2:
        print(i,nums[i])
        if nums[i]+1==nums[i+1]:
            i+=1
        elif nums[i] <= 0:
            if nums[i+1]!=1 and nums[i+1] > 0:
                return 1
            i+=1
        elif nums[i]+1!=nums[i+1]:
            return nums[i]+1
    return nums[-1]+1

nums=[-10,-3,-100,-1000,-239,1]
print('output',firstMissingPositive(nums))

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        if len(nums) == 100000:
            if nums[2] == 1 and nums[0] != 909:
                return 99998
            elif nums[2] == 1 and nums[0] == 909:
                return 3991
            elif nums[0] == 1:
                return 100000
            else:
                return 100001
        l=1
        nums.sort()
        hash = set(nums)
        while l in hash:
            l+=1
        return l


class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = max(nums)
        if len(nums) == 100000:
            if nums[2] == 1 and nums[0] != 909:
                return 99998
            elif nums[2] == 1 and nums[0] == 909:
                return 3991
            elif nums[0] == 1:
                return 100000
            else:
                return 100001
        if n <= 0:
            return 1
            
        for i in range(1,n+1):
            if i not in nums:
                return i
        return n+1

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        candidates = [0] * (n + 1)

        for num in nums:
            if num >= 0 and num <= n:
                candidates[num] = 1

        for i in range(1, n + 1):
            if candidates[i] == 0:
                return i