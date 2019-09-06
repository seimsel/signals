from uuid import uuid4
from .service import Service, method

class MemoryService(Service):
    def __init__(self, app, name):
        self.items = []
        super().__init__(app, name)
    
    @method
    def find(self, filterFunction=None, *params):
        if not filterFunction:
            return self.items

        return [item for item in self.items if filterFunction(item)]

    @method
    def get(self, uid, *params):
        if type(uid) == list:
            result = []
            for single_uid in uid:
                result.append(self.get(single_uid, *params))

            return result

        for item in self.items:
            if item['id'] == uid:

                if len(params) == 0:
                    return item

                result = {}

                for param in params:
                    result[param] = item[param]

                return result

    @method
    def create(self, data, *params):
        item = {
            'id': str(uuid4()),
            **data
        }
        self.items.append(item)

        return item

    @method
    def update(self, uid, data, *params):
        for i, item in enumerate(self.items):
            if item['id'] == uid:
                self.items[i] = {
                    'id': uid,
                    **data
                }

                return item

    @method
    def patch(self, uid, data, *params):
        for item in self.items:
            if item['id'] == uid:
                return item.update(data)

    @method 
    def remove(self, uid, *params):
        for item in self.items:
            if item['id'] == uid:
                return self.items.remove(item)
