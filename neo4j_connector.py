from neo4j import GraphDatabase

class Neo4jReasoning:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters).data()
  
    def find_connections(self, person_name):
        query = """
        MATCH (a:Person)-[:KNOWS*1..2]->(b:Person) 
        WHERE a.name = $name
        RETURN DISTINCT a.name AS From, b.name AS To;
        """
        return self.run_query(query, {"name": person_name})

    def find_groups(self, person_name):
        query = """
        MATCH (p:Person)-[:MEMBER_OF]->(g:Group)
        WHERE p.name = $name
        RETURN DISTINCT p.name AS Person, g.name AS Group;
        """
        return self.run_query(query, {"name": person_name})
