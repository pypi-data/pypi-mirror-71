# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 14:57:38 2018
permutation test: Parallel elastic net regression
Note.：The program is divided into many blocks
       so as to avoid interruption.
   input:
       fileName=fileName to save results
@author: Li Chao
"""

#from scipy import io
import sys  
sys.path.append(r'D:\myCodes\LC_MVPA\Python\MVPA_Python\utils')
# import module
#from joblib import Parallel, delayed
from sklearn.externals.joblib import Parallel, delayed
#from lc_write_read_h5py import write_h5py
from lc_read_write_Mat import write_mat
#from read_write_Mat_LC import write_mat
import time,os
import numpy as np
import lc_svc_rfe_cv as lsvc



# def
def permutation(X,y,k,N_perm,fileName):
    # instantiating object
    model=lsvc.svc_rfe_cv(permutation=1,num_jobs=1)#
    #
    start_time=time.clock()
    #
    Parallel(n_jobs=10,backend='threading')\
    (delayed(run_svc)(X,y,k,n_perm,model,fileName)\
     for n_perm in np.arange(N_perm))
    #
    end_time=time.clock()
    print('running time is: {:.1f} second'.format(end_time-start_time))  

def run_svc(X,y,k,n_perm,model,fileName):
    print('we have already completed {} permutation'.format(n_perm))
    y_rand=np.random.permutation(y)
    predict,dec,y_sorted,weight=model.main_svc_rfe_cv(X,y_rand,k)
#    # write h5py
#    write_h5py(fileName,'perm'+str(n_perm),['predict','dec','y_sorted','weight'],\
#          [predict,dec,y_sorted,weight])
#     write mat
    write_mat(os.path.join(fileName,str(n_perm)),\
              dataset_name=['predict','dec','y_sorted','weight'],\
             dataset=[predict,dec,y_sorted,weight])
    


#
if __name__=='__main__':
    print('=====running======')
    permutation(X,y,k=5,N_perm=20,fileName=r'D:\myCodes\LC_MVPA\Python\MVPA_Python\perm')