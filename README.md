# git-trend
A command line utility for getting the trending (top N) Repositories and Developers on GitHub.

- **Repositories** - The tool will print details such as the  name, owner, stars and the language of the repository.
- **Developers** - The tool will print details of the trending developer such as their username, name, their trending repository.

View it on PyPI at: https://pypi.org/project/git-trend/

### Installation

This tool has been built with python3. You need to install Python3.x for this utility.
Install this tool from PyPI (The Python Package Index) using pip

```shell
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

Currently, the supported languages are: Python, Ruby, C, C++, Java, Scala, Kotlin, Javascript, TypeScript, Go, Rust, Lua, Haskell