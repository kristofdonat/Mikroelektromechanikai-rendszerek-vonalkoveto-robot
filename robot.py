import tweepy
import random

auth = tweepy.OAuthHandler('felhaszn_kulcs','felhaszn_jelszó')
auth.set_access_token('API_kulcs','API_jelszó')

api = tweepy.API(auth)
randomszam = random.randrange(1,100)
api.update_status(str(randomszam))
print("sikeresen tweetelve az, hogy ", randomszam)
