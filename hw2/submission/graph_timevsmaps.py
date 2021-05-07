import matplotlib.pyplot as plt

map_sizes = [8*8, 16*16, 32*32]
sync_v1 = [0.6294584274291992, 13.782054424285889, 343.7200493812561]
sync_v2 = [0.22376012802124023, 1.7814924716949463, 14.816197872161865]
dist_v1 = [3.3376457691192627, 13.526809215545654, 41.454113960266113]
dist_v2 = [1.8064510822296143, 3.929654359817505, 13.990786075592041]

plt.plot(map_sizes, sync_v1)
plt.plot(map_sizes, sync_v2)
plt.plot(map_sizes, dist_v1)
plt.plot(map_sizes, dist_v2)
plt.xlabel('Number of States')
plt.ylabel('Time')
plt.legend(['Synchronized v1', 'Synchronized v2', 'Distributed v1', 'Distributed v2'], loc='upper right')
plt.show()
