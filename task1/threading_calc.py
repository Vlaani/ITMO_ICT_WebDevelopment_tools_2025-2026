import time
import threading

tasks_count : int = 16
chunk_size : int = 1000000000 // tasks_count
chunks = [i * chunk_size for i in range(tasks_count + 1)]
chunks[-1] = 1000000001
results = []

def calculate_sum(chunk: int) -> None:
    results.append(sum(range(chunks[chunk], chunks[chunk + 1], 1)))

def main():
    start = time.time()
    threads = []
    for i in range(tasks_count):
        t = threading.Thread(target=calculate_sum, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_sum = sum(results)
    end = time.time()

    print(f"Сумма: {total_sum}")
    print(f"Время работы: {end - start}")

if __name__ == "__main__":
    main()
