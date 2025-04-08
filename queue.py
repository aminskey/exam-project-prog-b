class Queue:
    def __init__(self, _type):
        self.arr = []
        self.type = _type

    def valCheck(self, val):
        return isinstance(val, self.type)

    def push(self, val):
        if not self.valCheck(val): return
        self.arr.append(val)

    def pop(self):
        v = self.arr[0]
        self.arr = self.arr[1:]

        return v