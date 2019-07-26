from linkedin_api import Linkedin
from settings import LINKEDIN_USER_NAME,LINKEDIN_PASSWORD
import tldextract
import toolz
import time,random

def url_parse(url):
    ext = tldextract.extract(url)
    if ext.domain=="linkedin":
        return url.split("/in")[1].replace("/","")
    else:
        return url


class LinkedinEngine:
    def __init__(self):
        self.api = Linkedin(LINKEDIN_USER_NAME,LINKEDIN_PASSWORD)

    def search_company(self,company_name):
        return self.api.search_people(keywords=company_name)

    def get_profile(self,user_name):
        time.sleep(random.randint(0,3))
        user_name = url_parse(user_name)
        get_contact_dict = self.api.get_profile_contact_info(user_name)
        get_profile_dict = self.api.get_profile(user_name)
        return toolz.merge(get_contact_dict, get_profile_dict)