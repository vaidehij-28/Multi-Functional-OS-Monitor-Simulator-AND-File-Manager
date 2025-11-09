import os
import random
import matplotlib
matplotlib.use('TkAgg')  # Use Tkinter for compatibility
import matplotlib.pyplot as plt

# ------------------------------
# Configuration
# ------------------------------
PATH = "E:\Documents"  # Change this to your USB or test directory
BLOCK_SIZE = 1024  # 1 KB per block
DISK_SIZE = 2000    # Simulated disk of 500 blocks
DISPLAY_TIME = 10   # seconds to show each comparison
FILE_LIMIT = 50

# ------------------------------
# Scanning Drive/USB files
# ------------------------------
def perfromscanning(path):
    print("--- Scanning USB drive files ---")
    files = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            filepath = os.path.join(root, f)
            try:
                size = os.path.getsize(filepath)
                files.append((f, size))
            except:
                continue
    #taking a random sample if too many files present 
    if len(files) > FILE_LIMIT:
        print(f"Found {len(files)} files, sampling {FILE_LIMIT} randomly for simulation.")
        files = random.sample(files, FILE_LIMIT)
    if not files:
        # Fallback: generate simulated files manually if data not present
        files = [(f"file_{i}", random.randint(5, 50) * BLOCK_SIZE) for i in range(10)]
    files.sort(key=lambda x: x[1])
    print(f"Scanned {len(files)} files.")
    return files


# ------------------------------
# Fragmenting
# ------------------------------
def fragment_disk(files, disk_size):
    print("--- Creating fragmented disk ---")
    disk = ['F'] * disk_size
    for idx, (name, size) in enumerate(files):
        blocks_needed = size // BLOCK_SIZE + 1

        #If file is too big skip it to fit the simulated disk
        if blocks_needed >= disk_size:
            print(f"Skipping file {name} (too large: {blocks_needed} blocks)")
            continue

        placed = False
        for _ in range(50):  # up to 50 attempts to place
            start = random.randint(0, disk_size - blocks_needed)
            if all(b == 'F' for b in disk[start:start + blocks_needed]):
                disk[start:start + blocks_needed] = [str(idx)] * blocks_needed
                placed = True
                break

        if not placed:
            print(f"Could not place {name}, skipping...")

    print("Fragmentation complete.")
    return disk


def fragmentation_ratio(disk):
    total_blocks = len(disk)
    free_segments = sum(1 for i in range(1, total_blocks) if disk[i] == 'F' and disk[i-1] != 'F')
    return (free_segments / total_blocks) * 100
    
    
# ------------------------------
# Visualization - individual
# ------------------------------
def plotChanges(before, after, title_before, title_after, main_title):
    colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#9370DB', '#FF69B4',
              '#00CED1', '#FFA500', '#B22222', '#ADFF2F']
    unique = sorted(list(set([b for b in before + after if b != 'F'])))
    color_map = {b: colors[i % len(colors)] for i, b in enumerate(unique)}
    color_map['F'] = 'white'

    frag_before = fragmentation_ratio(before)
    frag_after = fragmentation_ratio(after)

    fig, axs = plt.subplots(1, 2, figsize=(18, 6))
    plt.suptitle(f"{main_title}\nFragmentation ↓ {frag_before:.2f}% → {frag_after:.2f}%", fontsize=13, fontweight='bold')

    for ax, disk, subtitle in zip(axs, [before, after], [title_before, title_after]):
        ax.bar(range(len(disk)), [1]*len(disk),
               color=[color_map.get(b, 'gray') for b in disk],
               edgecolor='black', linewidth=0)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(subtitle, fontsize=10, fontweight='bold')

    plt.tight_layout(rect=[0, 0, 1, 0.9])
    #plt.pause(DISPLAY_TIME)
    plt.show(block=True)
    # Wait for user input
    #input("Press Enter to continue to the next chart...")

    plt.close()

# ------------------------------
# New: Fragmentation Summary Chart
# ------------------------------
def plot_summary_chart(disk_original, disk_simple, disk_best, disk_worst):
    """Display a bar chart comparing fragmentation percentages."""
    frag_values = [
        fragmentation_ratio(disk_original),
        fragmentation_ratio(disk_simple),
        fragmentation_ratio(disk_best),
        fragmentation_ratio(disk_worst)
    ]
    labels = ['Original', 'Simple', 'Best-Fit', 'Worst-Fit']
    colors = ['#FF6347', '#4682B4', '#32CD32', '#9370DB']

    plt.figure(figsize=(18, 6))
    plt.bar(labels, frag_values, color=colors, edgecolor='black')
    plt.ylabel("Fragmentation (%)")
    plt.title("Fragmentation Comparison Across Algorithms", fontsize=12, fontweight='bold')
    for i, v in enumerate(frag_values):
        plt.text(i, v + 0.3, f"{v:.2f}%", ha='center', fontsize=9, fontweight='bold')
    plt.tight_layout()
    plt.show()

# ------------------------------
# Visualization-all side by side
# ------------------------------
def plotAllCompactions(before, simple, best, worst):
    colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#9370DB', '#FF69B4',
              '#00CED1', '#FFA500', '#B22222', '#ADFF2F']
    
    unique = sorted(list(set(before + simple + best + worst)))
    unique = [b for b in unique if b != 'F']
    color_map = {b: colors[i % len(colors)] for i, b in enumerate(unique)}
    color_map['F'] = 'white'

    fig, axs = plt.subplots(1, 4, figsize=(18, 6))
    titles = ["Fragmented", "Simple", "Best-Fit", "Worst-Fit"]

    for ax, disk, title in zip(axs, [before, simple, best, worst], titles):
        ax.bar(range(len(disk)), [1]*len(disk),
               color=[color_map.get(b, 'gray') for b in disk],
               edgecolor='black', linewidth=0)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(title, fontsize=10, fontweight='bold')

    #Add a shared color legend for file IDs
    handles = [plt.Line2D([0], [0], color=color_map[b], lw=6) for b in unique[:10]]
    labels = [f"File {b}" for b in unique[:10]]
    fig.legend(handles, labels, loc='upper center', ncol=min(5, len(unique[:10])),
               bbox_to_anchor=(0.5, 1.3), fontsize=9)

    plt.tight_layout()
    plt.suptitle("All Compactions Side-by-Side", fontsize=13, fontweight='bold')
    plt.show()




# ------------------------------
# Compaction Algorithms
# ------------------------------
def simple_compaction(disk):
    new_disk = [b for b in disk if b != 'F']
    new_disk += ['F'] * (len(disk) - len(new_disk))
    return new_disk

def best_fit_compaction(disk):
    files_blocks = {}
    for i, b in enumerate(disk):
        if b != 'F':
            files_blocks.setdefault(b, []).append(i)
    new_disk = ['F'] * len(disk)
    index = 0
    for b in sorted(files_blocks.keys(), key=lambda x: len(files_blocks[x])):
        for _ in files_blocks[b]:
            new_disk[index] = b
            index += 1
    return new_disk

def worst_fit_compaction(disk):
    files_blocks = {}
    for i, b in enumerate(disk):
        if b != 'F':
            files_blocks.setdefault(b, []).append(i)
    new_disk = ['F'] * len(disk)
    index = 0
    for b in sorted(files_blocks.keys(), key=lambda x: -len(files_blocks[x])):
        for _ in files_blocks[b]:
            new_disk[index] = b
            index += 1
    return new_disk


def performCompaction():
   files = perfromscanning(PATH)
   
   disk_original = fragment_disk(files, DISK_SIZE)

   # Simple Compaction
   disk_simple = simple_compaction(disk_original)
   plotChanges(disk_original, disk_simple, "Before", "After", "Simple Compaction")

   # Best-Fit Compaction
   disk_best = best_fit_compaction(disk_original)
   plotChanges(disk_original, disk_best, "Before", "After", "Best-Fit Compaction")

   # Worst-Fit Compaction
   disk_worst = worst_fit_compaction(disk_original)
   plotChanges(disk_original, disk_worst, "Before", "After", "Worst-Fit Compaction")

   # Finally, show all four side-by-side
   plotAllCompactions(disk_original, disk_simple, disk_best, disk_worst)
    
   #plot_summary_chart(disk_original, disk_simple, disk_best, disk_worst)
    
   print("Side-by-side compaction visualization complete.") 

# ------------------------------
# Step 5: Run simulation
# ------------------------------
def main():
    files = perfromscanning(PATH)

    disk_original = fragment_disk(files, DISK_SIZE)

    # Simple Compaction
    disk_simple = simple_compaction(disk_original)
    plotChanges(disk_original, disk_simple, "Before", "After", "Simple Compaction")

    # Best-Fit Compaction
    disk_best = best_fit_compaction(disk_original)
    plotChanges(disk_original, disk_best, "Before", "After", "Best-Fit Compaction")

    # Worst-Fit Compaction
    disk_worst = worst_fit_compaction(disk_original)
    plotChanges(disk_original, disk_worst, "Before", "After", "Worst-Fit Compaction")

    # Finally, show all four side-by-side
    plotAllCompactions(disk_original, disk_simple, disk_best, disk_worst)
    
    #plot_summary_chart(disk_original, disk_simple, disk_best, disk_worst)
    
    print("Side-by-side compaction visualization complete.")

if __name__ == "__main__":
    main()
