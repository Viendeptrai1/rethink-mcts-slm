def minSubArraySum(nums):
    if not nums:
        return 0
    
    current_sum = min_sum = nums[0]
    
    for num in nums[1:]:
        current_sum = min(num, current_sum + num)
        min_sum = min(min_sum, current_sum)
    
    return min_sum