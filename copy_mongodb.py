from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def copy_collections(source_client, destination_client):
    # Get the list of collection names from the source database
    source_collections = source_client.list_collection_names()

    # Copy data from each collection to the destination database
    for collection_name in source_collections:
        source_collection = source_client[collection_name]
        destination_collection = destination_client[collection_name]

        # Retrieve all documents from the source collection
        documents = source_collection.find({})

        # Insert documents into the destination collection
        destination_collection.insert_many(documents)

if __name__ == "__main__":
    source_uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
    destination_uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"

    source_client = MongoClient(source_uri, server_api=ServerApi('1'), connect=False)
    destination_client = MongoClient(destination_uri, server_api=ServerApi('1'), connect=False)

    copy_collections(source_client, destination_client)

    # Close the connections
    source_client.close()
    destination_client.close()
