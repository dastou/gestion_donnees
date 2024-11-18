from neomodel import db

# Configurez la connexion à la base de données
db.set_connection('bolt://neo4j:123456789@localhost:7687')

# Test de la connexion
try:
    results, meta = db.cypher_query('MATCH (n) RETURN n LIMIT 1')
    print("Connection successful:", results)
except Exception as e:
    print("Connection failed:", str(e))
