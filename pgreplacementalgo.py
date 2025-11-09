# ============================================================
#   PAGE REPLACEMENT ALGORITHMS
#   Includes:
#     - FIFO, LRU, Optimal Page Replacement
# ============================================================

from colorama import Fore, Style, init
init(autoreset=True)


def fifo_algorithm(pages, noframes):
    flist = []
    page_faults = 0
    print("\n" + Fore.CYAN + "--- FIFO Page Replacement Result---")
    for page in pages:
        if page not in flist:
            if len(flist) < noframes:
                flist.append(page)
            else:
                flist.pop(0)
                flist.append(page)
            page_faults += 1
            print(Fore.RED + f"Page {page} caused a FAULT! Frame : {flist}")
        else:
            print(Fore.GREEN + f"Page {page} HIT! Frame state: {flist}")
    print(Fore.YELLOW + f"Total Page Faults: {page_faults}\n")

def lru_algorithm(pages, noframes):
    flist = []
    page_faults = 0
    print(Fore.CYAN + "--- LRU Page Replacement Result---")
    for page in pages:
        if page not in flist:
            if len(flist) < noframes:
                flist.append(page)
            else:
                flist.pop(0)
                flist.append(page)
            page_faults += 1
            print(Fore.RED + f"Page {page} caused a FAULT! Frame : {flist}")
        else:
            flist.remove(page)
            flist.append(page)
            print(Fore.GREEN + f"Page {page} HIT! Frame state: {flist}")
    print(Fore.YELLOW + f"Total Page Faults: {page_faults}\n")

def optimal_algorithm(pages, noframes):
    page_faults = 0
    flist = []
    print(Fore.CYAN + "--- Optimal Page Replacement Result---")
    for i in range(len(pages)):
        if pages[i] not in flist:
            if len(flist) < noframes:
                flist.append(pages[i])
            else:
                farthest = i
                index_to_replace = -1
                for j in range(len(flist)):
                    try:
                        next_use = pages[i+1:].index(flist[j])
                    except ValueError:
                        index_to_replace = j
                        break
                    if next_use > farthest:
                        farthest = next_use
                        index_to_replace = j
                flist[index_to_replace] = pages[i]
            page_faults += 1
            print(Fore.RED + f"Page {pages[i]} caused a FAULT! Frame state: {flist}")
        else:
            print(Fore.GREEN + f"Page {pages[i]} HIT! Frame state: {flist}")
    print(Fore.YELLOW + f"Total Page Faults: {page_faults}\n")


def performpgreplacement():
    # --- Input from user ---
    print(Fore.CYAN + "\n---- PAGE REPLACEMENT ALGORITHMS INPUT----")
    pages = list(map(int, input("Enter page references (space-separated): ").split()))
    noframes = int(input("Enter number of frames: "))

    fifo_algorithm(pages, noframes)
    lru_algorithm(pages, noframes)
    optimal_algorithm(pages, noframes)

    print(Fore.MAGENTA + Style.BRIGHT + "========== END OF PAGE REPLACEMENT ALGORITHM ==========")

if __name__ == "__main__":
    # --- Input from user ---
    print(Fore.CYAN + "\n---- PAGE REPLACEMENT ALGORITHMS INPUT----")
    pages = list(map(int, input("Enter page references (space-separated): ").split()))
    noframes = int(input("Enter number of frames: "))

    fifo_algorithm(pages, noframes)
    fifo_algorithm(pages, noframes)
    optimal_algorithm(pages, noframes)

    print(Fore.MAGENTA + Style.BRIGHT + "========== END OF PAGE REPLACEMENT ALGORITHM ==========")

