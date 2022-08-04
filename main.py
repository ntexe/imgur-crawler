from string import ascii_letters, digits
from random import randint, choices
from sys import argv
from sqlite3 import connect
import logging
import os

import grequests

import settings

default_links_per_call = 24 # link per call default

# logging setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ])

class App():
    def __init__(self, links_per_call=24):
        logging.info("Initializing class App")
        with open(settings.name_of_image_not_found, "rb") as file:
            self.image_not_found_bytes = file.read()
        self.links_per_call = links_per_call

        #### Constants for link generator ####

        # maxwidth parameter to get full resolution pic
        self.link_template = "https://i.imgur.com/{}?maxwidth=4320"
        self.strs = ascii_letters + digits
        self.range_of_lenghts_of_name = (5, 7)
        self.ext_to_check = (".png", ".mp4") # order is IMPORTANT

    def init_db(self):
        logging.info("Initializing database")
        connection = connect(settings.db_name)
        cursor = connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS downloaded_files_ids
            (id TEXT,
            moment TEXT)
            """)

        connection.commit()

        return connection, cursor


    def create_folder_if_not_exits(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def validate_response(self, response) -> bool:
        # return False if response is None
        if response == None:
            return False
            
        """
        videos and photos has "content-type" header, which is "video/mp4" or
        "image/png" or other, but html pages isn't have "content-type" header
        """

        # return False if response isn't image/video
        if "content-type" in response.headers:
            # if content-type problem will be fixed
            if  "image" not in response.headers["content-type"] \
            and "video" not in response.headers["content-type"]:
                return False
        else:
            return False

        # return False if file is "requested image not exits" or empty
        if response.content == self.image_not_found_bytes \
        or response.content == b"":
            return False

        return True

    def generate_name_with_extension(self, extension) -> str:
        return ''.join(
            choices(self.strs, k=randint(*self.range_of_lenghts_of_name))
            ) + extension

    def generate_link_list(self):
        link_list = \
        [
        self.link_template.format(self.generate_name_with_extension(ext))
        for ext in self.ext_to_check
        for _ in range(self.links_per_call // len(self.ext_to_check))
        ]

        return link_list

    def parse_id_with_ext(self, url) -> str:
        return url.split('/')[-1].split('?')[0]

    def parse_id(self, url) -> str:
        return self.parse_id_with_ext(url).split(".")[0]

    def generate_path(self, url) -> str:
        return f"{settings.path_to_folder}/{self.parse_id_with_ext(url)}"

    def main(self):
        self.create_folder_if_not_exits(settings.path_to_folder)

        connection, cursor = self.init_db()

        previous_link_bytes = None

        logging.info("Starting Crawling")

        while 1:
            logging.info(f"Generating {self.links_per_call} links")
            # generating link list
            link_list = self.generate_link_list()

            logging.info(f"Sending {self.links_per_call} requests")
            # charging and sending requests
            responses = grequests.map((grequests.get(u) for u in link_list))

            # checking and saving
            for response in responses:
                if not self.validate_response(response):
                    continue

                # continue if previous link file has the same content
                if response.content == previous_link_bytes:
                    continue
                previous_link_bytes = response.content

                # continue if id is already in DB
                cursor.execute("""SELECT id
                                  FROM downloaded_files_ids
                                  WHERE id=?""",
                               (self.parse_id(response.url),))
                if cursor.fetchall(): # if list is not empty
                    continue

                cursor.execute("""INSERT INTO downloaded_files_ids VALUES
                                  (?, CURRENT_TIMESTAMP)""",
                               (self.parse_id(response.url),))

                logging.info(
                f"Saving {response.url} to {self.generate_path(response.url)}"
                )

                # saving
                with open(self.generate_path(response.url), 'wb') as out_file:
                    out_file.write(response.content)
            connection.commit()

def parse_arg():
    if len(argv) > 1:
        try:
            int(argv[1])
        except:
            return default_links_per_call
        return int(argv[1])
    return default_links_per_call

# _ to avoid variable bugs
_links_per_call = parse_arg()

App(_links_per_call).main()