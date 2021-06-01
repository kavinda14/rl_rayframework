import numpy as np
import matplotlib.pyplot as plt
  
N = 3
ind = np.arange(N) 
width = 0.25
  
x = [74.7558, 136.0353, 6.5720]

bar1 = plt.bar(ind, x, width, color = 'r')
  
y = [340.7981, 151.0702, 40.7941]

bar2 = plt.bar(ind+width, y, width, color='g')
  
z = [46.0373, 32.9756, 7.3584]

bar3 = plt.bar(ind+width*2, z, width, color = 'b')
  
plt.ylabel('Runtime')
plt.title("Single Core vs Distributed without Evaluation (map_DH)")
  
plt.xticks(ind+width,['Q-Learning', 'SARSA', 'Dist Q-Learning'])
plt.legend( (bar1, bar2, bar3), ('\u03B5=0.3, \u03B2=0.001 ', '\u03B5=0.3, \u03B2=0.1', '\u03B5=0.05, \u03B2=0.001') )
plt.show()