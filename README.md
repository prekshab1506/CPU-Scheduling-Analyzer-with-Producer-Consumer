# CPU-Scheduling-Analyzer-with-Producer-Consumer
This project simulates CPU scheduling using real system processes. It compares algorithms like FCFS, SJF, Priority, and Round Robin based on waiting time, and uses multithreading to handle processes in real time. It also checks fairness and starvation.

CPU Scheduling Analyzer

This project is a complete simulation of CPU scheduling in an operating system, designed to demonstrate how different scheduling algorithms manage processes in real time. It combines concepts of process management, scheduling strategies, multithreading, and performance evaluation into a single integrated system.

Project Overview

The system collects real-time process information from the operating system using the /proc directory. Each process is assigned a burst time (calculated from CPU usage) and a priority value. These processes are then scheduled using different CPU scheduling algorithms, and their performance is analyzed and compared.

The project supports two modes of execution: Manual Analysis and Producer-Consumer Mode, allowing both static and dynamic simulation of scheduling behavior.

Step-by-Step Working

Step 1: Process Collection
The system scans the /proc directory to identify active processes. For each valid process:

* Process ID (PID) is extracted
* CPU time is used to calculate burst time
* A random priority is assigned

A limited number of processes are selected and shuffled to simulate real-world scenarios.

Step 2: Display of Processes
The selected processes are displayed in a tabular format showing:

* PID
* Burst Time
* Priority

This helps visualize the input before scheduling begins.

Step 3: Scheduling Algorithms Implementation

The following CPU scheduling algorithms are implemented:

First Come First Serve
Processes are executed in the order they arrive. It is simple but can lead to long waiting times if a large process comes first.

Shortest Job First
Processes with the smallest burst time are executed first. This usually gives the best average waiting time but may cause starvation of longer processes.

Priority Scheduling
Processes are executed based on priority values. Higher priority processes are scheduled first, which may delay lower priority ones.

Round Robin
Each process is given a fixed time quantum and executed in cycles. This improves fairness and ensures all processes get CPU time.

Each algorithm calculates:

* Waiting time for each process
* Execution timeline for visualization

Step 4: Performance Analysis

After running all algorithms, the system computes:

* Average Waiting Time for each algorithm
* Comparison of all algorithms

The best algorithm is selected based on the lowest average waiting time. A reason is also provided based on workload characteristics.

Step 5: Visualization

The system generates:

* Bar graph comparing algorithm performance
* Gantt chart showing execution order of the best algorithm

These visualizations help in understanding scheduling behavior clearly.

Step 6: Additional Metrics

Fairness Index
Calculated as the difference between maximum and minimum waiting times. It indicates how equally CPU time is distributed.

Starvation Detection
Processes with waiting time above a threshold are identified as starved. This highlights weaknesses in certain algorithms.

Step 7: Producer-Consumer Simulation

In dynamic mode, the system uses multithreading:

Producer Thread
Continuously generates new processes and adds them to a shared buffer.

Consumer Thread
Fetches processes from the buffer and performs scheduling and analysis in batches.

Monitor Thread
Tracks the number of active processes in the system at regular intervals.

This simulates real-time process scheduling in an operating system environment.

Key Features

Real-time process data collection from the system
Implementation of multiple CPU scheduling algorithms
Dynamic simulation using producer-consumer model
Multithreading for concurrent execution
Performance comparison using average waiting time
Fairness analysis and starvation detection
Graphical visualization using bar graphs and Gantt charts
Menu-driven interface for user interaction

Technologies Used

Python
Operating system process interface (/proc)
Threading for concurrency
Queue for synchronization
Matplotlib for visualization

How to Run

Run the Python script
Choose between Manual Analysis or Producer-Consumer Mode
Observe scheduling results, performance comparison, and graphs

Conclusion

This project provides a practical understanding of CPU scheduling by combining theoretical concepts with real-time system data. It demonstrates how different algorithms behave under varying workloads and highlights the trade-offs between efficiency, fairness, and responsiveness. It serves as a comprehensive model for studying process scheduling in operating systems.

SCREENSHOTS:
<img width="635" height="477" alt="Screenshot 2026-04-19 230132" src="https://github.com/user-attachments/assets/6fbfd8a1-45aa-44d8-a7f4-876bd674fe95" />
<img width="1920" height="1128" alt="Screenshot 2026-04-20 163528" src="https://github.com/user-attachments/assets/8ee5e1ea-1ca5-4fe5-9851-4ce5e4617ce9" />
<img width="1920" height="1128" alt="Screenshot 2026-04-20 163548" src="https://github.com/user-attachments/assets/089583d3-8047-45bb-965d-fd4e23bf3905" />
<img width="1920" height="1128" alt="Screenshot 2026-04-20 163557" src="https://github.com/user-attachments/assets/9c048590-f850-4fc4-a5d6-8ec32e06bfea" />
<img width="1920" height="1128" alt="Screenshot 2026-04-20 163611" src="https://github.com/user-attachments/assets/977bf38d-04d5-4682-b864-dfddfb1866b1" />



