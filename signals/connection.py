from uuid import uuid4

class Connection:
    def __init__(self, source_id, output, sink_id, input):
        self.id = str(uuid4())
        self.source_id = source_id
        self.output = output
        self.sink_id = sink_id
        self.input = input
