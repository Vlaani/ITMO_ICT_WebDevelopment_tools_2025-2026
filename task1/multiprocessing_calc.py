import time
import multiprocessing

tasks_count : int = 16
chunk_size : int = 1000000000 // tasks_count
chunks = [i * chunk_size for i in range(tasks_count + 1)]
chunks[-1] = 1000000001

def calculate_sum(chunk: int, queue) -> None:
    queue.put(sum(range(chunks[chunk], chunks[chunk + 1], 1)))

def main():
    start = time.time()
    processes = []
    queue = multiprocessing.Queue()
    for i in range(tasks_count):
        p = multiprocessing.Process(target=calculate_sum, args=(i, queue))
        processes.append(p)
        p.start()

    results = []
    for _ in range(tasks_count):
        results.append(queue.get())

    for proc in processes:
        proc.join()

    total_sum = sum(results)
    end = time.time()

    print(f"Сумма: {total_sum}")
    print(f"Время работы: {end - start}")

if __name__ == "__main__":
    main()