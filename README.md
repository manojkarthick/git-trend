# git-trend [![PyPI version](https://badge.fury.io/py/git-trend.svg)](https://badge.fury.io/py/git-trend) ![build](https://github.com/manojkarthick/git-trend/workflows/build/badge.svg) 

A command line utility for getting trending repositories and developers on GitHub.

- **Repositories** - The tool will print details such as the  name, owner, stars and the language of the repository.
- **Developers** - The tool will print details of the trending developer such as their username, name, their trending repository.

View it on PyPI at: https://pypi.org/project/git-trend/

### Installation

This tool has been built with python3. You need to install Python3.x for this utility.
Install this tool from PyPI (The Python Package Index) using pip:

```shell
$ pip install git-trend 
```
**NOTE**: Support for Python 2 is no longer available. For best experience, please use a terminal with unicode support.

### Options

The utility can fetch trending data for the overall site. In case you are interested in a particular language, use the language flag.

```
optional arguments:
  -h, --help            show this help message and exit
  --repos               to view trending repositories
  --devs                to view trending developers
  --period {daily,weekly,monthly}
                        time period of results
  --language <language_code>
                        the language whose trends you want to fetch. Use --languages flag to see supported languages.
  --spoken-language <spoken_language_code>
                        spoken language you want to filter results on. Use --spoken-languages flag to see supported spoken languages.
  --format {default,table,json}
                        Output format
  --languages           print list of languages supported
  --spoken-languages    print list of spoken languages supported
  --version             Package version
```

* Supported Output formats: default, table, json.
* Supported Languages: Run `git-trend --languages` to see list of supported languages
* Supported Spoken languages: Run `git-trend --spoken-languages` to see list of supported spoken languages

### Sample Output

#### List of trending git repositories

```
$ git-trend --repos

➜ facebookresearch/deit [Python, ★ 561]:  Official DeiT repository
➜ iptv-org/iptv [JavaScript, ★ 23,067]:  Collection of 5000+ publicly available IPTV channels from all over the world
➜ inancgumus/learngo [Go, ★ 6,730]:  1000+ Hand-Crafted Go Examples, Exercises, and Quizzes
➜ huanghyw/jd_seckill [Python, ★ 411]:  京东秒杀商品抢购，目前只支持茅台抢购，不支持其他商品！
➜ microsoft/Web-Dev-For-Beginners [JavaScript, ★ 8,640]:  24 Lessons, 12 Weeks, Get Started as a Web Developer
➜ ruby/ruby [Ruby, ★ 17,720]:  The Ruby Programming Language [mirror]
➜ netdata/netdata [C, ★ 50,756]:  Real-time performance monitoring, done right! https://www.netdata.cloud
➜ werner-duvaud/muzero-general [Python, ★ 717]:  MuZero
..... <output shortened>
````

#### List of trending developers

```
$ git-trend --devs

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

#### List of trending repositories using Rust in table format

```
$ git-trend --repos --language rust --format table

+------+----------------------------+-----------------------------------------------+----------+--------+
| Rank | Repository                 | URL                                           | Language | Stars  |
+------+----------------------------+-----------------------------------------------+----------+--------+
| 1    | sfackler/rust-postgres     | https://github.com/sfackler/rust-postgres     | Rust     | 1,977  |
| 2    | yewstack/yew               | https://github.com/yewstack/yew               | Rust     | 14,328 |
| 3    | paritytech/substrate       | https://github.com/paritytech/substrate       | Rust     | 3,503  |
| 4    | tauri-apps/tauri           | https://github.com/tauri-apps/tauri           | Rust     | 7,640  |
| 5    | paritytech/polkadot        | https://github.com/paritytech/polkadot        | Rust     | 1,848  |
| 6    | Geal/nom                   | https://github.com/Geal/nom                   | Rust     | 4,688  |
|                                                                                                       |
| ............................................< output shortened >....................................  |
|                                                                                                       |
| 25   | redox-os/orbtk             | https://github.com/redox-os/orbtk             | Rust     | 2,806  |
+------+----------------------------+-----------------------------------------------+----------+--------+
```

#### List of trending repositories using Scala this week in JSON format

```
$ git-trend --devs --language scala --format json --period weekly

{
    "Thibault Duplessis": {
        "rank": 1,
        "user_id": "ornicar",
        "repository": "lila",
        "description": "\u265e lichess.org: the forever free, adless and open source chess server \u265e",
        "url": "https://github.com/ornicar"
    },
    "Frank S. Thomas": {
        "rank": 2,
        "user_id": "fthomas",
        "repository": "refined",
        "description": "Simple refinement types for Scala",
        "url": "https://github.com/fthomas"
    },
    "P. Oscar Boykin": {
        "rank": 3,
        "user_id": "johnynek",
        "repository": "bosatsu",
        "description": "A python-ish pure and total functional programming language",
        "url": "https://github.com/johnynek"
    },
    .
    . 
    . <output shortened>
    .
    .
    "Fabio Labella": {
        "rank": 11,
        "user_id": "SystemFw",
        "repository": "Scala-World-2019",
        "description": "",
        "url": "https://github.com/SystemFw"
    }
}

```

### TODO

* [x] JSON output format support
* [x] Hyperlink support
* [x] Table output support
* [x] Support for Spoken language filter
* [x] Support for all languages available from GitHub
* [x] Subclasses

