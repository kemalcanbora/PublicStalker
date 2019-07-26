from elasticsearch import Elasticsearch
from settings import ELASTIC_SEARCH_HOST


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': ELASTIC_SEARCH_HOST, 'port': 9200}])
    if _es.ping():
        print('Yay Connected')
        if not _es.indices.exists(index="redfox"):
            _es.indices.create(index="redfox")
    else:
        print('Awww it could not connect!')
    return _es


def store_record(es_object, record, doc_type, database, id=None):
    is_stored = True
    try:
        es_object.index(index=database, doc_type=doc_type, id=id, body=record)  # save
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        is_stored = False
    finally:
        return is_stored


def elastic_indexing(es, docs, doc_type, database, docs_id=None):
    store_record(es_object=es,
                 record=docs,
                 doc_type=doc_type,
                 database=database,
                 id=docs_id)


def update_query(es, es_field_name, database, doc_id, data):
    es.update(index=database, doc_type="documents", id=doc_id, body={"doc": {"{}".format(es_field_name): data}})

    return data


def get_all(es,data_all=None):

    data = es.search(index="redfox", body={
        "from": 0, "size": 1000,
        "query": {
            "match_all": {}
        }
    })
    if data_all == True:
        return data
    else:
        missing_urls = []
        for value in data["hits"]["hits"]:
            try:
                missing_urls.append(
                    {"id": value["_id"],
                     "linkedin_url": value["_source"]["linkedin_url"],
                     "twitter_url": value["_source"]["twitter_url"],
                     "instagram_url": value["_source"]["instagram_url"],
                     "user_name":value["_source"]["linkedin"]["firstName"] +" "+ value["_source"]["linkedin"]["lastName"]
                     })
            except:
                pass

        return missing_urls


def get_all_tweets(es):

    data = es.search(index="redfox", body={
	    "from" : 0, "size" : 1000,
        "query": {
        "match_all": {}
        },
        "_source" : "twitter.twitter_text.text"})

    missing_urls = []
    for value in data["hits"]["hits"]:
        try:
            missing_urls.append({"id": value["_id"],"twitter": value["_source"]["twitter"]})
        except:
            pass

    return missing_urls


def get_all_instagram(es):

    data = es.search(index="redfox", body={
	    "from" : 0, "size" : 1000,
        "query": {
        "match_all": {}
        },
        "_source" : "instagram.images.instagram_image_link"})

    missing_urls = []
    for value in data["hits"]["hits"]:
        try:
            missing_urls.append({"id": value["_id"],"instagram": value["_source"]["instagram"]})
        except:
            pass

    return missing_urls


def get_nltk_statistics(es):
    data = es.search(index="nltk",
                     body = {
                         "from" : 0, "size" : 1,
                         "query": {"match_all": {}},
                         "sort":
                             [{"_id":
                                   {"order": "desc"}}
                              ]})

    return data["hits"]["hits"][0]["_source"]