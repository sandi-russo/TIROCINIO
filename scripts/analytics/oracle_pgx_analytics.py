def run_shortest_path_oracle(session, graph, src_id, dst_id):
    analyst = session.create_analyst()
    try:
        src  = graph.get_vertex(src_id)
        dst  = graph.get_vertex(dst_id)
        path = analyst.shortest_path_bidirectional_dijkstra(
            graph, src, dst, weight=None
        )
        return path.get_edges().size() if path else 0
    except Exception as e:
        print(f"Shortest path error: {e}")
        return 0


def run_pagerank_oracle(session, graph):
    analyst = session.create_analyst()
    analyst.pagerank(graph)
    return graph.num_vertices


def run_wcc_oracle(session, graph):
    analyst = session.create_analyst()
    analyst.wcc(graph)
    return graph.num_vertices