import matplotlib.pyplot as plt

def plot_results(data):
    plt.figure()
    plt.bar(range(len(data)), data)
    plt.xlabel("Orders")
    plt.ylabel("Time Taken")
    plt.title("Supply Chain Simulation")

    # Save graph as image
    plt.savefig("static/graph.png")
    plt.close()