import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

# Simulation Parameters
RANDOM_SEED = 42
SIM_TIME = 180  # minutes (5-8pm)
NUM_CONDUCTORS = 1
NUM_QUEUES = 2
NUM_BUSES_BASE = 5
BUS_CAPACITY = 58
BOARDING_TIME_RANGE = (30/60, 50/60)  # 30-50 seconds converted to minutes

random.seed(RANDOM_SEED)

# Passenger process
def passenger(env, name, conductor, bus_queue, wait_times, queue_lengths):
    arrival_time = env.now
    queue_lengths.append(len(conductor.queue))
    
    # Single conductor serves passenger
    with conductor.request() as req:
        yield req
        boarding_time = random.uniform(*BOARDING_TIME_RANGE)
        yield env.timeout(boarding_time)
    
    # Boarding bus
    bus = yield bus_queue.get()
    bus['passengers'] += 1
    wait_times.append(env.now - arrival_time)
    yield bus_queue.put(bus)

# Passenger arrival generator
def passenger_arrivals(env, conductor, bus_queue, wait_times, queue_lengths):
    passenger_id = 0
    while True:
        interarrival = random.uniform(2,5)  # 2-5 min
        yield env.timeout(interarrival)
        passenger_id += 1
        env.process(passenger(env, f"Passenger {passenger_id}", conductor, bus_queue, wait_times, queue_lengths))

# Bus departure monitoring
def bus_departure(env, bus_queue, departures):
    while True:
        for bus in bus_queue.items:
            if bus['passengers'] >= BUS_CAPACITY:
                departures.append((bus['id'], env.now))
                bus['passengers'] = 0
        yield env.timeout(5)

# Run Simulation
def run_simulation(num_queues=NUM_QUEUES, num_buses=NUM_BUSES_BASE):
    env = simpy.Environment()
    conductor = simpy.Resource(env, NUM_CONDUCTORS)
    bus_queue = simpy.FilterStore(env)
    
    for i in range(num_buses):
        bus_queue.items.append({'id': i+1, 'passengers': 0})
    
    wait_times = []
    queue_lengths = []
    departures = []
    
    env.process(passenger_arrivals(env, conductor, bus_queue, wait_times, queue_lengths))
    env.process(bus_departure(env, bus_queue, departures))
    env.run(until=SIM_TIME)
    
    results = {
        'average_wait': np.mean(wait_times) if wait_times else 0,
        'max_queue': max(queue_lengths) if queue_lengths else 0,
        'departures': departures,
        'wait_times': wait_times
    }
    return results

# Experiments
scenarios = {
    "Baseline": {'num_queues': 2, 'num_buses': 5},
    "More Queues": {'num_queues': 4, 'num_buses': 5},
    "More Buses": {'num_queues': 2, 'num_buses': 7}
}

all_results = {}
for name, params in scenarios.items():
    print(f"\nRunning scenario: {name}")
    results = run_simulation(**params)
    all_results[name] = results
    print(f"Average wait time: {results['average_wait']:.2f} min")
    print(f"Max queue length: {results['max_queue']}")
    print(f"Total bus departures: {len(results['departures'])}")

# Passenger Wait Time (Histogram)
plt.figure(figsize=(8,5))
for name, res in all_results.items():
    plt.hist(res['wait_times'], bins=20, alpha=0.5, label=name)
plt.xlabel("Wait Time (minutes)")
plt.ylabel("Passengers")
plt.title("Passenger Wait Time Distribution")
plt.legend()
plt.grid(True)
plt.show()

# Queue Length Comparison (Line Plot with Time Series)
plt.figure(figsize=(10,6))
for name, res in all_results.items():
    # Assuming queue_snapshots is recorded at regular intervals in your code
    queue_snapshots = res.get('queue_snapshots', res['wait_times'])  # fallback
    plt.plot(np.arange(len(queue_snapshots)), queue_snapshots, label=name)

plt.xlabel("Time (minutes)")
plt.ylabel("Queue Length")
plt.title("Boarding Queue Length Over Time by Scenario")
plt.legend()
plt.grid(True)
plt.show()


# Bus Departures Over Time (Stacked Area Chart)
plt.figure(figsize=(10,6))
for name, res in all_results.items():
    departures = res['departures']
    if departures:
        bus_ids, times = zip(*departures)
        cumulative_departures = np.arange(1, len(times)+1)
        plt.fill_between(times, cumulative_departures, alpha=0.4, label=name)

plt.xlabel("Time (minutes)")
plt.ylabel("Cumulative Bus Departures")
plt.title("Bus Departures Over Time (Stacked Area) by Scenario")
plt.legend()
plt.grid(True)
plt.show()

