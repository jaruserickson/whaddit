from clarifai import rest
from clarifai.rest import ClarifaiApp
from bs4 import BeautifulSoup
import requests, json, urllib

MODEL_LINKS = []
CLARIFAI_APP_ID = "YOUR_ID"
CLARIFAI_APP_SECRET = "YOUR_SECRET" #hidden!

def subExists(sub):
	#check the json
	resp = requests.get("http://reddit.com/r/" + sub + ".json", headers={'User-agent' : 'recommeddit:python3:v0.02 (by /u/levelprime)'})
	data = json.loads(resp.text)
	#data children will be empty on an invalid sub
	if (data["data"]["children"] == []):
		return False
	else:
		return True

if __name__ == "__main__":
	app = ClarifaiApp(CLARIFAI_APP_ID, CLARIFAI_APP_SECRET)

	#verify subreddit input is valid
	flag = False
	while not flag:
		subreddit = input("please input a subreddit: ")
		flag = subExists(subreddit)
		if not flag:
			print("that subreddit doesn't exist!")

	#get top X images from subreddit via bs4
	response = urllib.request.urlopen("http://imgur.com/r/%s" % (subreddit)).read()
	soup = BeautifulSoup(response, "html.parser")

	for link in soup.find_all("img"):
		src = link.get("src")[2:len(link.get("src"))]
		if "i.imgur.com" in src:
			#need to remove the thumbnail letter imgur adds to its links to get HD
			MODEL_LINKS.append(src[0:len(src)-5] + src[len(src)-4:len(src)])

	#predict with clarifai api what the images are most commonly
	#model = app.models.get("general-v1.3")
	#output = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')

	#predictions = output["outputs"][0]["data"]["concepts"]
	#for prediction in predictions:
		#print(prediction["name"], '{0:.4g}'.format(prediction["value"]*100))

	#print reccomendations

	print(MODEL_LINKS)
	print("Complete.")