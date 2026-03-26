import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

class Neo4jManager:
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )


    def project_subgraph(self, scale):
        graph_name = f"sub_{scale}"
        node_label = f"PH_NODE_{scale}"
        
        with self.driver.session() as session:
            session.run(f"CALL gds.graph.drop('{graph_name}', false)")
            
            print(f"Proiezione in memoria per scala {scale}% ...")
            session.run(f"""
                CALL gds.graph.project(
                    '{graph_name}',
                    '{node_label}',
                    '*'
                )
            """)
        return graph_name


    def drop_projection(self, name):
        with self.driver.session() as session:
            session.run(f"CALL gds.graph.drop('{name}', false)")


    def close(self):
        self.driver.close()