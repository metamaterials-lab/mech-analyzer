class IterUtil:
    def __init__(self, var : list[list[float]]):
        self.var = var
    def __iter__(self):
        i = 0
        while True:
            res = []
            for v in self.var:
                if i < len(v): res.append( v[i] )
            i += 1
            if res: yield res
            else: break