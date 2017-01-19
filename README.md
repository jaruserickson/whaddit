# whaddit

let ai guess what a subreddit is about!

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
python3 init.py
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

*created with :purple_heart: on a thursday in January*