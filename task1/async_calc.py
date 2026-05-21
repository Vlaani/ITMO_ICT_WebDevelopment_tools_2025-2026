import time
import asyncio

tasks_count : int = 16
chunk_size : int = 1000000000 // tasks_count
chunks = [i * chunk_size for i in range(tasks_count + 1)]
chunks[-1] = 1000000001

async def calculate_sum(chunk: int) -> int:
    return sum(range(chunks[chunk], chunks[chunk + 1], 1))

async def main():
    start = time.time()
    tasks = [calculate_sum(i) for i in range(0, tasks_count)]
    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    end = time.time()
    print(f"Сумма: {total_sum}")
    print(f"Время работы: {end - start}")

if __name__ == "__main__":
    asyncio.run(main())