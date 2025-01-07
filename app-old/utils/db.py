from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["crowd_iq"]


def save_metadata(data):
    """
    Save metadata to the database.

    Args:
        data (dict): Metadata to save.
    """
    db.metadata.insert_one(data)


def get_all_metadata():
    """
    Retrieve all metadata from the database.

    Returns:
        list: Metadata documents.
    """
    return list(db.metadata.find())


def export_metadata(file_path):
    data = get_all_metadata()
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
