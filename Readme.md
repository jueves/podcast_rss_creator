This is a podcast RSS generator.  
Given an audio file and its metadata, it adds it to the current RSS file.  
If given an URL it downloads and extracts the audio and metadata and adds it to the RSS file.

## Example
To recreate the rss file from the json file: `python3 main.py`
For local files: `python3 main.py my_audio.ogg`
For remote files: `python3 main.py www.somewebsite.com/great_chapter.ogg`


### To do
- [X] Compose RSS file.
- [x] Replace argparser arguments with standard input.
- [ ] Add yt-dlp support.

