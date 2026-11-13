def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of any non-empty sub-array
    of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
    if not nums:
        return 0

    current_min = nums[0]
    global_min = nums[0]

    for i in range(1, len(nums)):
        # Either extend the current subarray or start a new one from current element
        # We want minimum, so if current element is smaller than current_min + nums[i], start new
        current_min = min(nums[i], current_min + nums[i])
        global_min = min(global_min, current_min)

    return global_min