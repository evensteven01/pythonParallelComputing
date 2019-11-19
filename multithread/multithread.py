from collections import Counter
import threading

n = 0
lock = threading.Lock()

def unsafe():
    global n
    n += 1

def safe():
    global n
    with lock:
        n += 1

def run(run_safe=True):
    global n
    n = 0
    func = safe if run_safe else unsafe
    threads = []
    for i in range(100):
        t = threading.Thread(target=func)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return n

safe_or_not = [*[False]*20, *[True]*20]

results = Counter()
for mode in safe_or_not:
    res = run(run_safe=mode)
    mode_name = 'Safe' if mode else 'Unsafe'
    mode_result = f"{mode_name}{'=' if res==100 else '!'}=100"
    results.update([mode_result])

print(f'Results: {results}')
