# Change Log


## 1.3

Released on October 21, 2021

### Added

* Convert information to HTML and PDF formats and write it to a local file (optional arguments --to-html and --to-pdf)

### Changed

* Change package folder structure 
* Split rss_reader.py into several modules
* Input arguments are parsed into dictionary instead of argparse.Namespace object
* Update news item in cache if it changed on site (url must remain the same, or the new item will be added)
* Catch errors when working with SQL database
* Increase logging functionality
* Update all docstrings
* Update README.md, CHANGELOG.md, .gitignore, setup.cfg


## 1.2

Released on October 14, 2021

### Added

* Cache read news in local SQL database (optional arguments --date and --clean)

### Changed

* Split urlparse errors into: no scheme in source URL and no host in source URL 
* Convert non-ascii source URL to ASCII character-set
* Change urlopen mechanism from urlopen(url) to urlopen(Request(url, headers))
* Change strip_html function to strip_text (add stripping of excessive whitespaces and HTML entities, limit text to no more than 1000 characters)
* If item's image is not in tag 'enclosure', search it in tag 'description' or namespaces' tags. If none is found try to add channel's image or root's image
* Replace relative URLs of image link and news page link with absolute URLs
* Handle situation when necessary tags in XML are present but empty 
* Modify dict_to_string function to be able to receive news from cache for particular date
* Update all docstrings
* Update README.md, CHANGELOG.md, .gitignore, setup.cfg


## 1.1

Released on October 10, 2021

### Added

* Wrap program into distribution package (pyproject.toml, setup.cfg, /dist/)
* Add CHANGELOG.md, LICENSE, .gitignore

### Changed

* Build a package `rss_reader` for the main program script (/src/rss_reader/)
* Build a package `tests` for the tests script (/tests/)
* Update import path of the main program script in tests.py
* Update all docstrings
* Update README.md


## 1.0

Released on October 06, 2021

### Added

* First version of the pure Python command-line RSS reader, containing:
	- Main program script (rss_reader.py)
	- Tests script (tests.py)
	- README.md