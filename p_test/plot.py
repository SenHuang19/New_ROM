import matplotlib.pyplot as plt
import numpy as np

a=np.loadtxt('p_test.csv',delimiter=',')
b=[]
c=[]
d=[]
e=[]
for i in range(len(a)):
     b.append(a[i][0])
     c.append(a[i][1])
     d.append(a[i][2])
     e.append(a[i][3])

plt.plot(b,c,label='tout')
plt.plot(b,d,label='compressor status')
plt.plot(b,e,label='previous temp')

plt.ylabel('Pearson correlation')
plt.xlabel('Sampling interval [minute]')
plt.legend(loc='best')
plt.savefig('Pearson.png',bbox_inches = 'tight',pad_inches = 0.1)
plt.show()
