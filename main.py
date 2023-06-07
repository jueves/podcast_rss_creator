import datetime
import json
import os
import sys

json_file = "podcasts.json"
header_file = "header.rss"
footer_file = "footer.rss"
rss_file = "html/podcasts.rss"
server_ip = "10.69.0.3"

def create_rss_file(podcasts_list, rss_file=rss_file):
    # Define label strings
    title_label = '\n    <item>\n      <title>'
    link_label = '</title>\n      <link>'
    description_label = '</link>\n      <description>'
    audio_url_label = '</description>\n      <enclosure url="'
    audio_type_label = '" type="'
    pubDate_label = '" />\n      <pubDate>'
    end_podcast_label = '</pubDate>\n    </item>'

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
        
    
    ## Add footer
    rss = rss + footer

    ## Write file
    with open(rss_file, "w") as f:
        f.write(rss)

if (len(sys.argv) < 2):
    # Load current podcasts
    with open(json_file) as f:
        podcasts_list = json.load(f)
    # Write rss file
    create_rss_file(podcasts_list)
    
elif (sys.argv[1] == "-h"):
    print("To recreate the rss file from the json file: python3 main.py")
    print("For local files: python3 main.py filename")
    print("For remote files: python3 main.py URL")
    
else:
    file_name = sys.argv[1]
    
    # Standard Input
    print("Introduce metadatos sobre el capítulo. \n" + 
        "Si se deja en blanco estos serán asignados automáticamente.")
    chapter_title = input("Título: ")
    chapter_link = input("URL info: ")
    chapter_description = input("Descripción: ")
    chapter_audioURL = input("URL audio: ")
    chapter_audioType = input("Tipo de archivo: ") or "audio/mpeg"
    chapter_pubDate = input("Fecha de publicación: ") or datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    # Set default title
    if (len(chapter_title)<1):
        chapter_title = file_name

    # Set proper audio url
    if file_name[:4] == "http":
        chapter_audioURL = file_name
    else:
        os.rename(file_name, "html/podcasts/" + file_name)
        chapter_audioURL = "http://" + server_ip + "/podcasts/" + file_name

    # Load current podcasts
    with open(json_file) as f:
        podcasts_list = json.load(f)

    def format_date(date_str):
        date = datetime.datetime.strptime(date_str, "%d/%m/%Y %H:%M")
        formated_date = date.strftime("%a, %d %b %Y %H:%M:%S %Z")
        return(formated_date)

    # Add new podcast
    new_podcast = {
        'title': chapter_title,
        'link': chapter_link,
        'description': chapter_description,
        'audio_url': chapter_audioURL,
        'audio_type': chapter_audioType,
        'pubDate': format_date(chapter_pubDate)
    }

    podcasts_list.append(new_podcast)

    # Save updated podcasts list
    with open(json_file, "w") as f:
        json_podcasts = json.dumps(podcasts_list, indent=4)
        f.write(json_podcasts)

    # Write podcasts to rss file
    create_rss_file(podcasts_list)


'''
    # Create a better name if url is set as default name
    if (file_name == chapter_audioURL):
        file_name = file_name.split(".")
        del file_name[0]
        del file_name[-1]
        file_name = " ".join(file_name)
'''

