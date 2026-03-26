import time, statistics, csv, os

class BenchmarkManager:
    def __init__(self):
        self.results = []

    def run_benchmark(self, db_name, query_name, func, *args):
        print(f"Esecuzione benchmark: {db_name} - {query_name}")

        start = time.perf_counter()
        res = func(*args)
        cold_time = (time.perf_counter() - start) * 1000

        warm_times = []
        for i in range(35):
            start = time.perf_counter()
            func(*args)
            warm_times.append((time.perf_counter() - start) * 1000)
        
        self.results.append({
            "db": db_name,
            "test": query_name,
            "cold_ms": cold_time,
            "warm_avg_ms": statistics.mean(warm_times),
            "warm_std_ms": statistics.stdev(warm_times) if len(warm_times) > 1 else 0
        })

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        keys = self.results[0].keys()
        with open(path, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.results)