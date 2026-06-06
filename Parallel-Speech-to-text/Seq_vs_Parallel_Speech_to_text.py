import whisper
import os
import time
from multiprocessing import Pool
import matplotlib.pyplot as plt

folder = "Data Set speech processing/Girls"

files = [os.path.join(folder,f) for f in os.listdir(folder)]



def process(file):
    model = whisper.load_model("tiny")
    result = model.transcribe(file, fp16=False)
    return result["text"]

if __name__ == "__main__":

    print("=========== Sequential Processing ============")

    start = time.time()

    for file in files:
        text = process(file)
        print(file, ":", text)

    seq_time = time.time() - start

    print("Sequential Time:", seq_time)


    print("\n=========== Parallel Processing ============")

    start = time.time()

    with Pool(4) as p:
        output = p.map(process, files)

    par_time = time.time() - start

    print("Parallel Time:", par_time)

    print("\nTranscription Output:")
    print(output)


    speedup = seq_time / par_time

    print("\n=========== Performance ============")

    print("Speedup:", speedup)


    # GRAPH
    methods = ["Sequential","Parallel"]
    times = [seq_time, par_time]

    plt.bar(methods, times)

    plt.xlabel("Processing Method")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Sequential vs Parallel Speech Processing")

    plt.savefig("performance_graph.png")

    print("Graph saved as performance_graph.png")