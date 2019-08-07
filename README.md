# twitter-media-downloader
downloads photos and videos from twitter
# Usage
Get prompted for input:
```
python3 core.py
```
Use a list:
```
python3 core.py list.txt
```
Dont use the username but the whole link. Like this: https://twitter.com/twitter
### todo:
- [ ] Make crawling and downloading run at the same time.
- [ ] Only ignore 403 Error while downloading videos.
- [ ] When the program stops while downloading photos write the id of the last downloaded photo to the resume file so the crawler knows where it left off.
