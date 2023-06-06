import notional

# from notional import Block, Page
from notional import schema
from notional.iterator import EndpointIterator
from notional.blocks import Page
from notional.orm import connected_page
from config import PAGE_ID, NOTION_SECRET
# from datetime import datetime

# from table_schema import SCHEMA


class NotionInterface:
    def __init__(self):
        self.notional = notional.connect(auth=NOTION_SECRET)

    def get_strava_page_by_id(self):
        return self.notional.pages.retrieve(PAGE_ID)

    def strava_page_has_database(self, strava_page):
        # check if page already contains child database
        # TODO as of current, returns first child of type child_database; resfactor into more selective?
        for block in self.notional.blocks.children.list(strava_page):
            if hasattr(block, "type") and block.type == "child_database":
                return block
            else:
                return False

    def create_activity_log_table_notional(self, strava_page):

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

    def add_row_to_database(self, id, data):
        """Adds row to Strava database, returns true if row already has been added"""
        stravaDB = self.notional.databases.retrieve(id)

        # retrieve activities to be iterated in order to check
        # if new activities are already added
        runs = EndpointIterator(
            endpoint=self.notional.databases().query
        )
        params = {
             "database_id": id,
             "sorts": [
                {
                    "property": "Date",
                    "direction": "descending"
                }
             ]
        }
        for run in runs(**params):
            current_run_date = run.properties["Date"].date.start

            current_run_ID = run.properties["ID"].number

            if current_run_ID == data.upload_id:
                print(
                    f"Skipped {data.name} on {data.start_date_local}; already added!"
                )
                return True
        print(
            f"About to add run {data.name} on {data.start_date_local} with ID {data.upload_id}"
        )
        Run: Page = connected_page(self.notional, source_db=stravaDB)

        Run.create(
            Title=data.name if hasattr(data, "name") else "",
            Date=data.start_date_local
            if hasattr(data, "start_date_local")
            else "",
            Type=data.type,
            Distance=data.distance,
            Duration=data.moving_time,
            ID=data.upload_id,
        )

        print(f"Added {data.name} on {data.start_date_local} to Notion!")
