# whaddit
<p align="center">
  <img src="https://github.com/jaruserickson/whaddit/blob/master/img/whaddit.png?raw=true"/>
  <br> Let AI guess what your favourite subreddit is all about!
</p>

## Usage
To use whaddit, you'll need a few python libraries first (and an API key!)

```
pip3 install clarifai
pip3 install beautifulsoup4
pip3 install requests
```

After installing the 3 libraries above, you'll need an api key for clarifai since i can't afford to host on my own!

```
https://www.clarifai.com/
```

Then simply input your favourite subreddit and clarifai will guess what the subreddit is about, and try to predict its /r/ url!

Here's a common output! :smiley:

```
python3 whaddit.py
```
```
Please input a subreddit: dogs
Validating subreddit...
Scraping subreddit...
Getting data from clarifai... (this may take a minute)
Getting most common trends...
I think your subreddit is about dog (97.755847%) or maybe mammal (95.322234%) or portrait (93.955130%).
Complete.
```

## Logic
whaddit is a combination of multiple python libraries and some basic data analysis. 

whaddit works as follows:

1. Verify the subreddit a user inputs is valid with Requests and JSON
2. Using BeautifulSoup4, whaddit scrapes the imgur/r/sub the user specifies and gets urls to the 50 hottest photos from the subreddit
3. Clarifai will then analyze all the photos and predict what is in each photo, feeding results into a large dictionary
4. whaddit orders the predictions based on percentage and occurrence

That's all there is to it!

*created with :purple_heart: on a thursday in January*
