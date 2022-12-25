from .error import PCloudError

class PCloudResponse:
    def __init__(self, data):
        self.__data = data

    def __contains__(self, name):
        return (name != 'result') and (name in self.__data)

    def __getitem__(self, name):
        if (name == 'result'): #pragma: no cover
            raise KeyError("No such key: 'result'")
        return self.__data[name]

    def __delitem__(self, name):
        if (name == 'result'): #pragma: no cover
            raise KeyError("No such key: 'result'")
        del self.__data[name]

    def __repr__(self): #pragma: no cover
        r = "PCloudResponse(\n"
        for k, v in self.__data.items():
            if (k != 'result'):
                r += f"    {k}: {v!r}\n"
        r += ")"
        return r

    @property
    def result(self):
        return int(self.__data['result'])

    def raise_for_status(self):
        if (self.result != 0):
            raise PCloudError(self.result)
