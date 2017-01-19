from clarifai import rest
from clarifai.rest import ClarifaiApp
from bs4 import BeautifulSoup
import requests, json, urllib

MODEL_LINKS = []
CLARIFAI_APP_ID = "YOUR_ID"
CLARIFAI_APP_SECRET = "YOUR_SECRET" #hidden!

def subExists(sub):
	#(str) -> bool
	#checks if a subreddit exists, based on its json
	print("Validating subreddit...")
	resp = requests.get("http://reddit.com/r/" + sub + ".json", headers={'User-agent' : 'whaddit:python3:v1.0 (by /u/levelprime)'})
	data = json.loads(resp.text)
	#data children will be empty on an invalid sub
	if (data["data"]["children"] == []):
		return False
	else:
		return True

def mostCommon(preds):
	#(list of lists of str,double) -> dict(str, double)
	#catered function to find most commonly found values in predicitons 2d list
	print("Getting most common trends...")
	common, commonAvg = {}, {}
	for prediction in predictions:
		if prediction[0] not in list(common.keys()):
			common[prediction[0]] = [prediction[1]]
		else:
			common[prediction[0]].append(prediction[1])
	#now calculate the average for prediction values and set the key to that (weighted by occurrence)
	for key in list(common.keys()):
		avg = (float(sum(common[key]))/float(len(common[key])))
		length = int(len(common[key]))
		common[key] = avg*length
		commonAvg[key] = avg
	return (common, commonAvg)

def addGuess(guess, prob, dict):
	#filter out the weird "no person" guess clarifai has
	if guess != "no person":
		dict[guess] = prob
		return True
	return False

if __name__ == "__main__":
	app = ClarifaiApp(CLARIFAI_APP_ID, CLARIFAI_APP_SECRET)

	#verify subreddit input is valid
	flag = False
	while not flag:
		subreddit = input("Please input a subreddit: ")
		flag = subExists(subreddit)
		if not flag:
			print("That subreddit doesn't exist!")

	#get top X images from subreddit via bs4
	print("Scraping subreddit...")
	response = urllib.request.urlopen("http://imgur.com/r/%s" % (subreddit)).read()
	soup = BeautifulSoup(response, "html.parser")

	for link in soup.find_all("img"):
		src = link.get("src")[2:len(link.get("src"))]
		if "i.imgur.com" in src:
			#need to remove the thumbnail letter imgur adds to its links to get HD
			MODEL_LINKS.append(src[0:len(src)-5] + src[len(src)-4:len(src)])

	#predict with clarifai api what the images are most commonly representative of
	model = app.models.get("general-v1.3")
	predictions = []

	#puts predictions into 2d array
	print("Getting data from clarifai... (this may take a minute)")
	for i in range(len(MODEL_LINKS)):
		url = 'https://%s' % MODEL_LINKS[i]
		output = model.predict_by_url(url=url)
		for prediction in output["outputs"][0]["data"]["concepts"]:
			predictions.append([prediction["name"], prediction["value"]])

	common = mostCommon(predictions)

	#get sorted tuple
	commonTuple = sorted(common[0].items(), key=lambda x:x[1])
	top = {}
	
	for i in range(3):
		if not addGuess(commonTuple[len(commonTuple)-(i+1)][0], common[1][commonTuple[len(commonTuple)-(i+1)][0]]*100, top):
			addGuess(commonTuple[len(commonTuple)-4][0], common[1][commonTuple[len(commonTuple)-4][0]]*100, top)

	sortedWeights = sorted(top.items(), key=lambda x:x[1])

	print("I think your subreddit is about %s (%f%%) or maybe %s (%f%%) or %s (%f%%)." % (sortedWeights[2][0],
																							sortedWeights[2][1],
																							sortedWeights[1][0],
																							sortedWeights[1][1],
																							sortedWeights[0][0],
																							sortedWeights[0][1]))

	print("Complete.")