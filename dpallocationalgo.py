# ============================================================
#   DYNAMIC PARTITION ALLOCATION SIMULATOR
#   Includes:
#     - First Fit, Best Fit, Worst Fit
# ============================================================

from colorama import Fore, Style, init
init(autoreset=True)

def first_fit(blocksize, processsize):
    allocation = [-1] * len(processsize)
    for i in range(len(processsize)):
        for j in range(len(blocksize)):
            if blocksize[j] >= processsize[i]:
                allocation[i] = j
                blocksize[j] -= processsize[i]
                break
    return allocation

def best_fit(blocksize, processsize):
    allocation = [-1] * len(processsize)
    for i in range(len(processsize)):
        best_idx = -1
        for j in range(len(blocksize)):
            if blocksize[j] >= processsize[i]:
                if best_idx == -1 or blocksize[j] < blocksize[best_idx]:
                    best_idx = j
        if best_idx != -1:
            allocation[i] = best_idx
            blocksize[best_idx] -= processsize[i]
    return allocation

def worst_fit(blocksize, processsize):
    allocation = [-1] * len(processsize)
    for i in range(len(processsize)):
        worst_idx = -1
        for j in range(len(blocksize)):
            if blocksize[j] >= processsize[i]:
                if worst_idx == -1 or blocksize[j] > blocksize[worst_idx]:
                    worst_idx = j
        if worst_idx != -1:
            allocation[i] = worst_idx
            blocksize[worst_idx] -= processsize[i]
    return allocation

def print_allocation(processsize, allocation):
    print("\nProcess No.\tProcess Size\tBlock No.")
    for i in range(len(processsize)):
        print(f"{i+1}\t\t{processsize[i]}\t\t", end="")
        if allocation[i] != -1:
            print(Fore.GREEN + str(allocation[i] + 1))
        else:
            print(Fore.RED + "Not Allocated")


def performdpallocation():
    print(Fore.CYAN + "---- Dynamic Partition Allocation ----")
    noblocks = int(input("Enter number of memory blocks: "))
    blocksize = list(map(int, input("Enter block sizes (space-separated): ").split()))

    noprocesses = int(input("Enter number of processes: "))
    processsize = list(map(int, input("Enter process sizes (space-separated): ").split()))
    
    print(Fore.CYAN + "---- Dynamic Partition Allocation ----")
    
    print(Fore.BLUE + "\n---- FIRST FIT RESULT----")
    print_allocation(processsize, first_fit(blocksize.copy(), processsize))

    print(Fore.BLUE + "\n---- BEST FIT RESULT----")
    print_allocation(processsize, best_fit(blocksize.copy(), processsize))

    print(Fore.BLUE + "\n---- WORST FIT RESULT----")
    print_allocation(processsize, worst_fit(blocksize.copy(), processsize))
    
    print(Fore.MAGENTA + Style.BRIGHT + "========== END OF Dynamic Partition Allocation ==========")


if __name__ == "__main__":
    print(Fore.CYAN + "---- Dynamic Partition Allocation ----")
    noblocks = int(input("Enter number of memory blocks: "))
    blocksize = list(map(int, input("Enter block sizes (space-separated): ").split()))

    noprocesses = int(input("Enter number of processes: "))
    processsize = list(map(int, input("Enter process sizes (space-separated): ").split()))
    
    print(Fore.CYAN + "---- Dynamic Partition Allocation ----")
    
    print(Fore.BLUE + "\n---- FIRST FIT RESULT----")
    print_allocation(processsize, first_fit(blocksize.copy(), processsize))

    print(Fore.BLUE + "\n---- BEST FIT RESULT----")
    print_allocation(processsize, best_fit(blocksize.copy(), processsize))

    print(Fore.BLUE + "\n---- WORST FIT RESULT----")
    print_allocation(processsize, worst_fit(blocksize.copy(), processsize))
    
    print(Fore.MAGENTA + Style.BRIGHT + "========== END OF Dynamic Partition Allocation ==========")
