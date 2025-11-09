# chart.py

import matplotlib.pyplot as plt
import psutil
import time

# --- Live Pie Chart ---
def getpiechart_live(get_sizes_func, labels, title='Live Pie Chart', refresh_rate=1):
    """
    get_sizes_func: function returning a list of sizes [used, free] dynamically
    labels: list of labels for the pie chart
    refresh_rate: seconds between refresh
    """
    plt.ion()  # Interactive mode
    fig, ax = plt.subplots()
    
    try:
        while True:
            if not plt.fignum_exists(fig.number):
                break  # Stop if user closes the chart window
            sizes = get_sizes_func()
            ax.clear()
            ax.pie(sizes, labels=labels, autopct='%1.1f', startangle=90)
            ax.set_title(title)
            plt.draw()
            plt.pause(refresh_rate)
    except KeyboardInterrupt:
        print("\nLive chart stopped.")
    finally:
        plt.ioff()
        plt.close(fig)


# --- Live Line Chart ---
def getlinechart_live(get_value_func, title='Live Line Chart', xlabel='Time', ylabel='Value', duration=30, interval=1):
    """
    get_value_func: function returning a numeric value (e.g., cpu_percent)
    duration: total time to monitor (seconds)
    interval: refresh interval (seconds)
    """
    plt.ion()
    fig, ax = plt.subplots()
    x_vals, y_vals = [], []

    try:
        for i in range(duration):
            if not plt.fignum_exists(fig.number):
                break
            value = get_value_func()
            x_vals.append(i * interval)
            y_vals.append(value)
            ax.clear()
            ax.plot(x_vals, y_vals, marker='o', color='blue')
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_title(title)
            plt.draw()
            plt.pause(0.1)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nLive line chart stopped.")
    finally:
        plt.ioff()
        plt.close(fig)


# --- Simple Bar Chart ---
def getbarchart(values, labels, title='Bar Chart', ylabel='Values', color=None):
    """
    values: list of numeric values
    labels: list of category labels
    """
    plt.figure()
    if color is None:
        color = ['#FF6347']*len(values)
    plt.bar(labels, values, color=color)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.show()


# --- Pie Chart (Static) ---
def getpiechart(values, labels, title='Pie Chart'):
    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.axis('equal')
    plt.show()
