import numpy as np
import matplotlib.pyplot as plt
import psutil
import os
'''
a = [1, 2, 3, 4, 5]
b = [7, 7, 7, 7, 7]
c = [8, 8, 8, 8, 8]
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot()
ax.plot(a, b, linewidth=1, antialiased=True, color='red', label='jipa')
ax.plot(a, c, linewidth=1, antialiased=True, color='green')
ax.set_ylim(label='jiba')
plt.show()'''
cpu_c = psutil.cpu_count(logical=False)
path_lib = os.getcwd()
print(path_lib)