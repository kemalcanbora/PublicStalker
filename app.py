from flask_cors import CORS
from flask import request, Flask
from celery.result import AsyncResult
from json import dumps
import tasks

app = Flask(__name__)
app.config.update(dict(SECRET_KEY='your_secret_key', CSRF_ENABLED=True, ))
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/search_person', methods=['GET', 'POST'])
def search_person_api():
    linkedin_user_name = request.args.get('linkedin_user_name', None)
    res = tasks.search_person.delay(linkedin_user_name)
    AsyncResult(res, app=tasks.celery)

    return dumps({"status":linkedin_user_name})


@app.route('/search_company', methods=['GET', 'POST'])
def search_company_api():
    company_name = request.args.get('company_name', None)
    res = tasks.search_company.delay(company_name)
    AsyncResult(res, app=tasks.celery)

    return dumps({"status":company_name})


@app.route('/update_data', methods=['GET', 'POST'])
def update_data_api():
    linkedin_user_name = request.args.get('linkedin_user_name', None)
    twitter_user_name = request.args.get('twitter_user_name', None)
    instagram_user_name = request.args.get('instagram_user_name', None)

    res = tasks.update_data.delay(linkedin_user_name,
                                  twitter_user_name,
                                  instagram_user_name)
    AsyncResult(res, app=tasks.celery)

    return dumps({"update":linkedin_user_name})



if __name__ == '__main__':
    app.run()
