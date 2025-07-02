import heapq
from collections import defaultdict

class DualHeap:
    def __init__(self, k):
        self.small = []
        self.large = []
        self.delayed = defaultdict(int)

        self.k = k
        
        self.small_size = 0
        self.large_size = 0


    def prune(self, heap):
        while heap and self.delayed[heap[0][1]]:
            self.delayed[heap[0][1]] -= 1
            heapq.heappop(heap)


    def balance(self):
        if self.small_size > self.large_size + 1:
            val, idx = heapq.heappop(self.small)
            heapq.heappush(self.large, (-val, idx))
            self.small_size -= 1
            self.large_size += 1
            self.prune(self.small)
        elif self.small_size < self.large_size:
            val, idx = heapq.heappop(self.large)
            heapq.heappush(self.small, (-val, idx))
            self.small_size += 1
            self.large_size -= 1
            self.prune(self.large)

    def insert(self, val, idx):
        heapq.heappush(self.small, (-val, idx))
        self.small_size += 1
        self.balance()

    def erase(self, num, idx):
        self.delayed[(num, idx)] += 1
        if num <= self.small[0][0]:
            self.small_size -= 1
            if (num, idx) == self.small[0]:
                self.prune(self.small)

        else:
            self.large_size -= 1
            if (num, idx) == self.large[0]:
                self.prune(self.large)

        self.balance()
        

    def get_median(self):
        if self.k % 2 == 1:
            return -self.small[0][0]
        else:
            return (-self.small[0][0] + self.large[0][0]) / 2
        
    
def medianSlidingWindow(nums, k):
    if not nums or k == 0:
        return []
    
    dh = DualHeap(k)

    result = []


    for i in range(k):
        dh.insert(nums[i], i)
    result.append(dh.get_median())


    for i in range(k, len(nums)):
        dh.insert(nums[i], i)
        dh.erase(nums[i - k], i - k)
        result.append(dh.get_median())


    return result


nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(medianSlidingWindow(nums, k))