# Pure Python command-line RSS reader


### Homework for EPAM Python Training 2021.09


### Author: Nickolai Lychagin, belarusconsul@gmail.com
### Version 1.2, 14.10.2021

> This program:
> 
> - downloads information from RSS news feed
> - processes various data from news items (title, description, date, image, link)
> - prints data to console in text or JSON format 
> - stores downloaded data to local cache file in SQL format
>
> It supports all news feeds that fully comply with RSS 2.0 Specification. Correct operation on other RSS channels is not guaranteed. 

---
## INSTALLATION

The program is written in Python 3.9 with it's standard library. Installation of additional modules is not required.

1. Clone repository to your local drive:<br>
   `git clone https://github.com/belarusconsul/Homework.git`

2. You can run this program without installation. The executable script is in the master branch:<br>
   *<path to /Homework/NickolaiLychagin/src/rss_reader/rss_reader.py>*
   
3. Install prebuilt package to your computer:<br>
   **Windows:**<br>
   `py -m pip install <path to /Homework/NickolaiLychagin/dist/rss_reader-1.2-py3-none-any.whl>`<br>
   **Unix/MacOS:**<br>
   `python3 -m pip install <path to /Homework/NickolaiLychagin/dist/rss_reader-1.2-py3-none-any.whl>`<br>

   This installs program from a Wheel file (built distribution). If you prefer to use a Source Distribution file (source archive) run:<br>
   **Windows:**<br>
   `py -m pip install <path to /Homework/NickolaiLychagin/dist/rss_reader-1.2.tar.gz>`<br>
   **Unix/MacOS:**<br>
   `python3 -m pip install <path to /Homework/NickolaiLychagin/dist/rss_reader-1.2.tar.gz>`<br>

   After that you can run program through CLI utility rss_reader.

4. If you want to build the distribution package yourself, go to *<path to /Homework/NickolaiLychagin/>* in the master branch and run:<br>
   **Windows:**<br>
   `py -m build`<br>
   **Unix/MacOS:**<br>
   `python3 -m build`
 
---
## USAGE

1. Without installation:<br>
	**Windows:**<br>
	`rss_reader.py <arguments>` (run from directory with rss_reader.py) or<br>
	`py -m rss_reader <arguments>` (if directory with rss_reader.py is in sys.path)<br>
	**Unix/MacOS:**<br>
	`python3 rss_reader.py <arguments>`(run from directory with rss_reader.py) or<br>
	`python3 -m rss_reader <arguments>`(if directory with rss_reader.py is in sys.path)<br>

2. With installation of CLI utility:<br>
	**Windows/Unix/MacOS:**<br>
	`rss_reader <arguments>`

```
    Example usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--clean] [source]

    positional arguments:
      source         RSS URL

    optional arguments:
      -h, --help     show this help message and exit
      --version      Print version info
      --json         Print result as JSON in stdout
      --verbose      Outputs verbose status messages
      --limit LIMIT  Limit news topics if this parameter provided
      --date DATE    Date formatted as YYYYMMDD
      --clean        Clean all data from cache file
```

---
## CACHE

News items retrieved from source URL are stored in a local SQL database in the 'news' table created as follows:
```
CREATE TABLE news
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
   channel TEXT, 
   url TEXT, 
   title TEXT, 
   date TEXT,
   date_as_date DATE, 
   desc TEXT, 
   image TEXT, 
   link TEXT,
   UNIQUE(channel, url, title, date, desc, image, link))
```
If a news item does not have date or date is in the wrong format, it is saved to cache with the date "19000101" (January 1, 1900).

---
## SAMPLE OUTPUT

> In text format:
1. From URL:
```
Feed: The Latest News from the UK and Around the World | Sky News
Description: Sky news delivers breaking news, headlines and top stories from business, politics, entertainment and more in the UK and worldwide.
URL: https://feeds.skynews.com/feeds/rss/home.xml

Title: Man kills five with bow and arrows in Norway before 'confrontation' with police
Date: Wed, 13 Oct 2021 19:54:00 +0100
Image: https://e3.365dm.com/21/10/70x70/skynews-kongsberg-arrow_5545741.jpg?20211013220801
Detail: Five people have been killed and others - including an off-duty police officer - were injured in a series of bow and arrow attacks in Norway, according to police.
Read more: http://news.sky.com/story/norway-bow-and-arrow-attacks-five-killed-in-kongsberg-before-suspect-in-confrontation-with-police-12433212

Title: EU offers to cut 80% of GB-Northern Ireland checks on some goods to end 'sausage war'
Date: Wed, 13 Oct 2021 14:52:00 +0100
Image: https://e3.365dm.com/21/10/70x70/skynews-comp-larne_5545586.jpg?20211013184651
Detail: The EU has offered to cut 80% of checks on some goods moving from Great Britain to Northern Ireland in an effort to avoid a post-Brexit trade clash.
Read more: http://news.sky.com/story/brexit-eu-offers-to-cut-80-of-gb-northern-ireland-checks-on-some-goods-to-end-sausage-war-12433021
```
2. From cache file:
```
Cached news items for date 'October 13, 2021'

Title: Man kills five with bow and arrows in Norway before 'confrontation' with police
Channel: The Latest News from the UK and Around the World | Sky News
Channel URL: https://feeds.skynews.com/feeds/rss/home.xml
Date: Wed, 13 Oct 2021 19:54:00 +0100
Image: https://e3.365dm.com/21/10/70x70/skynews-kongsberg-arrow_5545741.jpg?20211013220801
Detail: Five people have been killed and others - including an off-duty police officer - were injured in a series of bow and arrow attacks in Norway, according to police.
Read more: http://news.sky.com/story/norway-bow-and-arrow-attacks-five-killed-in-kongsberg-before-suspect-in-confrontation-with-police-12433212

Title: EU offers to cut 80% of GB-Northern Ireland checks on some goods to end 'sausage war'
Channel: The Latest News from the UK and Around the World | Sky News
Channel URL: https://feeds.skynews.com/feeds/rss/home.xml
Date: Wed, 13 Oct 2021 14:52:00 +0100
Image: https://e3.365dm.com/21/10/70x70/skynews-comp-larne_5545586.jpg?20211013184651
Detail: The EU has offered to cut 80% of checks on some goods moving from Great Britain to Northern Ireland in an effort to avoid a post-Brexit trade clash.
Read more: http://news.sky.com/story/brexit-eu-offers-to-cut-80-of-gb-northern-ireland-checks-on-some-goods-to-end-sausage-war-12433021
```

> In JSON format:
1. From URL:
```
{
    "Channel": {
        "Title": "The Latest News from the UK and Around the World | Sky News",
        "Description": "Sky news delivers breaking news, headlines and top stories from business, politics, entertainment and more in the UK and worldwide.",
        "URL": "https://feeds.skynews.com/feeds/rss/home.xml"
    },
    "News 1": {
        "Title": "Man kills five with bow and arrows in Norway before 'confrontation' with police",
        "Date": "Wed, 13 Oct 2021 19:54:00 +0100",
        "Image": "https://e3.365dm.com/21/10/70x70/skynews-kongsberg-arrow_5545741.jpg?20211013220801",
        "Description": "Five people have been killed and others - including an off-duty police officer - were injured in a series of bow and arrow attacks in Norway, according to police.",
        "Link": "http://news.sky.com/story/norway-bow-and-arrow-attacks-five-killed-in-kongsberg-before-suspect-in-confrontation-with-police-12433212"
    },
    "News 2": {
        "Title": "EU offers to cut 80% of GB-Northern Ireland checks on some goods to end 'sausage war'",
        "Date": "Wed, 13 Oct 2021 14:52:00 +0100",
        "Image": "https://e3.365dm.com/21/10/70x70/skynews-comp-larne_5545586.jpg?20211013184651",
        "Description": "The EU has offered to cut 80% of checks on some goods moving from Great Britain to Northern Ireland in an effort to avoid a post-Brexit trade clash.",
        "Link": "http://news.sky.com/story/brexit-eu-offers-to-cut-80-of-gb-northern-ireland-checks-on-some-goods-to-end-sausage-war-12433021"
    }
}
```
2. From cache file:
```
{
    "News 1": {
        "Title": "Man kills five with bow and arrows in Norway before 'confrontation' with police",
        "Channel": "The Latest News from the UK and Around the World | Sky News",
        "Channel URL": "https://feeds.skynews.com/feeds/rss/home.xml",
        "Date": "Wed, 13 Oct 2021 19:54:00 +0100",
        "Image": "https://e3.365dm.com/21/10/70x70/skynews-kongsberg-arrow_5545741.jpg?20211013220801",
        "Description": "Five people have been killed and others - including an off-duty police officer - were injured in a series of bow and arrow attacks in Norway, according to police.",
        "Link": "http://news.sky.com/story/norway-bow-and-arrow-attacks-five-killed-in-kongsberg-before-suspect-in-confrontation-with-police-12433212"
    },
    "News 2": {
        "Title": "EU offers to cut 80% of GB-Northern Ireland checks on some goods to end 'sausage war'",
        "Channel": "The Latest News from the UK and Around the World | Sky News",
        "Channel URL": "https://feeds.skynews.com/feeds/rss/home.xml",
        "Date": "Wed, 13 Oct 2021 14:52:00 +0100",
        "Image": "https://e3.365dm.com/21/10/70x70/skynews-comp-larne_5545586.jpg?20211013184651",
        "Description": "The EU has offered to cut 80% of checks on some goods moving from Great Britain to Northern Ireland in an effort to avoid a post-Brexit trade clash.",
        "Link": "http://news.sky.com/story/brexit-eu-offers-to-cut-80-of-gb-northern-ireland-checks-on-some-goods-to-end-sausage-war-12433021"
    }
}
```