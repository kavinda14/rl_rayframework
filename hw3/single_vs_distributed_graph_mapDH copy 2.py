import numpy as np
import matplotlib.pyplot as plt
  
N = 3
ind = np.arange(N) 
width = 0.25
  
x = [69.2964, 113.4861, 4.0763]

bar1 = plt.bar(ind, x, width, color = 'r')
  
y = [26.7820, 126.8947, 16.7820]

bar2 = plt.bar(ind+width, y, width, color='g')
  
z = [31.7901, 33.0125, 5.3231]

bar3 = plt.bar(ind+width*2, z, width, color = 'b')
  
plt.ylabel('Runtime')
plt.title("Single Core vs Distributed (map_DH)")
  
plt.xticks(ind+width,['Q-Learning', 'SARSA', 'Dist Q-Learning'])
plt.legend( (bar1, bar2, bar3), ('\u03B5=0.3, \u03B2=0.001 ', '\u03B5=0.3, \u03B2=0.1', '\u03B5=0.05, \u03B2=0.001') )
plt.show()