from neo4j import GraphDatabase

class Neo4jReasoning:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="your_password_here"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters).data()
    
    def get_reasoning(self, user_message):
        print("Reasoning recieved -- ")
