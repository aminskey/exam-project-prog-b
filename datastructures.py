class Queue:
    def __init__(self):
        self.arr = []


    def push(self, val):
        self.arr.append(val)

    def seek(self, val):
        return self.arr.index(val)

    def seekByAttr(self, attr):
        for i, val in enumerate(self.arr):
            if hasattr(val, attr):
                return (i, val)

    def seekByAttrVal(self, attr, val):
        for i, v in enumerate(self.arr):
            try:
                if getattr(v, attr) == val:
                    return (i, v)
            except AttributeError:
                continue
        return None
    def pop(self):
        v = self.arr[0]
        self.arr = self.arr[1:]

        return v