# strava 2 notional
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`strava2notional` is a forked implementation of [`strava2notion`](https://github.com/IVIURRAY/strava2notion). This implementation uses the [`notional`](https://github.com/jheddings/notional/) API wrapper, rather than the unofficial `notion` API.


![Notion Data](/media/notion.png)

# How to use

### Setup 
1. Create an App though the [Strava API](https://www.strava.com/settings/api)
2. Create a page in Notion that will act as a parent page for the Strava activity database.
3. Open the page in a webbrowser and note the parent page ID (character string following *notion.so/[parent-page-name]*-)
4. Create a new integration through [My Integrations](https://www.notion.so/my-integrations) , grant it access to your Notion and note Internal Integration Token


### How to run
1. `git clone https://github.com/edenheijer/strava2notional.git`
2. `virtualenv venv`
3. `source venv/bin/activate` (Mac) or `venv/Scripts/activate` (Window)
4. `pip install -r requirements.txt`
5. Insert `Client ID` and `Client Secret` into [`strava_api.py`](strava_api.py).
6. Insert internal integration token from the newly created Integration info [`config.py`](config.py).
7.  Enter the page ID in [`config.py`](config.py) from step 5 of the Setup
8. `python strava_api.py` (Requires 3.5+ and 64-bit python install)
9. If you've set it up correctly a Strava App auth page will appear
10. Click Authorize ![Strava Auth](/media/oauth.png)
11. The script will create a database if there isn't one already and add new entries into it
12. You will be able to see it adding data in real time (Press `Ctrl + r` if you see nothing happening)

# Contact
## Author

👤 **Ewout den Heijer**

* Website: wgdenheijer.nl
* Github: [@edenheijer](https://github.com/edenheijer)
* LinkedIn: [@Ewout den Heijer](https://www.linkedin.com/in/ewout-den-heijer-8325481a/)
  
