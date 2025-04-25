class Queue:
    def __init__(self):
        self.__arr = []


    def push(self, val):
        self.__arr.append(val)

    def seek(self, val):
        return self.__arr.index(val)

    def seekByAttr(self, attr):
        for i, val in enumerate(self.__arr):
            if hasattr(val, attr):
                return (i, val)

    def seekByAttrVal(self, attr, val):
        for i, v in enumerate(self.__arr):
            try:
                if getattr(v, attr) == val:
                    return (i, v)
            except AttributeError:
                continue
        return None

    @property
    def length(self):
        return len(self.__arr)

    @property
    def arr(self):
        return self.__arr

    def seekAllByAttr(self, attr):
        l = []
        for val in self.arr:
            if hasattr(val, attr):
                l.append(val)

        return l

    def pop(self):
        v = self.__arr[0]
        self.__arr = self.__arr[1:]

        return v