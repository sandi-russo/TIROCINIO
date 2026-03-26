def run_shortest_path_neo4j(driver, graph_name, src_id, dst_id):
    query = """
    MATCH (s {id: $src}) WITH s LIMIT 1
    MATCH (t {id: $dst}) WITH s, t LIMIT 1
    CALL gds.shortestPath.dijkstra.stream($graphName, {
        sourceNode: s,
        targetNode: t
    })
    YIELD index
    RETURN count(*) as path_found
    """
    with driver.session() as session:
        try:
            res = session.run(query, graphName=graph_name, src=src_id, dst=dst_id)
            return 1
        except Exception:
            return 0


def run_pagerank_neo4j(driver, graph_name):
    query = f"CALL gds.pageRank.stats('{graph_name}') YIELD computeMillis RETURN 1"
    with driver.session() as session:
        session.run(query)
        return 1


def run_wcc_neo4j(driver, graph_name):
    query = f"CALL gds.wcc.stats('{graph_name}') YIELD computeMillis RETURN 1"
    with driver.session() as session:
        session.run(query)
        return 1