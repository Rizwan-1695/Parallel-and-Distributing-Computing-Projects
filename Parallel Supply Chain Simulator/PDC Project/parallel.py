from multiprocessing import Process, Manager
from simulation import run_simulation

def worker(run_id, shared_list):
    result = run_simulation(run_id)
    shared_list.extend(result)

def run_parallel():
    processes = []
    manager = Manager()
    shared_list = manager.list()

    for i in range(3):  # 3 parallel simulations
        p = Process(target=worker, args=(i, shared_list))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return list(shared_list)