from clarifai import rest
from clarifai.rest import ClarifaiApp
from bs4 import BeautifulSoup
import urllib, praw

MODEL_LINKS = []
CLARIFAI_APP_ID = "APP_ID_HERE"
CLARIFAI_APP_SECRET = "APP_SECRET_HERE" #hidden!
REDDIT_CL_ID = "CL_ID_HERE"
REDDIT_CL_SECRET = "CL_SECRET_HERE" #hidden!

app = ClarifaiApp(CLARIFAI_APP_ID, CLARIFAI_APP_SECRET)

subreddit = input("please input a subreddit: ")
s = urllib.request.urlopen("http://imgur.com/r/%s" % (subreddit)).read()
soup = BeautifulSoup(s, "html.parser")

for link in soup.find_all("img"):
	src = link.get("src")[2:len(link.get("src"))]
	if "i.imgur.com" in src:
		#need to remove the thumbnail letter imgur adds to its links to get HD
		MODEL_LINKS.append(src[0:len(src)-5] + src[len(src)-4:len(src)])

#model = app.models.get("general-v1.3")
#output = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')

#predictions = output["outputs"][0]["data"]["concepts"]
#for prediction in predictions:
	#print(prediction["name"], '{0:.4g}'.format(prediction["value"]*100))

r = praw.Reddit(user_agent='python3:github/jaruserickson:v0.1 (by /u/levelprime)')
r.set_oauth_app_info(client_id=REDDIT_CL_ID,
                      client_secret=REDDIT_CL_SECRET,
                      redirect_uri='http://github.com/jaruserickson/recomeddit'
                                   'authorize_callback')
print(r.get_subreddit(subreddit, fetch=True))
print("0-----0")

print(MODEL_LINKS)
print("Complete.")