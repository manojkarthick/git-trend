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
**NOTE**: Support for Python 2 is no longer available. For best experience, please use a terminal with unicode support for best results.

### Options

The utility can fetch trending data for the overall site. In case you are interested in a particular language. Use the language option.

```shell
-h, --help                  Print the help text
--repos                     Get the details of the trending repositories
--devs                      Get the details of the trending developers
--period PERIOD             Period refers to the time period over which the results are available
                            The options available are daily, weekly, monthy. Defaults to daily.
--language LANGUAGE         The utility supports getting trending details of repositories and 
                            developers of a particular language. Optional, by default fetches  overall trending statistics
--languages                 Get the list of supported languages
```

### Sample Output

```shell
$ git-trend --repos

Fetching data from https://github.com/trending?since=daily. Please wait....

➜ facebookresearch/deit [Python, ★ 561]:  Official DeiT repository
➜ iptv-org/iptv [JavaScript, ★ 23,067]:  Collection of 5000+ publicly available IPTV channels from all over the world
➜ inancgumus/learngo [Go, ★ 6,730]:  1000+ Hand-Crafted Go Examples, Exercises, and Quizzes
➜ huanghyw/jd_seckill [Python, ★ 411]:  京东秒杀商品抢购，目前只支持茅台抢购，不支持其他商品！
➜ microsoft/Web-Dev-For-Beginners [JavaScript, ★ 8,640]:  24 Lessons, 12 Weeks, Get Started as a Web Developer
➜ ruby/ruby [Ruby, ★ 17,720]:  The Ruby Programming Language [mirror]
➜ netdata/netdata [C, ★ 50,756]:  Real-time performance monitoring, done right! https://www.netdata.cloud
➜ werner-duvaud/muzero-general [Python, ★ 717]:  MuZero
..... <output shortened>


$ git-trend --devs

Fetching data from https://github.com/trending/developers?since=daily. Please wait....

➜ Jan De Dobbeleer (JanDeDobbeleer)
  oh-my-posh: A prompt theming engine for Powershell
➜ Sean McArthur (seanmonstar)
  reqwest: An easy and powerful Rust HTTP Client
➜ Dan Davison (dandavison)
  delta: A viewer for git and diff output
➜ Steve Purcell (purcell)
  emacs.d: An Emacs configuration bundle with batteries included
➜ Ariel Mashraki (a8m)
  golang-cheat-sheet: An overview of Go syntax and features.
➜ Arvid Norberg (arvidn)
  libtorrent: an efficient feature complete C++ bittorrent implementation
➜ Matthias Urhahn (d4rken)
  sdmaid-public: SD Maid is an Android app that helps you manage files and apps.
..... <output shortened>

```

Currently, only the following languages are supported: Python, Ruby, C, C++, Java, Scala, Kotlin, Javascript, TypeScript, Go, Rust, Lua, Haskell


### TODO

[ ] Support for Spoken language filter
[ ] Support for all languages available from GitHub

