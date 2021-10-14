# Change Log


## 1.2

Released on October 14, 2021

### Added

* Cache read news in local SQL database (optional arguments --date and --clean)
* New tests for new functionality

### Changed

* Split urlparse errors into: no scheme in source URL and no host in source URL 
* Convert non-ascii source URL to ASCII character-set
* Change urlopen mechanism from urlopen(url) to urlopen(Request(url, headers))
* Change strip_html function to strip_text (add stripping of excessive whitespaces and HTML entities, limit text to no more than 1000 characters)
* If item's image is not in tag 'enclosure', search it in tag 'description' or namespaces' tags. If none is found try to add channel's image or root's image
* Replace relative URLs of image link and news page link with absolute URLs
* Ensure that necessary tags are not empty if present 
* Modify dict_to_string function to be able to receive news from cache for particular date
* Update docstrings in rss_reader.py and tests.py
* Update README.md, CHANGELOG.md, .gitignore


## 1.1

Released on October 10, 2021

### Added

* Wrap program into distribution package (pyproject.toml, setup.cfg, /dist/)
* Add CHANGELOG.md, LICENSE, .gitignore

### Changed

* Build a package `rss_reader` for the main program script (/src/rss_reader/)
* Build a package `tests` for the tests script (/tests/)
* Update README.md
* Update import path of the main program script in tests.py
* Update docstrings in rss_reader.py and tests.py


## 1.0

Released on October 06, 2021

### Added

* First version of the pure Python command-line RSS reader, containing:
	- Main program script (rss_reader.py)
	- Tests script (tests.py)
	- README.md