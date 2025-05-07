from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
def get_session():
    cloud_config = {
        'secure_connect_bundle': 'secure-connect-final-project.zip'
    }

    with open("final_project-token.json") as f:
        secrets = json.load(f)

    CLIENT_ID = secrets["clientId"]
    CLIENT_SECRET = secrets["secret"]

    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    session.set_keyspace('default_keyspace')
    return session