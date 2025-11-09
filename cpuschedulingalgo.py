# CPU Scheduling Algorithms
# Algorithms: FCFS, SJF, SRTF, Round Robin

import random
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# ------------------ FCFS ------------------ #
def fcfs(processes):
    #processes.sort(key=lambda x: x['arrival'])
    processes.sort(key=getfcfsarrival)
    time = 0
    for p in processes:
        if time < p['arrival']:
            time = p['arrival']
        p['start'] = time
        p['finish'] = time + p['burst']
        p['waiting'] = p['start'] - p['arrival']
        p['turnaround'] = p['finish'] - p['arrival']
        time = p['finish']
    return processes
    
def getfcfsarrival(x):
    return x['arrival']

# ------------------ SJF (Non-Preemptive) ------------------ #
def sjf(processes):
    n = len(processes)
    completed = 0
    time = 0
    ready = []
    result = []
    while completed < n:
        for p in processes:
            if p not in ready and p['arrival'] <= time and 'finish' not in p:
                ready.append(p)
        if ready:
            ready.sort(key=getsjfburst)
            p = ready.pop(0)
            if time < p['arrival']:
                time = p['arrival']
            p['start'] = time
            p['finish'] = time + p['burst']
            p['waiting'] = p['start'] - p['arrival']
            p['turnaround'] = p['finish'] - p['arrival']
            time = p['finish']
            completed += 1
            result.append(p)
        else:
            time += 1
    return result
    
def getsjfburst(x):
    return x['burst']

# ------------------ SRTF (Preemptive SJF) ------------------ #
def srtf(processes):
    n = len(processes)
    remaining = [p['burst'] for p in processes]
    complete = 0
    time = 0
    minm = float('inf')
    shortest = None
    check = False

    while complete != n:
        for j in range(n):
            if (processes[j]['arrival'] <= time and 
                remaining[j] < minm and remaining[j] > 0):
                minm = remaining[j]
                shortest = j
                check = True
        if not check:
            time += 1
            continue

        remaining[shortest] -= 1
        minm = remaining[shortest] if remaining[shortest] > 0 else float('inf')

        if remaining[shortest] == 0:
            complete += 1
            check = False
            finish_time = time + 1
            processes[shortest]['finish'] = finish_time
            processes[shortest]['waiting'] = (finish_time - 
                processes[shortest]['burst'] - processes[shortest]['arrival'])
            if processes[shortest]['waiting'] < 0:
                processes[shortest]['waiting'] = 0
        time += 1

    for p in processes:
        p['turnaround'] = p['burst'] + p['waiting']
    return processes

# ------------------ Round Robin ------------------ #
def round_robin(processes, quantum):
    n = len(processes)
    time = 0
    completed = set()
    queue = []
    queue_set = set()  # for O(1) lookup
    remaining = {p['pid']: p['burst'] for p in processes}
    start_time = {}
    finish_time = {}

    while len(completed) < n:
        # Add newly arrived processes
        for p in processes:
            if p['arrival'] <= time and p['pid'] not in completed and p['pid'] not in queue_set:
                queue.append(p)
                queue_set.add(p['pid'])
        
        if not queue:
            # Jump to next arrival if queue empty
            next_arrival = min([p['arrival'] for p in processes if p['pid'] not in completed], default=None)
            if next_arrival is not None and next_arrival > time:
                time = next_arrival
            else:
                time += 1
            continue

        p = queue.pop(0)
        #queue_set.remove(p['pid'])

        if p['pid'] not in start_time:
            start_time[p['pid']] = time

        exec_time = min(quantum, remaining[p['pid']])
        remaining[p['pid']] -= exec_time
        time += exec_time

        # Add any new arrivals during execution
        for new_p in processes:
            if new_p['arrival'] <= time and new_p['pid'] not in completed and new_p['pid'] not in queue_set:
                queue.append(new_p)
                queue_set.add(new_p['pid'])

        if remaining[p['pid']] == 0:
            finish_time[p['pid']] = time
            completed.add(p['pid'])
            queue_set.remove(p['pid'])
        else:
            queue.append(p)
            queue_set.add(p['pid'])

    # Compute metrics
    for p in processes:
        p['finish'] = finish_time[p['pid']]
        p['turnaround'] = p['finish'] - p['arrival']
        p['waiting'] = p['turnaround'] - p['burst']
        p['start'] = start_time[p['pid']]

    return processes


# ------------------ Helper to Display Results ------------------ #
def display(title, processes):
    print(f"\n--- {title} ---")
    table = PrettyTable(["PID", "Arrival", "Burst", "Start", "Finish", "Waiting", "Turnaround"])
    total_wt = total_tat = 0
    for p in processes:
        table.add_row([p['pid'], p['arrival'], p['burst'],
                       p.get('start', '-'), p['finish'],
                       p['waiting'], p['turnaround']])
        total_wt += p['waiting']
        total_tat += p['turnaround']
    print(table)
    print(f"Average Waiting Time: {total_wt/len(processes):.2f}")
    print(f"Average Turnaround Time: {total_tat/len(processes):.2f}")

#-------------------Draw Gant Chart -------------------#
def draw_gantt_chart(title, processes, preemptive=False):
    print(f"\nGenerating Gantt Chart for {title}...")
    fig, ax = plt.subplots(figsize=(8, 3))
    colors = {}

    # Assign random colors to each process
    for p in processes:
        colors[p['pid']] = (random.random(), random.random(), random.random())

    # For non-preemptive algorithms (FCFS, SJF)
    if not preemptive:
        current_y = 10
        for p in processes:
            ax.barh(10, p['burst'], left=p['start'], color=colors[p['pid']], edgecolor='black')
            ax.text(p['start'] + p['burst']/2 - 0.3, 10, p['pid'], color='white', fontsize=10, fontweight='bold')
        ax.set_yticks([])
        ax.set_xlabel("Time")
        ax.set_title(title)
        plt.show()
        return

    # For preemptive (SRTF, RR)
    # Build a list of (process_id, start_time, end_time)
    timeline = []
    time = 0
    remaining = [p['burst'] for p in processes]
    complete = 0
    n = len(processes)
    
    def getremainingtime(process):
        return remaining[processes.index(process)]

    while complete != n:
        ready = [p for p in processes if p['arrival'] <= time and remaining[processes.index(p)] > 0]
        if not ready:
            time += 1
            continue

        if title == "SRTF (Preemptive SJF)":
            
            current = min(ready, key=getremainingtime)

        elif title == "Round Robin":
            # Simplified RR for visualization
            quantum = 2
            current = ready[0]
        else:
            current = ready[0]

        idx = processes.index(current)
        exec_time = 1 if title == "SRTF (Preemptive SJF)" else min(2, remaining[idx])
        start_time = time
        time += exec_time
        end_time = time
        remaining[idx] -= exec_time

        timeline.append((current['pid'], start_time, end_time))
        if remaining[idx] == 0:
            complete += 1

    # Merge consecutive same-process intervals
    merged = []
    for pid, start, end in timeline:
        if merged and merged[-1][0] == pid:
            merged[-1] = (pid, merged[-1][1], end)
        else:
            merged.append((pid, start, end))

    for pid, start, end in merged:
        ax.barh(10, end - start, left=start, color=colors[pid], edgecolor='black')
        ax.text(start + (end - start)/2 - 0.3, 10, pid, color='white', fontsize=10, fontweight='bold')

    ax.set_yticks([])
    ax.set_xlabel("Time")
    ax.set_title(title)
    plt.show()

#-------------------Draw Gant Chart - Round Robin -------------------#
def draw_gantt_chart_rr(title, processes, preemptive=False, quantum=2):
    print(f"\nGenerating Gantt Chart for {title}...")
    fig, ax = plt.subplots(figsize=(8, 3))
    colors = {}

    for p in processes:
        colors[p['pid']] = (random.random(), random.random(), random.random())

    # Non-preemptive algorithms (FCFS, SJF)
    if not preemptive:
        for p in processes:
            ax.barh(10, p['burst'], left=p['start'], color=colors[p['pid']], edgecolor='black')
            ax.text(p['start'] + p['burst']/2 - 0.3, 10, p['pid'], color='white', fontsize=10, fontweight='bold')
        ax.set_yticks([])
        ax.set_xlabel("Time")
        ax.set_title(title)
        plt.show()
        return

    # Preemptive: SRTF or Round Robin
    timeline = []
    time = 0
    n = len(processes)
    remaining = {p['pid']: p['burst'] for p in processes}
    completed = set()
    queue = []
    queue_set = set()

    def get_remaining_time(process):
        return remaining[process['pid']]

    while len(completed) < n:
        # Add newly arrived
        for p in processes:
            if p['arrival'] <= time and p['pid'] not in completed and p['pid'] not in queue_set:
                queue.append(p)
                queue_set.add(p['pid'])

        if not queue:
            time += 1
            continue

        if title == "SRTF (Preemptive SJF)":
            # choose shortest remaining
            current = min(queue, key=get_remaining_time)
            #if current['pid'] in queue_set:
            #    queue_set.remove(current['pid'])
            queue.remove(current)
            queue_set.remove(current['pid'])
            exec_time = 1

        elif title == "Round Robin":
            current = queue.pop(0)
            #if current['pid'] in queue_set:
            #    queue_set.remove(current['pid'])

            exec_time = min(quantum, remaining[current['pid']])
        else:
            current = queue.pop(0)
            if current['pid'] in queue_set:
                queue_set.remove(current['pid'])

            exec_time = 1

        start_time = time
        time += exec_time
        end_time = time
        remaining[current['pid']] -= exec_time
        timeline.append((current['pid'], start_time, end_time))

        # Add any newly arrived processes during execution
        for p in processes:
            if p['arrival'] <= time and p['pid'] not in completed and p['pid'] not in queue_set and remaining[p['pid']] > 0:
                queue.append(p)
                queue_set.add(p['pid'])

        if remaining[current['pid']] == 0:
            completed.add(current['pid'])
        elif title == "Round Robin":
            queue.append(current)
            queue_set.add(current['pid'])

    # Merge consecutive same-process intervals
    merged = []
    for pid, start, end in timeline:
        if merged and merged[-1][0] == pid:
            merged[-1] = (pid, merged[-1][1], end)
        else:
            merged.append((pid, start, end))

    for pid, start, end in merged:
        ax.barh(10, end - start, left=start, color=colors[pid], edgecolor='black')
        ax.text(start + (end - start)/2 - 0.3, 10, pid, color='white', fontsize=10, fontweight='bold')

    ax.set_yticks([])
    ax.set_xlabel("Time")
    ax.set_title(title)
    plt.show()


def performcpuscheduling():
    print("_____________PERFORMING______________")
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        pid = f"P{i+1}"
        arrival = int(input(f"Arrival time for {pid}: "))
        burst = int(input(f"Burst time for {pid}: "))
        processes.append({'pid': pid, 'arrival': arrival, 'burst': burst})
    
    quantum = int(input("Enter time quantum for Round Robin: "))

    display("FCFS", fcfs([p.copy() for p in processes]))
    draw_gantt_chart_rr("FCFS", fcfs([p.copy() for p in processes]))
    
    display("SJF (Non-preemptive)", sjf([p.copy() for p in processes]))
    draw_gantt_chart_rr("SJF (Non-preemptive)", sjf([p.copy() for p in processes]))
    
    display("SRTF (Preemptive SJF)", srtf([p.copy() for p in processes]))
    draw_gantt_chart_rr("SRTF (Preemptive SJF)", srtf([p.copy() for p in processes]), preemptive=True)
    
    rr_result = round_robin([p.copy() for p in processes], quantum)
    display("Round Robin", rr_result)
    draw_gantt_chart_rr("Round Robin", rr_result, preemptive=True, quantum=quantum)

    #display("Round Robin", round_robin([p.copy() for p in processes], quantum))
    #draw_gantt_chart("Round Robin", round_robin([p.copy() for p in processes], quantum), preemptive=True)
    #draw_gantt_chart_rr("Round Robin", round_robin([p.copy() for p in processes], quantum), preemptive=True, quantum=quantum)


