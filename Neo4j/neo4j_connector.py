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
        """Find who a person knows directly and indirectly (up to 2 hops)"""
        query = """
        MATCH (a:Person)-[:KNOWS*1..2]->(b:Person) 
        WHERE a.name = $name
        RETURN DISTINCT a.name AS From, b.name AS To;
        """
        return self.run_query(query, {"name": person_name})


    def find_groups(self, person_name):
        """Find which groups a person belongs to"""
        query = """
        MATCH (p:Person)-[:MEMBER_OF]->(g:Group)
        WHERE p.name = $name
        RETURN DISTINCT p.name AS Person, g.name AS Group;
        """
        result = self.run_query(query, {"name": person_name})
        print("DEBUG: Raw Group Data:", result)  # Debugging output
        return result



# Replace with your Neo4j credentials
NEO4J_URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "Indresh@2006"  
# Initialize Reasoning System
db = Neo4jReasoning(NEO4J_URI, USERNAME, PASSWORD)

# Test Reasoning
person = "Person 1"
connections = db.find_connections(person)
groups = db.find_groups(person)

print(f"\nWho does {person} know (directly or indirectly)?")
for row in connections:
    print(f"{row['From']} → {row['To']}")

print(f"\nWhat groups is {person} a member of?")
for row in groups:
    print(f"{row['Person']} → {row['Group']}")

db.close()
