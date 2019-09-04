from uuid import uuid4
from .service import Service

class MemoryService(Service):
    def __init__(self, app, name):
        self.items = []
        super().__init__(app, name)
    
    def find(self, *params):
        return self.items

    def get(self, id, *params):
        for item in self.items:
            if item['id'] == id:
                return item

    def create(self, data, *params):
        item = {
            'id': str(uuid4()),
            **data
        }
        self.items.append(item)

        return item

    def update(self, id, data, *params):
        for i, item in enumerate(self.items):
            if item['id'] == id:
                self.items[i] = {
                    'id': id,
                    **data
                }

                return item

    def patch(self, id, data, *params):
        for item in self.items:
            if item['id'] == id:
                return item.update(data)
    
    def remove(self, id, *params):
        for item in self.items:
            if item['id'] == id:
                return self.items.remove(item)
