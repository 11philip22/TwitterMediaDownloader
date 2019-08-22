![](https://img.shields.io/github/last-commit/11philip22/twitter-media-downloader)

# twitter-media-downloader
Downloads photos and videos from twitter. <br/>
Tested with python3.7 :) <br/>
If you have questions, requests or ideas send me a mail or open an issue.
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
- [ ] Write queue to file when exit
- [ ] Detect if the photo is already downloaded before making a request (maybe with the id or something)
- [x] Make crawling and downloading run at the same time.
- [ ] Only ignore 403 Error while downloading videos. (does youtube dl only output errors as a string or am i retarded?)
- [ ] When the program stops while downloading photos write the id of the last downloaded photo to the resume file so the crawler knows where it left off.
