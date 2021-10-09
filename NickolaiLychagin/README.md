# Pure Python command-line RSS reader


### Homework for EPAM Python Training 2021.09


### Author: Nickolai Lychagin, belarusconsul@gmail.com
### Version 1.1, 10.10.2021

> This program:
> 
> - downloads information from RSS news feed
> - processes various data from news items (title, description, date, image, link)
> - prints data to console in text or JSON format 

---
## INSTALLATION

1. Clone repository to your local drive:<br>
   `git clone https://github.com/belarusconsul/Homework.git`

2. You can run this program without installation. The executable script is in the master branch:<br>
   *<path to /Homework/NickolaiLychagin/src/rss_reader/rss_reader.py>*
   
3. Install prebuilt package to your computer:<br>
   **Windows:**<br>
   `py -m pip install <path to /Homework/NickolaiLychagin/dist/rss_reader-1.1-py3-none-any.whl>`<br>
   **Unix/MacOS:**<br>
   `python3 -m pip install <path to /Homework/NickolaiLychagin/dist/rss_reader-1.1-py3-none-any.whl>`<br>

   This installs program from a Wheel file (built distribution). If you prefer to use a Source Distribution file (source archive) run:<br>
   **Windows:**<br>
   `py -m pip install <path to /Homework/NickolaiLychagin/dist/rss_reader-1.1.tar.gz>`<br>
   **Unix/MacOS:**<br>
   `python3 -m pip install <path to /Homework/NickolaiLychagin/dist/rss_reader-1.1.tar.gz>`<br>

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
	`rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source` (run from directory with rss_reader.py) or<br>
	`py -m rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] source` (if directory with rss_reader.py is in sys.path)<br>
	**Unix/MacOS:**<br>
	`python3 rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source`(run from directory with rss_reader.py) or<br>
	`python3 -m rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] source`(if directory with rss_reader.py is in sys.path)<br>

2. With installation of CLI utility:<br>
	**Windows/Unix/MacOS:**<br>
	`rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] source`

```
    positional arguments:
      source         RSS URL

    optional arguments:
      -h, --help     show this help message and exit
      --version      Print version info
      --json         Print result as JSON in stdout
      --verbose      Outputs verbose status messages
      --limit LIMIT  Limit news topics if this parameter provided
```


---

## SAMPLE OUTPUT


> In text format:
```
Feed: The Latest News from the UK and Around the World | Sky News
Description: Sky news delivers breaking news, headlines and top stories from business, politics, entertainment and more in the UK and worldwide.

Title: Boris Johnson to launch attack on former Tory PMs in promise to tackle big issues
Date: Tue, 05 Oct 2021 22:09:00 +0100
Image: https://e3.365dm.com/21/10/70x70/skynews-speech-conservative_5536049.jpg?20211005145733
Boris Johnson will close his party's conference in a rousing finale in which he will accuse his Tory predecessors of "drift and dither" and lacking the guts to tackle big problems.
Read more: http://news.sky.com/story/conservative-party-conference-boris-johnson-to-launch-attack-on-former-tory-pms-in-promise-to-tackle-big-issues-12426949

Title: Facebook 'operates in shadows' - and Instagram is worse than other social sites, whistleblower tells Congress
Date: Tue, 05 Oct 2021 14:40:00 +0100
Image: https://e3.365dm.com/21/10/70x70/skynews-frances-haugen-facebook-whistleblower_5536168.jpg?20211005163325
Facebook's products "harm children, stoke division and weaken our democracy", a whistleblower has claimed.
Read more: http://news.sky.com/story/facebook-whistleblower-frances-haugen-tells-congress-hearing-tackle-the-company-like-big-tobacco-12426665
```


> In JSON format:
```
{
    "Channel": {
        "Title": "The Latest News from the UK and Around the World | Sky News",
        "Description": "Sky news delivers breaking news, headlines and top stories from business, politics, entertainment and more in the UK and worldwide."
    },
    "News 1": {
        "Title": "Boris Johnson to launch attack on former Tory PMs in promise to tackle big issues",
        "Date": "Tue, 05 Oct 2021 22:09:00 +0100",
        "Image": "https://e3.365dm.com/21/10/70x70/skynews-speech-conservative_5536049.jpg?20211005145733",
        "Description": "Boris Johnson will close his party's conference in a rousing finale in which he will accuse his Tory predecessors of \"drift and dither\" and lacking the guts to tackle big problems.",
        "Link": "http://news.sky.com/story/conservative-party-conference-boris-johnson-to-launch-attack-on-former-tory-pms-in-promise-to-tackle-big-issues-12426949"
    },
    "News 2": {
        "Title": "Facebook 'operates in shadows' - and Instagram is worse than other social sites, whistleblower tells Congress",
        "Date": "Tue, 05 Oct 2021 14:40:00 +0100",
        "Image": "https://e3.365dm.com/21/10/70x70/skynews-frances-haugen-facebook-whistleblower_5536168.jpg?20211005163325",
        "Description": "Facebook's products \"harm children, stoke division and weaken our democracy\", a whistleblower has claimed.",
        "Link": "http://news.sky.com/story/facebook-whistleblower-frances-haugen-tells-congress-hearing-tackle-the-company-like-big-tobacco-12426665"
    }
}
```