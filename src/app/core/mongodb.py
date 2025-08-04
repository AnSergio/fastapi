# src/app/core/mongodb.py
from bson import ObjectId


def convert_id(doc: dict) -> dict:
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


def convert_ids(docs: list[dict]) -> list[dict]:
    for doc in docs:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
    return docs


def convert_oid(value):
    if isinstance(value, dict):
        new_value = {}
        for k, v in value.items():
            if k == "_id":
                if isinstance(v, str):
                    # Converte diretamente para ObjectId
                    new_value[k] = ObjectId(v)
                    continue
                elif isinstance(v, dict) and "$in" in v and isinstance(v["$in"], list):
                    # Caso de _id: { $in: [ "id1", "id2" ] }
                    new_value[k] = {
                        "$in": [ObjectId(item) if isinstance(item, str) else item for item in v["$in"]]
                    }
                    continue
            # Recorre para outras chaves normalmente
            new_value[k] = convert_oid(v)
        return new_value

    elif isinstance(value, list):
        return [convert_oid(item) for item in value]

    else:
        return value
