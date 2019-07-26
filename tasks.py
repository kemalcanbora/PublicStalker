from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery
from crawler.TwitterCrawler.twitter_engine import TwitterEngine
from crawler.LinkedinCrawler.linkedin_engine import LinkedinEngine
from crawler.InstagramCrawler.instagram_engine import InstagramEngine
from datetime import timedelta
from elasticsearch_dsl import connect_elasticsearch, elastic_indexing, update_query, get_all_tweets, get_all
from settings import ELASTIC_SEARCH_DATABASE_NAME, ELASTIC_SEARCH_NLTK_NAME
from nlp_lib import Analytics
import time

celery = Celery('tasks')
celery.conf.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    CELERY_ACCEPT_CONTENT=['application/json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TASK_SERIALIZER='json')

celery.conf.CELERYBEAT_SCHEDULE = {
    'nltk_twitter': {
        'task': 'tasks.nltk_twitter',
        'schedule': timedelta(seconds=60)
    },
    'twitter_task_crawler': {
        'task': 'tasks.twitter_task_crawler',
        'schedule': timedelta(seconds=60)
    },
    'instagram_task_crawler': {
        'task': 'tasks.instagram_task_crawler',
        'schedule': timedelta(seconds=60)
    },
    'linkedin_user_information_task_crawler': {
        'task': 'tasks.linkedin_user_information_task_crawler',
        'schedule': timedelta(seconds=86400)
    }
}


class Crawler:
    def __init__(self):
        pass

    def twitter_task(self, twitter_user_name):
        if twitter_user_name is not None:
            return TwitterEngine().parse(screen_name=twitter_user_name)
        else:
            pass

    def linkedin_user_information_task(self, linkedin_user_name):
        if linkedin_user_name is not None:
            return LinkedinEngine().get_profile(user_name=linkedin_user_name)

    def linkedin_companys_employee_searcher_task(self, company_name):
        if company_name is not None:
            return LinkedinEngine().search_company(company_name=company_name)

    def instagram_task(self, instagram_user_name):
        engine = InstagramEngine()
        if instagram_user_name is not None:
            return engine.parse_user(instagram_user_name)


ES = connect_elasticsearch()


@shared_task
def search_person(linkedin_user_name=None):
    if linkedin_user_name is None:
        return {"status": None}
    else:
        twitter_data = None
        twitter_user_name = None
        employee_data = Crawler().linkedin_user_information_task(linkedin_user_name)
        if employee_data["twitter"] != []:
            twitter_user_name = employee_data["twitter"][0]["name"]
            twitter_data = Crawler().twitter_task(twitter_user_name)
        else:
            print("Twitter adresi LinkedIn üzerinde yok {}".format(linkedin_user_name))

        data = {"linkedin": employee_data,
                "twitter": twitter_data,
                "instagram": None,
                "twitter_url": twitter_user_name,
                "linkedin_url": linkedin_user_name,
                "instagram_url": None}

        elastic_indexing(es=ES,
                         docs=data,
                         docs_id=linkedin_user_name,
                         doc_type="documents",
                         database=ELASTIC_SEARCH_DATABASE_NAME)

        return data


@shared_task
def update_data(linkedin_user_name, twitter_user_name=None, instagram_user_name=None):
    if twitter_user_name is not None:
        update_query(es=ES, database=ELASTIC_SEARCH_DATABASE_NAME, doc_id=linkedin_user_name, data=twitter_user_name,
                     es_field_name="twitter_url")

    if instagram_user_name is not None:
        update_query(es=ES, database=ELASTIC_SEARCH_DATABASE_NAME, doc_id=linkedin_user_name, data=instagram_user_name,
                     es_field_name="instagram_url")


@shared_task
def twitter_task_crawler():
    data = get_all(es=ES)
    for user in data:
        data_twitter = Crawler().twitter_task(user["twitter_url"])
        update_query(es=ES, database=ELASTIC_SEARCH_DATABASE_NAME, doc_id=user["id"], data=data_twitter,
                     es_field_name="twitter")

@shared_task
def instagram_task_crawler():
    data = get_all(es=ES)
    for user in data:
        data_instagram = Crawler().instagram_task(user["instagram_url"])
        update_query(es=ES, database=ELASTIC_SEARCH_DATABASE_NAME, doc_id=user["id"], data=data_instagram,
                     es_field_name="instagram")


@shared_task
def linkedin_user_information_task_crawler():
    data = get_all(es=ES)
    for user in data:
        data_linkedin = Crawler().linkedin_user_information_task(user["linkedin_url"])
        update_query(es=ES, database=ELASTIC_SEARCH_DATABASE_NAME, doc_id=user["id"], data=data_linkedin,
                     es_field_name="linkedin")


@shared_task
def nltk_twitter():
    tweet_list = []
    for data in get_all_tweets(ES):
        for tweet in data["twitter"]["twitter_text"]:
            tweet_list.append(tweet["text"])
    data = Analytics().pos_tag_analiz(text_list=tweet_list)
    epoch_time = int(time.time())

    data_js = {"data": data,
               "total_tweet": len(tweet_list),
               "labels": list(data["stemmed"].keys()),
               "values": list(data["stemmed"].values())
               }

    elastic_indexing(es=ES,
                     docs=data_js,
                     docs_id=epoch_time,
                     doc_type="documents",
                     database=ELASTIC_SEARCH_NLTK_NAME)

@shared_task
def search_company(company_name=None):
    if company_name is None:
        return {"status":None}
    else:
        employee_list = Crawler().linkedin_companys_employee_searcher_task(company_name)
        twitter_data = None
        for employee in employee_list:
            employee_data = Crawler().linkedin_user_information_task(employee["public_id"])
            try:
                if employee_data["twitter"] != []:
                    twitter_user_name = employee_data["twitter"][0]["name"]
                    twitter_data = Crawler().twitter_task(twitter_user_name)
                else:
                    twitter_user_name = None
                    print("Twitter adresi LinkedIn üzerinde yok {}".format(employee))

                data = {"linkedin": employee_data,
                         "twitter": twitter_data,
                         "instagram":None,
                         "twitter_url":twitter_user_name,
                         "linkedin_url":employee["public_id"],
                         "instagram_url":None}
                elastic_indexing(es=ES,
                                 docs=data,
                                 docs_id=employee["public_id"],
                                 doc_type="documents",
                                 database=ELASTIC_SEARCH_DATABASE_NAME)
            except:
                pass
