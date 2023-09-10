import pymongo
import certifi


CONNECTION_STRING = "mongodb+srv://dsci551:dsci551_final@cluster0.twjqnut.mongodb.net/myFirstDatabase"


def get_documents():
   
    client = pymongo.MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
    db = client['final_project']
    collection = db['data']

    all_documents = collection.find({}, {'_id':0})
    
    documents_dict = {}
    for document in all_documents:
        document_id = document["station_id_int"]
        documents_dict[document_id] = document
    #for document in all_documents:
    #   print(document)

    client.close()

    return documents_dict
def update_documents(users):

    client = pymongo.MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
    db = client['final_project']
    collection = db['data']

    # Delete all documents in the collection
    collection.delete_many({})

    # Convert users dictionary keys to strings and create a list of dictionaries
    users_list = [{**{'_id': k}, **v} for k, v in users.items()]
    # Insert new documents into the collection
    collection.insert_many(users_list)
    print('\nUpdate Successed')
    client.close()
#print(get_documents())