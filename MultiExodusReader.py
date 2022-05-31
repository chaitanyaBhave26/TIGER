import ExodusReader
import glob
import numpy as np

class MultiExodusReader:
    def __init__(self,file_names):
        self.file_names = glob.glob(file_names)
        global_times = set()
        file_times = []
        exodus_readers = []
        for file_name in self.file_names:
            er = ExodusReader.ExodusReader(file_name)
            times = er.times
            global_times.update(times[:])
            exodus_readers+= [er]
            file_times+=[ [min(times),max(times)] ]
        self.dim = exodus_readers[0].dim
        global_times = list(global_times)
        global_times.sort()
        self.global_times = global_times
        self.exodus_readers = exodus_readers
        self.file_times = np.asarray(file_times)

    def get_data_from_file_idx(self,var_name,read_time,i):
        er = self.exodus_readers[i]
        x = er.x
        y = er.y
        z = er.z
        idx = np.where(read_time == er.times)[0][0]
        c = er.get_var_values(var_name,idx)
        return (x,y,z,c)

    def get_data_at_time(self,var_name,read_time):
        X = []
        Y = []
        Z = []
        C = []
        for (i,file_time) in enumerate(self.file_times):
            if ( file_time[0]<= read_time and file_time[1]>= read_time  ):
                x,y,z,c = self.get_data_from_file_idx(var_name,read_time,i)
                try:
                    X.append(x)
                    Y.append(y)
                    Z.append(z)
                    C.append(c)
                except:
                    # Is this actually what you want it to do?
                    X = x
                    Y = y
                    Z = z
                    C = c
            else:
                pass
        X = np.vstack(X)
        Y = np.vstack(Y)
        Z = np.vstack(Z)
        C = np.hstack(C)
        return (X,Y,Z,C)
