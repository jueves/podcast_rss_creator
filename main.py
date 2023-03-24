import argparse
import datetime
import json
import os

json_file = "podcasts.json"
server_ip = "10.69.0.3"

parser = argparse.ArgumentParser(
    prog="Podcast RSS Creator",
    description="Adds a new podcast entry in the RSS for a given audio file."
    )
parser.add_argument("filename", help="Audio file name")
parser.add_argument("-t", "--tittle", help = "Podcast chapter title", default=parser.parse_args().filename)
parser.add_argument("-l", "--link", help = "Podcast chapter URL (not audio URL)", default="none")
parser.add_argument("-d", "--description", help = "Podcast chapter description", default="none")
parser.add_argument("--audiourl", default = "none")
parser.add_argument("--audiotype", help = "File type, defaults to 'audio/mpeg'", default="audio/mpeg")
parser.add_argument("--pubDate", help = "Date in which the podcast chapter was released in the format:\
                     23/03/2023 19:00. Defaults to current date and time.",
                    default=datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))

args = parser.parse_args()

with open(json_file) as f:
    podcasts_dic = json.load(f)

# Set proper audio url
if args.filename[:4] == "http":
    args.audiourl = args.filename
else:
    os.rename(args.filename, "podcasts/" + args.filename)
    args.audiourl = "http://" + server_ip + "/podcasts/" + args.filename


# Define label strings
title_label = '            {\n               "title": '
link_label = ',\n               "link": '
description_label = ',\n               "description": '
audio_url_label = ',\n               "enclosure": {\n                  "_url": '
audio_type_label = ',\n                  "_type": '
pubDate_label = '\n               },\n               "pubDate": '
end_podcast_label = '\n            },\n'

# Create RSS file
