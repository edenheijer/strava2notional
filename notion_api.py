import notional

# from notional import Block, Page
from notional import schema
from notional.iterator import EndpointIterator
from notional.records import Database, Page
from notional.orm import connected_page
from config import TOKEN_V2, PAGE_ID, NOTION_SECRET
from datetime import datetime, tzinfo

# from table_schema import SCHEMA


class NotionInterface:
    def __init__(self):
        self.notional = notional.connect(auth=NOTION_SECRET)
        self.strava_page_title = "CPC"
        self.strava_table_title = "Strava log"

    def get_strava_page_by_id(self):
        page = self.notional.pages.retrieve(PAGE_ID)
        return page


    def get_strava_page(self):
        strava_page = None
        for page in self.client.get_top_level_pages():
            if self.strava_page_title == page.title:
                strava_page = page

        if strava_page is None:
            raise LookupError(
                f"Unable to find Strava page, is there a page with a "
                f"title of '{self.strava_page_title}' in your workspace?"
            )

        return strava_page

    def create_activity_log_table_notional(self):
        # retrieve Strava page by ID
        strava_page = self.get_strava_page_by_id()

        # check if page already contains child database
        # TODO as of current, returns first child of type child_database; refactor into more selective?
        for block in self.notional.blocks.children.list(strava_page):
            if hasattr(block, "type") and block.type == "child_database":
                return block

        # define schema for Strava database
        strava_schema = {
            "Title": schema.Title(),
            "Date": schema.Date(),
            "Type": schema.Select(),
            "Distance": schema.Number(),
            "Duration": schema.Number(),
            "ID": schema.Number(),
        }
        strava_table = self.notional.databases.create(
            parent=strava_page, title="Strava", schema=strava_schema
        )

        return strava_table

    def add_row_to_database(self, db: Database, data):
        """Adds row to Strava database, returns true if row already has been added"""
        stravaDB = self.notional.databases.retrieve(db.id)

        # retrieve activities to be iterated in order to check if new activities are already added
        runs = EndpointIterator(
            endpoint=self.notional.databases().query,
            database_id=db.id,
            sorts=[{"direction": "descending", "property": "Date"}],
        )
        
        for run in runs:
            current_run_date = datetime.strptime(run["properties"]["Date"]["date"]["start"], "%Y-%m-%d").replace(tzinfo=None)

            current_run_title = run["properties"]["Title"]["title"][0]["plain_text"]
            current_run_ID = run["properties"]["ID"]["number"]

            if datetime.strptime(
                run["properties"]["Date"]["date"]["start"], "%Y-%m-%d"
            ).replace(tzinfo=None) > data.start_date_local.replace(tzinfo=None) or (current_run_ID == data.upload_id
            ):
                print(f"Skipped {data.name} on {data.start_date_local}; already added!")
                return True
        print(f"About to add run {data.name} on {data.start_date_local} with ID {data.upload_id}")
        Run: Page = connected_page(self.notional, source_db=stravaDB)

        run_record = Run.create(
            Title=data.name if hasattr(data, "name") else "",
            Date=data.start_date_local if hasattr(data, "start_date_local") else "",
            Type=data.type,
            Distance=data.distance,
            Duration=data.moving_time,
            ID=data.upload_id
        )

        print(f"Added {data.name} on {data.start_date_local} to Notion!")

