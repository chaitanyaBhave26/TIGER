from netCDF4 import Dataset
import numpy as np
import os

class ExodusReader:
    def __init__(self,file_name):
        if os.path.exists(file_name):
            self.file_name = file_name
            self.mesh = Dataset(self.file_name,'r') #,parallel=parallel_flag
            self.get_times()
            self.get_xyz()
            try:
                self.get_nodal_names()
            except:
                pass
            try:
                self.get_elem_names()
            except:
                pass
        else:
            print("File path does not exist. Please check if file path and name are correct.")
            exit()
    def get_times(self):
        self.times = self.mesh.variables['time_whole'][:]
        return self.times
    def get_xyz(self):
        self.dim = 0
        try:
            x = self.mesh.variables['coordx'][:]
            self.dim += 1
        except:
            print("X dimension empty. Mesh must have atleast one non-empty dimension")
            return -1
        try:
            y = self.mesh.variables['coordy'][:]
            self.dim += 1
        except:
            y = np.zeros(x.shape)
        try:
            z = self.mesh.variables['coordz'][:]
            self.dim += 1
        except:
            z = np.zeros(x.shape)
        connect = self.mesh.variables['connect1'][:]
        xyz = np.array([x[:], y[:],z[:]]).T
        X = x[connect[:] -1]
        Y = y[connect[:] -1]
        Z = z[connect[:] -1]

        self.x = np.asarray(X)
        self.y = np.asarray(Y)
        self.z = np.asarray(Z)
        self.connect = self.mesh.variables['connect1'][:]

        return (self.x,self.y,self.z)
    def get_nodal_names(self):
        names = self.mesh.variables["name_nod_var"]
        names.set_auto_mask(False)
        self.nodal_var_names = [b"".join(c).decode("latin1") for c in names[:]]
        return self.nodal_var_names
    def get_elem_names(self):
        names = self.mesh.variables["name_elem_var"]
        names.set_auto_mask(False)
        elem_var_names = []
        for n in names[:]:
            temp = [i.decode('latin1') for i in n   ]
            idx = temp.index('')
            elem_var_names+=[''.join(temp[:idx]) ]
        self.elem_var_names = elem_var_names
        return self.elem_var_names
    def get_var_values(self,var_name,timestep):
        if var_name in self.nodal_var_names:
            idx = self.nodal_var_names.index(var_name)
            var_name_exodus = 'vals_nod_var'+str(idx+1)
            var_vals_nodal = self.mesh.variables[var_name_exodus]
            if timestep == -1:
                var_vals = np.average([ var_vals_nodal[:,(self.connect[:,i] -1) ] for i in range(self.connect.shape[1]) ],0 )
            else:
                var_vals = np.average([ var_vals_nodal[timestep,(self.connect[:,i] -1) ] for i in range(self.connect.shape[1]) ],0 )

        elif var_name in self.elem_var_names:
            idx = self.elem_var_names.index(var_name)
            var_name_exodus = 'vals_elem_var'+str(idx+1)+'eb1'
            var_vals = np.asarray(self.mesh.variables[var_name_exodus][timestep])
        else:
            print("Value not in nodal or elemental variables. Check variable name.")
            return -1

        return var_vals
