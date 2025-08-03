# src/app/core/mongodb.py
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
        for key, val in value.items():
            if key == "_id":
                if isinstance(val, str):
                    new_value[key] = {"$oid": val}
                    continue

                if isinstance(val, dict) and "$in" in val:
                    in_array = val["$in"]
                    if isinstance(in_array, list):
                        new_array = []
                        for v in in_array:
                            if isinstance(v, str):
                                new_array.append({"$oid": v})
                            else:
                                new_array.append(v)
                        val["$in"] = new_array
                new_value[key] = convert_oid(val)
            else:
                new_value[key] = convert_oid(val)
        return new_value

    elif isinstance(value, list):
        return [convert_oid(item) for item in value]

    else:
        return value
