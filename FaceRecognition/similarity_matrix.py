import numpy as np
import os
# a = [2,0]
# b = [2,2]
# a1 = np.array(a)
# b1 = np.array(b)
# print(np.linalg.norm(b1 - a1))
# print(np.dot(a1,b1)/(np.linalg.norm(a1)*(np.linalg.norm(b1))))
filelist = os.listdir('../database/features')
print(filelist)
L_list = []
for i in filelist:
    vector = np.loadtxt('../database/features/' + i)
    L_list.append(vector)
result = []
for i in range(0, len(filelist)):
    row = []
    for j in range(0, len(filelist)):
        row.append(np.dot(L_list[i],L_list[j])/(np.linalg.norm(L_list[i])*(np.linalg.norm(L_list[j]))))
    result.append(row)
print(np.array(result))