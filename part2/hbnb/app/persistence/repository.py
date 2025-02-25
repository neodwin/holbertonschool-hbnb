
class Repository:
    def __init__(self):
        self.data = {}
    
    def add(self, obj):
        self.data[obj.id] = obj
    
    def get(self, obj_id):
        return self.data.get(obj_id)
    
    def all(self):
        return list(self.data.values())
