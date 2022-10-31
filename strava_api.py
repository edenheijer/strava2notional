from stravaio import strava_oauth2
from stravaio import StravaIO

from config import CLIENT_ID, CLIENT_SECRET
from notion_api import NotionInterface

token = strava_oauth2(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# Get Strava Data
client = StravaIO(access_token=token["access_token"])
activities = client.get_logged_in_athlete_activities()
activities = activities[::-1]
# Upload information to Notion
notion = NotionInterface()

database = notion.create_activity_log_table_notional()
# TODO implement more robust checking for existing entries
# current implementation assumes no new records after newest date in Notion
already_added = False

for activity in activities:
    already_added = notion.add_row_to_database(database, activity)
    if already_added:
        break
