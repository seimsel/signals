from uuid import uuid4
from .service import Service, method

class MemoryService(Service):
    def __init__(self, app, name):
        self.items = []
        super().__init__(app, name)
    
    @method
    def find(self, *params):
        return self.items

    @method
    def get(self, id, *params):
        for item in self.items:
            if item['id'] == id:
                return item

    @method
    def create(self, data, *params):
        item = {
            'id': str(uuid4()),
            **data
        }
        self.items.append(item)

        return item

    @method
    def update(self, id, data, *params):
        for i, item in enumerate(self.items):
            if item['id'] == id:
                self.items[i] = {
                    'id': id,
                    **data
                }

                return item

    @method
    def patch(self, id, data, *params):
        for item in self.items:
            if item['id'] == id:
                return item.update(data)

    @method 
    def remove(self, id, *params):
        for item in self.items:
            if item['id'] == id:
                return self.items.remove(item)
