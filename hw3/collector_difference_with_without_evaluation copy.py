import numpy as np
import matplotlib.pyplot as plt
  
N = 3
ind = np.arange(N) 
width = 0.25
  
x = [12.3488, 7.5223, 8.1793]

bar1 = plt.bar(ind, x, width, color = 'r')
  
y = [90.5524, 40.4150, 59.3817]

bar2 = plt.bar(ind+width, y, width, color='g')
  
z = [13.6648, 8.0068, 5.8763]

bar3 = plt.bar(ind+width*2, z, width, color = 'b')
  
plt.ylabel('Runtime')
plt.title("Dist Q-Learning With Different Collectors (map_DH)")
  
plt.xticks(ind+width,['Collectors = 2', 'Collectors = 4', 'Collectors = 8'])
plt.legend( (bar1, bar2, bar3), ('\u03B5=0.3, \u03B2=0.001 ', '\u03B5=0.3, \u03B2=0.1', '\u03B5=0.05, \u03B2=0.001') )
plt.show()