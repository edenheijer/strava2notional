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
strava_page = notion.get_strava_page_by_id()
database = notion.create_activity_log_table_notional(strava_page=strava_page)
# TODO implement more robust checking for existing entries
# current implementation skips out after 10 activities already added
already_added_counter = 0

for activity in activities:
    already_added = notion.add_row_to_database(database.id, activity)
    if already_added:
        already_added_counter += 1

    if already_added_counter > 9:
        print(
            "Skipped {counter} activities, breaking out now".format(
                counter=already_added_counter
            )
        )
        break
