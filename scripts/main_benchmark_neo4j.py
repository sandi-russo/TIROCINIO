import os, logging
from dotenv import load_dotenv
from database.neo4j_manager import Neo4jManager
from benchmark_manager import BenchmarkManager
from analytics import neo4j_gds_analytics as n_an

logging.getLogger('neo4j').setLevel(logging.ERROR)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


TEST_NODES = {
    25:  ("n0", "n22948051"),
    50:  ("n0", "n22948051"),
    75:  ("n0", "n22948051"),
    100: ("n0", "n22948051")
}

SCALES = [25, 50, 75, 100]

def main():
    nm = Neo4jManager()
    bm = BenchmarkManager()

    for scale in SCALES:
        print(f"\nScala {scale}%")
        n_graph = nm.project_subgraph(scale)
        src, dst = TEST_NODES[scale]

        print(f"Test Dijkstra...")
        try:
            bm.run_benchmark("Neo4j", f"ShortestPath_{scale}", n_an.run_shortest_path_neo4j, nm.driver, n_graph, src, dst)
        except Exception as e: print(f"Errore ShortestPath: {e}")

        try:
            bm.run_benchmark("Neo4j", f"PageRank_{scale}", n_an.run_pagerank_neo4j, nm.driver, n_graph)
        except Exception as e: print(f"Errore PageRank: {e}")

        try:
            bm.run_benchmark("Neo4j", f"WCC_{scale}", n_an.run_wcc_neo4j, nm.driver, n_graph)
        except Exception as e: print(f"Errore WCC: {e}")

        nm.drop_projection(n_graph)

    os.makedirs("results", exist_ok=True)
    bm.save("results/benchmark_neo4j.csv")
    nm.close()
    print("\Benchmark completato!")

if __name__ == "__main__":
    main()