# Makumbura Multimodal Center Simulation

## Overview

This python simulation based models passenger arrivals, ticketing and bus bording at Makumbura Multimodal Center, Kottawa. This case study is focusing on the long ques in Fridays, high passanger arrival for busses in Makumbura Multimodal Center, Kottawa. Im using a Simpy for an simulation code to track waiting time, queue length and serve passengers on a first-come-first-served basis.

The simulation allows for parameter variations like number of counters, buses, bus capacity, boarding time to test different scenarios and performance improvements.

## Requirements

- You must install Python 3.x
- pip install simpy numpy matplotlib
- Libraries using are simpy, numpy, matplotlib

## Simulation Parameters

RANDOM_SEED = 42
SIM_TIME = Total simulation time in minutes
NUM_CONDUCTORS = Number of Conductors
NUM_QUEUES = Number of queues
NUM_BUSES_BASE = Number of buses available
BUS_CAPACITY = Maximum passengers per bus
BOARDING_TIME_RANGE = (30/60, 50/60) # 30-50 seconds converted to minutes

## Run Simulation

Open a Python environment and run the script:

python multimodal_simulation.py

The simulation will automatically run three scenarios:

Baseline: Default counters and buses

More Counters: Increase ticket counters

More Buses: Increase number of buses

## Output Metrics

After running, the script prints:

- Average passenger wait time
- Maximum queue length at bus boarding
- Total bus departures

Visualizations

- Histogram of passenger wait times by scenario
- Line chart of boarding queue lengths over time
- Area chart of cumulative bus departures over time

## Customizing Scenarios

You can easily modify the scenarios by editing the scenarios dictionary:

scenarios = {
"Baseline": {'num_queues': 2, 'num_buses': 5},
"More Queues": {'num_queues': 4, 'num_buses': 5},
"More Buses": {'num_queues': 2, 'num_buses': 7},
}

Or you can run the simulation manually with different parameters:

<results = run_simulation(num_queues=3, num_buses=6)>

## Notes

- The simulation uses a time-dependent arrival rate to model Friday peak congestion (5–7 PM).
- You can expand the simulation by adding more routes, bus priorities, or dynamic boarding times.
