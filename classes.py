class Node:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.splitFeature = None
        self.label = None
        self.leaf = False
        self.vote = None
        self.majority = None
        
class Representative:
    def __init__(self, id, party, votes):
        self.id = id
        self.party = party
        self.votes = votes