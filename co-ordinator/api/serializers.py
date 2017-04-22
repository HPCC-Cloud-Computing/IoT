from collections import OrderedDict


def get_metadata(es_result):
    meta = OrderedDict()
    meta["_id"] = es_result["_id"]
    meta["_index"] = es_result["_index"]
    meta["_type"] = es_result["_type"]
    meta["_score"] = es_result["_score"]
    return meta

def es_serialize(es_results):
    result = []
    for es_result in es_results:
        item = OrderedDict()
        item.update(OrderedDict(es_result["_source"]))
        item["meta"] = get_metadata(es_result)
        item["highlight"] = es_result['highlight']
        result.append(item)
    return result
