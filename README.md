![](https://img.shields.io/github/last-commit/11philip22/twitter-media-downloader)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

# twitter-media-downloader
Downloads photos and videos from twitter. <br/>
Tested with python3.7 :) <br/>
If you have questions, requests or ideas send me a mail or open an issue.
# Usage
### Use as program
Get prompted for input:
```
python3 core.py
```
Use a list:
```
python3 core.py list.txt
```
Dont use the username but the whole link. Like this: https://twitter.com/twitter
## Use the Twitter class in your own python program
``` python
from twitter import Twitter


usernames = ["username1", "username2", "username3"]
location = "../Downloads/"
t = Twitter(usernames=usernames, location=location)
t.start()
```
Note: the location need to have a trailing /
### todo:
- [ ] Write queue to file when exit
- [ ] Detect if the photo is already downloaded before making a request (maybe with the id or something)
- [x] Make crawling and downloading run at the same time.
- [ ] Only ignore 403 Error while downloading videos. (does youtube dl only output errors as a string or am i retarded?)
- [ ] When the program stops while downloading photos write the id of the last downloaded photo to the resume file so the crawler knows where it left off.
- [ ] Use pathlib or something so you can use it on Windows
