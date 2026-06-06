import simpy
import random

def delivery(env, name, results):
    start_time = env.now
    
    # Processing time
    yield env.timeout(random.randint(1, 5))
    
    # Delivery time
    yield env.timeout(random.randint(2, 6))
    
    end_time = env.now
    
    results.append(end_time - start_time)

def run_simulation(run_id):
    env = simpy.Environment()
    results = []
    
    for i in range(5):
        env.process(delivery(env, f"Customer {i+1}", results))
    
    env.run()
    
    print(f"Simulation {run_id} completed")
    return results