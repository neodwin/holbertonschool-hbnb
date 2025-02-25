from app.persistence.repository import Repository
class Facade:
    def __init__(self):
        self.repo = Repository()
    
    def add_object(self, obj):
        self.repo.add(obj)
    
    def get_object(self, obj_id):
        return self.repo.get(obj_id)
    
    def get_all_objects(self):
        return self.repo.all()
