import argparse
import datetime
import json
import os

json_file = "podcasts.json"
header_file = "header.rss"
footer_file = "footer.rss"
rss_file = "podcasts.rss"
server_ip = "10.69.0.3"

parser = argparse.ArgumentParser(
    prog="Podcast RSS Creator",
    description="Adds a new podcast entry in the RSS for a given audio file."
    )
parser.add_argument("filename", help="Audio file name")
parser.add_argument("-t", "--title", help = "Podcast chapter title", default="none")
parser.add_argument("-l", "--link", help = "Podcast chapter URL (not audio URL)", default="none")
parser.add_argument("-d", "--description", help = "Podcast chapter description", default="none")
parser.add_argument("--audiourl", default = "none")
parser.add_argument("--audiotype", help = "File type, defaults to 'audio/mpeg'", default="audio/mpeg")
parser.add_argument("--pubDate", help = "Date in which the podcast chapter was released in the format:\
                     23/03/2023 19:00. Defaults to current date and time.",
                    default=datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))

args = parser.parse_args()

# Set default title
if (args.title == "none"):
    args.title = args.filename

# Set proper audio url
if args.filename[:4] == "http":
    args.audiourl = args.filename
else:
    os.rename(args.filename, "html/podcasts/" + args.filename)
    args.audiourl = "http://" + server_ip + "/podcasts/" + args.filename

# Define label strings
title_label = '            {\n               "title": '
link_label = ',\n               "link": '
description_label = ',\n               "description": '
audio_url_label = ',\n               "enclosure": {\n                  "_url": '
audio_type_label = ',\n                  "_type": '
pubDate_label = '\n               },\n               "pubDate": '
end_podcast_label = '\n            },\n'

# Load current podcasts
with open(json_file) as f:
    podcasts_list = json.load(f)

# Add new podcast
new_podcast = {
    'title': args.title,
    'link': args.link,
    'description': args.description,
    'audio_url': args.audiourl,
    'audio_type': args.audiotype,
    'pubDate': args.pubDate
}

podcasts_list.append(new_podcast)


# Load header and footer
with open(header_file) as f:
    header = f.read()

with open(footer_file) as f:
    footer = f.read()

# Create RSS file
## Create file with header
rss = header

## Iterate throught podcasts
for podcast in podcasts_list:
    rss = "".join([rss, title_label + podcast['title'],
             link_label + podcast['link'],
             description_label, podcast['description'],
             audio_url_label, podcast['audio_url'],
             audio_type_label, podcast['audio_type'],
             pubDate_label, podcast['pubDate'],
             end_podcast_label
             ])
    
'''
    rss = rss + title_label + podcast['title'],
    rss = rss + link_label + podcast['link'],
    rss = rss + description_label + podcast['description']
    rss = rss + audio_url_label + podcast['audio_url']
    rss = rss + audio_type_label + podcast['audio_type']
    rss = rss + pubDate_label + podcast['pubDate']
    print("Fin de bucle")

'''
    
## Add footer
rss = rss + footer

print("Lass rss type:")
print(type(rss))

## Write file
with open(rss_file, "w") as f:
    f.write(rss)
