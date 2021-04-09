import matplotlib.pyplot as plt

if __name__ == "__main__":

    total_times = [1.91796, 3.22042, 3.22477, 6.13340]
    cpus = [4, 3, 2, 1]

    plt.plot(cpus,total_times)
    plt.title('Map Reduce Task')
    plt.xlabel('CPUs')
    plt.ylabel('Total Time')
    plt.xticks(range(1,5))
    plt.show()