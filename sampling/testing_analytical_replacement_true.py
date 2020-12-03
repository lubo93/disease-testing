import time
import numpy as np
from testing import Ptot

if __name__ == "__main__": 
    
    # number of tests
    Q = int(1e3)
    # population size
    N = 1e4
    
    I = 1e2
    R = 2e2
    S = N - I - R    
    
    Qtildep_arr = np.arange(Q)[:300]
    
    # FNR variations
    Ptot_arr_save = []
    Ptot_arr_save.append(Qtildep_arr)
    
    FNR_arr = [1e-15, 0.05, 0.1, 0.2]
    
    start_time = time.time()
    for i in range(len(FNR_arr)):
        Ptot_arr = [Ptot(Qtildep, I = I, S = S, R = R, Q = Q, \
                   b = 1, FNR = FNR_arr[i], FPR = 1e-15, replacement = True) 
                   for Qtildep in Qtildep_arr]
        Ptot_arr_save.append(Ptot_arr)
    
    np.savetxt("testing_data_replacement_true_FNR.dat", np.c_[Ptot_arr_save].T)
    print("--- %s seconds ---" % (time.time() - start_time))

    # FPR variations
    Ptot_arr_save = []
    Ptot_arr_save.append(Qtildep_arr)
    
    FPR_arr = [1e-15, 0.01, 0.05, 0.1, 0.2]
    
    start_time = time.time()
    for i in range(len(FPR_arr)):
        Ptot_arr = [Ptot(Qtildep, I = I, S = S, R = R, Q = Q, \
                   b = 1, FNR = 1e-15, FPR = FPR_arr[i], replacement = True) 
                   for Qtildep in Qtildep_arr]
        Ptot_arr_save.append(Ptot_arr)
    
    np.savetxt("testing_data_replacement_true_FPR.dat", np.c_[Ptot_arr_save].T)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    # b variations
    Ptot_arr_save = []
    Ptot_arr_save.append(Qtildep_arr)
    
    b_arr = [0.5, 1, 1.5, 2]
    
    start_time = time.time()
    for i in range(len(b_arr)):
        Ptot_arr = [Ptot(Qtildep, I = I, S = S, R = R, Q = Q, \
                   b = b_arr[i], FNR = 1e-15, FPR = 1e-15, replacement = True) 
                   for Qtildep in Qtildep_arr]
        Ptot_arr_save.append(Ptot_arr)
    
    np.savetxt("testing_data_replacement_true_b.dat", np.c_[Ptot_arr_save].T)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    # b variations
    Ptot_arr_save = []
    Ptot_arr_save.append(Qtildep_arr)
    
    IR_arr = [200, 400, 600, 800, 1000]
    
    start_time = time.time()
    for i in range(len(IR_arr)):
        S = N - IR_arr[i]
        Ptot_arr = [Ptot(Qtildep, I = IR_arr[i]/2, S = S, R = IR_arr[i]/2, Q = Q, \
                   b = 1, FNR = 1e-15, FPR = 1e-15, replacement = True) 
                   for Qtildep in Qtildep_arr]
        Ptot_arr_save.append(Ptot_arr)
    
    np.savetxt("testing_data_replacement_true_IR.dat", np.c_[Ptot_arr_save].T)
    print("--- %s seconds ---" % (time.time() - start_time))