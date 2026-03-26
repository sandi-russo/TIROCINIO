import os
from opg4py import graph_server
from dotenv import load_dotenv

class OracleManager:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
        self.user     = os.getenv("ORACLE_USER")
        self.password = os.getenv("ORACLE_PASSWORD")
        self.base_url = os.getenv("ORACLE_PGX_URL")
        self.session  = None
        self.graph    = None


    def connect_pgx(self):
        try:
            instance = graph_server.get_instance(
                self.base_url,
                self.user,
                self.password
            )
            self.session = instance.create_session("benchmark_session")
            print(f"Connesso! Session ID: {self.session.id}")
            return self.session
        except Exception as e:
            print(f"Errore connessione PGX: {e}")
            return None
        

    def load_subgraph(self, scale=25):
        if not self.session:
            self.connect_pgx()

        graph_sql_name = f"pharmebinet_graph_{scale}"

        print(f"Caricamento da DB del grafo: {graph_sql_name}...")
        try:
            self.graph = self.session.read_graph_by_name(graph_sql_name.upper(), "pg_sql")
            print(f"Grafo pronto: {self.graph.num_vertices} nodi, {self.graph.num_edges} archi")
            return self.graph
        except Exception as e:
            print(f"Errore nel caricamento del grafo Oracle: {e}")
            return None
            

    def close_session(self):
        if self.session:
            self.session.close()
            print("Sessione chiusa.")