import tweepy
from settings import TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_SECRET, TWITTER_CONSUMER_KEY, TWITTER_ACCESS_TOKEN_KEY, GET_TWEET_COUNT


class TwitterEngine:
    def __init__(self):
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth,wait_on_rate_limit=True)

    def parse(self, screen_name, twitter_count=GET_TWEET_COUNT, retweet=False):
        tweet = []
        try:
            new_tweets = self.api.user_timeline(screen_name=screen_name, count=twitter_count, tweet_mode="extended",
                                                include_rts=retweet)

            user = self.api.get_user(screen_name=screen_name)

            full_name = user.name
            location = user.location
            protected = user.protected
            creation_date = user.created_at.timestamp()  # epoch time
            friends_ids = self.get_friends_ids(screen_name)
            followers_ids = self.get_followers_ids(screen_name)

            for i in new_tweets:
                tweet.append({"text": i.full_text, "publish_date": i.created_at.timestamp()})  # epoch time

            return {"twitter_location": location,
                    "twitter_creation_date": creation_date,
                    "twitter_full_name": full_name,
                    "twitter_text": tweet,
                    "protected": protected,
                    "followers_ids": followers_ids,
                    "friends_ids": friends_ids
                    }

        except tweepy.TweepError as e:
            if e.api_code == 34:
                print("not exist this user")
            if e.args[0] == "Not authorized.":
                print("Not authorized..follow {}".format(screen_name))
                try:
                    user = self.api.get_user(screen_name=screen_name)
                    self.api.create_friendship(user.id)
                except:
                    pass

    def get_followers_ids(self, screen_name):
        ids = []
        for page in tweepy.Cursor(self.api.followers_ids, screen_name=screen_name).pages():
            ids.extend(page)
        return ids

    def get_friends_ids(self, screen_name):
        ids = []
        for page in tweepy.Cursor(self.api.friends_ids, screen_name=screen_name).pages():
            ids.extend(page)
        return ids