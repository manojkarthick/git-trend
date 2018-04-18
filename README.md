# git-trend v0.2
A command line utility for getting the trending(top 10) Repositories and Developers at GitHub.

View it on PyPI at: https://pypi.python.org/pypi/git-trend/0.2

**Repositories** - The tool will print details such as the  name, owner, stars and the language of the repository.

**Developers** - The tool will print details of the trending developer such as their username, name, their trending repository.

### Installation
This tool has been built with python3. You need to install Python3.x for this utility.
Install this tool from PyPI (The Python Package Index) using pip
```shell
# If Python 3.x is not your primary version of python, then use
$ pip3 install git-trend 

#If Python3 is your default python version, then use
$ pip install git-trend
```
**NOTE**:   You can check your python version using `python -V`. Please use a terminal with unicode support for best results.

### Options
The utility can fetch trending data for the overall site. In case you are interested in a particular language. Use the language option.
```
-h, --help                  Print the help text
--repos                     Get the details of the trending repositories
--devs                      Get the details of the trending developers
--period PERIOD             Period refers to the time period over which the results are available
                            The options available are daily, weekly, monthy. Defaults to daily.
--language LANGUAGE         The utility supports getting trending details of repositories and 
                            developers of a particular language. Optional, by default fetches  overall trending statistics
--languages                 Get the list of supported languages
```

Currently, the supported languages are: Python, Ruby, C, C++, Java, Javascript, go, rust, lua, haskell