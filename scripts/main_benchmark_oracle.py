import os, logging
from dotenv import load_dotenv
from database.oracle_manager import OracleManager
from benchmark_manager import BenchmarkManager
from analytics import oracle_pgx_analytics as o_an

logging.getLogger('oracle').setLevel(logging.ERROR)
logging.getLogger('pypgx').setLevel(logging.ERROR)
logging.getLogger('opg4py').setLevel(logging.ERROR)

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

TEST_NODES = {
    25:  ("n0", "n22948051"),
    50:  ("n0", "n22948051"),
    75:  ("n0", "n22948051"),
    100: ("n0", "n22948051")
}

SCALES = [25, 50, 75, 100]

def main():
    om = OracleManager()
    bm = BenchmarkManager()

    session = om.connect_pgx()
    if not session:
        return

    for scale in SCALES:
        print(f"Scala {scale}%")

        o_graph = om.load_subgraph(scale)
        if not o_graph:
            continue

        src, dst = TEST_NODES[scale]

        try:
            bm.run_benchmark("Oracle", f"ShortestPath_{scale}", o_an.run_shortest_path_oracle, session, o_graph, src, dst)
            bm.run_benchmark("Oracle", f"PageRank_{scale}", o_an.run_pagerank_oracle, session, o_graph)
            bm.run_benchmark("Oracle", f"WCC_{scale}", o_an.run_wcc_oracle, session, o_graph)
        except Exception as e:
            print(f"Errore durante i test: {e}")
        finally:
            print(f"Svuotamento RAM per scala {scale}%...")
            o_graph.destroy()

    os.makedirs("results", exist_ok=True)
    bm.save("results/benchmark_oracle_final.csv")
    om.close_session()
    print("\Benchmark completato!")

if __name__ == "__main__":
    main()