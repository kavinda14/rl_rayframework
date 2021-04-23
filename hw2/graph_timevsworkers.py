import matplotlib.pyplot as plt

#map_8
dist_v1 = [0.803361177444458, 0.7904572486877441, 0.5251586437225342] 
dist_v2 = [1.1900033950805664, 1.8223743438720703, 2.2798309326171875]
workers = [2, 4, 8] 

plt.plot(workers, dist_v1)
plt.plot(workers, dist_v2)
plt.xlabel('Number of Workers (map_8)')
plt.ylabel('Time')
plt.legend(['Distributed VI Version 1', 'Distributed VI Version 2'], loc='upper right')
plt.show()

#map_16
dist_v1 = [4.619285345077515, 2.0417048931121826,  1.457641839981079] 
dist_v2 = [3.095673084259033, 3.3745386600494385, 4.679270029067993]
workers = [2, 4, 8] 

plt.plot(workers, dist_v1)
plt.plot(workers, dist_v2)
plt.xlabel('Number of Workers (map_16)')
plt.ylabel('Time')
plt.legend(['Distributed VI Version 1', 'Distributed VI Version 2'], loc='upper right')
plt.show()

#map_32
dist_v1 = [32.46612215042114, 19.637737035751343,  18.358941078186035] 
dist_v2 = [13.94634485244751, 15.629204034805298, 16.326448917388916]
workers = [2, 4, 8] 

plt.plot(workers, dist_v1)
plt.plot(workers, dist_v2)
plt.xlabel('Number Of Workers (map_32)')
plt.ylabel('Time')
plt.legend(['Distributed VI Version 1', 'Distributed VI Version 2'], loc='upper right')
plt.show()