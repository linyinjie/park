import random
import params

# A range predicate to issue to the database.
class Query:
    def __init__(self, starts, ends):
        # starts and ends are points at opposite ends of the query rectangle that uniquely define
        # it.
        self.start_pt = starts
        self.end_pt = ends
        for s, e in zip(starts, ends):
            if s > e:
                raise Exception("Invalid query: range has 0 volume")

class Action:
    def __init__(self, dims, cols):
        # The list of dimensions to index. The last dimension is the sort dimension; the others are
        # used to form the grid.
        # Dimensions are 0-indexed.
        self.dimensions = dims
        # A list of size len(self.dimensions)-1, containing
        # the number of columns in each dimension.
        self.columns = cols

def DataIterator(datafile):
    with df as open(datafile, 'rb'):
        while True:
            # Each value is a 64-bit number
            pt_bytes = df.read(params.NDIMS * 8)
            if not pt_bytes:
                return
            fmt_str = 'q' * params.NDIMS
            pt = list(struct.unpack('<' + fmt_str, pt_bytes))
            yield pt

class DataObs:
    def __init__(self, datafile):
        df = datafile if datafile is not None else params.DATA_FILE
        self.data_iterator = DataIterator(df)

class QueryObs:
    def __init__(self, qs, times):
        self.queries = []
        for q in qs:
            d = len(q)/2
            # Each query is a 2*d numpy array, with the start and endpoints concatenated
            self.queries.append(Query(q[:d], q[d:]))

    def valid(self):
        valid = True
        valid &= len(s) == params.QUERIES_PER_STEP
        for q in s.valid:
            valid &= isinstance(q, QueryResult)
        return valid




