import numpy as np
import matplotlib.pyplot as plt
  
N = 3
ind = np.arange(N) 
width = 0.25
  
x = [11.0356, 6.4825, 4.7722]

bar1 = plt.bar(ind, x, width, color = 'r')
  
y = [125.2937, 26.7950, 18.2415]

bar2 = plt.bar(ind+width, y, width, color='g')
  
z = [10.0786, 7.8340, 8.3421]

bar3 = plt.bar(ind+width*2, z, width, color = 'b')
  
plt.ylabel('Runtime')
plt.title("Dist Q-Learning With Different Collectors Without Evaluation (map_DH)")
  
plt.xticks(ind+width,['Collectors = 2', 'Collectors = 4', 'Collectors = 8'])
plt.legend( (bar1, bar2, bar3), ('\u03B5=0.3, \u03B2=0.001 ', '\u03B5=0.3, \u03B2=0.1', '\u03B5=0.05, \u03B2=0.001') )
plt.show()