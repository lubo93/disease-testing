import time
import numpy as np
from testing import Ptot
import matplotlib.pyplot as plt

if __name__ == "__main__": 
    
    div = int(1e4)
    # number of tests
    Q = int(8e6)//div
    # population size
    N = int(40e6)//div
    
    R = 0
    
    Ip_arr = np.arange(500, 3000)
    
    # FNR variations
    Ptot_arr_save = []
    Ptot_arr_save.append(Ip_arr)
    
    FNR = 0.2
    
    start_time = time.time()
    Ptot_arr = [Ptot(Q, I = Ip, S = N - Ip - R, R = R, Q = Q, \
                   b = 2, FNR = FNR, FPR = 0.05, replacement = True) 
                   for Ip in Ip_arr]

    Ptot_arr_save.append(Ptot_arr)
    
    np.savetxt("testing_data_replacement_true_CA.dat", np.c_[Ptot_arr_save].T)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    print(Ptot_arr_save)
    plt.figure()
    plt.plot(Ptot_arr_save[0], Ptot_arr_save[1])
    plt.show()