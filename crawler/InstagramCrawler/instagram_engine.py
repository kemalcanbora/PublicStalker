from InstagramAPI import InstagramAPI
import requests
import json
from pprint import pprint
from settings import INSTAGRAM_USER_NAME,INSTAGRAM_PASSWORD

class InstagramEngine:
    api = InstagramAPI(INSTAGRAM_USER_NAME,INSTAGRAM_PASSWORD)
    api.login()

    def __init__(self):
        self.isLogin = False

    def parse_user(self,user_name):
        url = "https://www.instagram.com/{}/?__a=1".format(user_name)
        r = requests.get(url)
        if r.status_code is not 200:
            return {"status_code": r.status_code}

        js = json.loads(r.text)
        user_id = js["graphql"]["user"]["id"]
        private = js["graphql"]["user"]["is_private"]

        if private is True:
            return {"status": False}  # private accounts

        InstagramEngine.api.getProfileData()
        InstagramEngine.api.getUserFeed(usernameId=user_id)
        dataset = []
        for item in InstagramEngine.api.LastJson['items']:
            comments = []
            try:
                like_count = item["like_count"]
            except:
                like_count = None
            try:
                comment_count = item["comment_count"]
            except:
                comment_count = None
            try:
                img_url = item["image_versions2"]["candidates"][0]["url"]
            except:
                img_url = None
            try:
                location = item["location"]["name"]
            except:
                location = None

            try:
                created_at = item["caption"]["created_at"]
            except:
                created_at = None

            try:
                text = item["caption"]["text"]
            except:
                text = None

            try:
                media_id = item["caption"]["media_id"]
            except:
                media_id = item["id"].split("_")[0]

            if  comment_count > 0:
                InstagramEngine.api.getMediaComments(str(media_id), str(comment_count))
                for comment in InstagramEngine.api.LastJson["comments"]:
                    comments.append({
                        "text": comment["text"],
                        "creation_time": comment["created_at"],
                        "username": comment["user"]["username"],
                        "user_full_name": comment["user"]["full_name"],
                        "user_id": comment["user_id"],
                        # "comment_like_count": comment["comment_like_count"]
                    })

            data = {"instagram_publish_date": created_at,
                    "instagram_text": text,
                    "instagram_image_link": img_url,
                    "instagram_location": location,
                    "instagram_like_count": like_count,
                    "instagram_comment_count": comment_count,
                    "instagram_comments": comments}

            dataset.append(data)

        instagram = {"images": dataset,
                     "instagram_user_name": user_name}
        return instagram

    def parse_media(self,media_id,max_id):
        if self.isLogin is False:
            return {"message":"Media cannot be parsed."}
        self.api.getMediaComments(media_id,max_id)
        pprint(self.api.LastJson)