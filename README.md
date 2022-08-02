# Imgur Crawler
***(ONLY FOR EDUCATIONAL PURPOSES)***

Crawls pictures and videos from [imgur.com](https://imgur.com) at full resolution

## Features
* Getting maximum resolution of image/video
* Asynchronous requests using [grequests](https://pypi.org/project/grequests/)
* Readable code, so you can fork it and modify for yourself
* Ids of images/videos saving to database, so downloaded images will not be downloaded again.
* You can dump database using Python script "make_dump_of_db.py"

## Installation
### Linux
```
sudo apt update && sudo apt upgrade
sudo apt-get install git python3
git clone https://github.com/ntexe/imgur-crawler.git
cd imgur-crawler
pip3 install requirements.txt
```
### Termux
```
pkg update && pkg upgrade
pkg install git python3
git clone https://github.com/ntexe/imgur-crawler.git
cd imgur-crawler
pip3 install requirements.txt
```
### Windows
Download ZIP archive and unpack it using winrar/7z or other software

![image](https://user-images.githubusercontent.com/82678562/182241806-9df91772-2c41-4dc2-be35-49a7d0a9fffc.png)

Then install Python (google how to do it)

<ins>**Be sure to click the "Add Python to PATH" checkbox**</ins>

![image](https://miro.medium.com/max/1282/1*ecMIFT0gDLcLRD1y5q8_Tg.png)

Then shift-click in the folder where you unpacked archive and click "Open Powershell window here"

![image](https://user-images.githubusercontent.com/82678562/182243232-3d75e91f-31d2-44cb-bdbf-1f02bc2e674f.png)

Write in powershell this line
```
pip install requirements.txt
```

## Usage
### Linux
```
cd imgur-crawler
python3 main.py [links per function call]
```
**Termux is the same**
### Windows

Shift-click in the folder where you unpacked archive and click "Open Powershell window here"

![image](https://user-images.githubusercontent.com/82678562/182243232-3d75e91f-31d2-44cb-bdbf-1f02bc2e674f.png)

Write in powershell this line
```
python main.py [links per function call]
```

Tested on
* Windows 10 21H2 Python 3.10.2
* Termux Python 3.10.4
