import heapq as H

class Entry(object):
    def __init__(self, domain_length, cell):
        self.domain_length = domain_length
        self.cell = cell
        
    def __lt__(self, obj):
        """self < obj."""
        return self.domain_length < obj.domain_length

    def __le__(self, obj):
        """self <= obj."""
        return self.domain_length <= obj.domain_length

    def __eq__(self, obj):
        """self == obj."""
        return self.domain_length == obj.domain_length

    def __ne__(self, obj):
        """self != obj."""
        return self.domain_length != obj.domain_length

    def __gt__(self, obj):
        """self > obj."""
        return self.domain_length > obj.domain_length

    def __ge__(self, obj):
        """self >= obj."""
        return self.domain_length >= obj.domain_length
    
class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        H.heapify(self.queue)
        
    def push(self, entry):
        H.heappush(self.queue, entry)
        
    def pop(self):
        return H.heappop(self.queue)
    
    def get_min(self):
        return H.nsmallest(1, self.queue)
    
    def update(self):
        H.heapify(self.queue)
        
    def is_empty(self):
        return len(self.queue) == 0
        
        
        