import os
import random
import time
import threading
from queue import Queue
import matplotlib.pyplot as plt

monitor_count = 0

# ----------- Shared Buffer -----------
buffer = Queue(maxsize=5)

# ----------- Get Processes -----------
def get_processes(limit=5):
    processes = []

    for pid in os.listdir("/proc"):
        if pid.isdigit():
            try:
                with open(f"/proc/{pid}/stat") as f:
                    data = f.read().split()

                    burst = ((int(data[13]) + int(data[14])) % 50) + 1

                    processes.append({
                        "pid": pid,
                        "arrival": 0,
                        "burst": burst,
                        "priority": random.randint(1, 10)
                    })
            except:
                continue

    random.shuffle(processes)
    return processes[:limit]


# ----------- Display -----------
def display_processes(processes):
    print("\nPID\tBurst\tPriority")
    print("-" * 30)
    for p in processes:
        print(f"{p['pid']}\t{p['burst']}\t{p['priority']}")


# ----------- Algorithms -----------

def fcfs(processes):
    time_now = 0
    waiting = {}
    timeline = []

    for p in processes:
        waiting[p["pid"]] = time_now
        timeline.append((p["pid"], time_now, time_now + p["burst"]))
        time_now += p["burst"]

    return waiting, timeline


def sjf(processes):
    time_now = 0
    waiting = {}
    timeline = []

    for p in sorted(processes, key=lambda x: x["burst"]):
        waiting[p["pid"]] = time_now
        timeline.append((p["pid"], time_now, time_now + p["burst"]))
        time_now += p["burst"]

    return waiting, timeline


def priority_scheduling(processes):
    time_now = 0
    waiting = {}
    timeline = []

    for p in sorted(processes, key=lambda x: x["priority"]):
        waiting[p["pid"]] = time_now
        timeline.append((p["pid"], time_now, time_now + p["burst"]))
        time_now += p["burst"]

    return waiting, timeline


def round_robin(processes, quantum=4):
    time_now = 0
    processes = sorted(processes, key=lambda x: x["arrival"])

    queue = []
    remaining = {p["pid"]: p["burst"] for p in processes}
    waiting = {p["pid"]: 0 for p in processes}
    last_finish = {p["pid"]: p["arrival"] for p in processes}

    timeline = []
    i = 0

    while queue or i < len(processes):
        while i < len(processes) and processes[i]["arrival"] <= time_now:
            queue.append(processes[i])
            i += 1

        if not queue:
            time_now += 1
            continue

        current = queue.pop(0)
        pid = current["pid"]

        waiting[pid] += time_now - last_finish[pid]

        exec_time = min(quantum, remaining[pid])
        timeline.append((pid, time_now, time_now + exec_time))

        time_now += exec_time
        remaining[pid] -= exec_time
        last_finish[pid] = time_now

        while i < len(processes) and processes[i]["arrival"] <= time_now:
            queue.append(processes[i])
            i += 1

        if remaining[pid] > 0:
            queue.append(current)

    return waiting, timeline


# ----------- Metrics -----------
def avg_wait(waiting):
    return sum(waiting.values()) / len(waiting)


def fairness_index(waiting):
    return max(waiting.values()) - min(waiting.values())


def detect_starvation(waiting, threshold=50):
    starved = [pid for pid, wt in waiting.items() if wt > threshold]
    if starved:
        print("⚠️ Starvation Detected:", starved)
    else:
        print("✅ No Starvation")


# ----------- Graph -----------
def show_graph(results):
    names = [r[0] for r in results]
    values = [r[1] for r in results]

    plt.figure()
    plt.bar(names, values)

    plt.title("CPU Scheduling Performance")
    plt.xlabel("Algorithms")
    plt.ylabel("Avg Waiting Time")

    for i, v in enumerate(values):
        plt.text(i, v, f"{v:.2f}", ha='center')

    plt.tight_layout()
    plt.savefig("performance_graph.png")
    plt.close()

    print("Graph saved as performance_graph.png")


# ----------- Gantt Chart -----------
def show_gantt_chart(timeline, title="Gantt Chart"):
    plt.figure()

    for pid, start, end in timeline:
        plt.barh(pid, end - start, left=start)
        plt.text(start + (end - start)/2, pid, pid,
                 ha='center', va='center')

    plt.xlabel("Time")
    plt.ylabel("Processes")
    plt.title(title)

    plt.tight_layout()
    filename = title.replace(" ", "_").lower() + ".png"
    plt.savefig(filename)
    plt.close()

    print(f"Gantt chart saved as {filename}")


# ----------- Analysis -----------
def analyze(processes):
    fcfs_w, fcfs_t = fcfs(processes)
    sjf_w, sjf_t = sjf(processes)
    prio_w, prio_t = priority_scheduling(processes)
    rr_w, rr_t = round_robin(processes)

    results = [
        ("FCFS", avg_wait(fcfs_w)),
        ("SJF", avg_wait(sjf_w)),
        ("Priority", avg_wait(prio_w)),
        ("Round Robin", avg_wait(rr_w))
    ]

    show_graph(results)

    print("\n--- Performance Comparison ---")
    for name, val in results:
        print(f"{name:<12}: {val:.2f}")

    best = min(results, key=lambda x: x[1])
    print(f"\n🔥 Best Algorithm → {best[0]}")

    if best[0] == "FCFS":
        show_gantt_chart(fcfs_t, "FCFS Gantt Chart")
    elif best[0] == "SJF":
        show_gantt_chart(sjf_t, "SJF Gantt Chart")
    elif best[0] == "Priority":
        show_gantt_chart(prio_t, "Priority Gantt Chart")
    else:
        show_gantt_chart(rr_t, "Round Robin Gantt Chart")

    print("\nAdditional Metrics:")
    print("Fairness:", fairness_index(fcfs_w))
    detect_starvation(fcfs_w)


# ----------- Producer -----------
def producer():
    while True:
        processes = get_processes(3)
        for p in processes:
            buffer.put(p)
            print(f"[Producer] Added {p['pid']}")
        time.sleep(2)


# ----------- Consumer -----------
def consumer():
    while True:
        batch = []

        while not buffer.empty():
            batch.append(buffer.get())

        if batch:
            print("\n[Consumer] Scheduling Batch")
            display_processes(batch)
            analyze(batch)

        time.sleep(3)


# ----------- Monitor -----------
def monitor():
    global monitor_count
    while True:
        monitor_count = len(get_processes())
        time.sleep(5)


# ----------- MAIN -----------
threading.Thread(target=monitor, daemon=True).start()

while True:
    print(f"\n[System] Active Processes: {monitor_count}")
    print("\n===== MENU =====")
    print("1. Manual Analysis")
    print("2. Run Producer-Consumer Mode 🔥")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        processes = get_processes()
        display_processes(processes)
        analyze(processes)

    elif choice == "2":
        print("\nStarting Producer-Consumer System...\n")
        threading.Thread(target=producer, daemon=True).start()
        threading.Thread(target=consumer, daemon=True).start()

        while True:
            time.sleep(1)

    elif choice == "3":
        break

    else:
        print("Invalid choice")
