import json
from argparse import ArgumentParser
from collections import OrderedDict

import pkg_resources
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from termcolor import colored


class Colors(object):
    GREEN = 'green'
    RED = 'red'
    BLUE = 'blue'
    YELLOW = 'yellow'


class Constants(object):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    REPOSITORIES = "repositories"
    DEVELOPERS = "developers"


SUPPORTED_LANGUAGES = [
    'python',
    'ruby',
    'c',
    'c++',
    'java',
    'scala',
    'kotlin',
    'javascript',
    'typescript',
    'go',
    'rust',
    'lua',
    'haskell'
]


def strip_and_get(val, fallback=""):
    """
    Return the enclosing text or provided fallback value
    :param val: item to get text and strip whitespace
    :param fallback: fallback when val is None
    :return: stripped text value
    """
    if val:
        return val.text.strip(' \t\n\r')
    else:
        return fallback


def get_url(content_type, period, language=None):
    """
    Get URLs for repository/developer information with optional time period
    :param content_type: Type of content to return
    :param period: time period to query for
    :param language: language to filter on
    :return: URL for processing
    """

    return "https://github.com/trending{t}{l}since={p}".format(
        t="" if content_type == Constants.REPOSITORIES else "/{}".format(Constants.DEVELOPERS),
        p=period,
        l="?" if not language else "/{}?".format(language)
    )


def get_github_soup(content_type, period, lang):
    """
    Parse web page using BeautifulSoup's HTML parser
    :param urls: Dictionary containing queryable URLs
    :param content_type: Type of parser (repos, devs)
    :param period: Time period (daily, weekly, monthly)
    :return: parsed html content
    """
    url = get_url(content_type, period, lang)
    try:
        req = requests.get(url)
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out while querying the URL: {}".format(url))
        print("Please check if the URL is valid.")
        exit(1)
    except requests.exceptions.TooManyRedirects:
        print("ERROR: Too many redirects when querying the URL: {}".format(url))
        print("Please check if the URL is valid.")
    except requests.exceptions.RequestException as e:
        print("ERROR: Could not get the requested page: {}".format(url))
        raise SystemExit(e)

    page_content = req.text
    try:
        soup = BeautifulSoup(page_content, 'html.parser')
    except ImportError:
        print("ERROR: No HTML parser found. Please check your install of BeautifulSoup")
        exit(1)
    except Exception as e:
        raise SystemExit(e)

    return soup


def get_repositories(list_items):
    """
    Get repository name, description, language and stars
    :param list_items: Contains list of DOM elements containing repo information
    :return: K-V of repository information
    """
    trending = OrderedDict()
    for index, item in enumerate(list_items):
        repo_organization, repo_name = item.find("h1", class_="h3 lh-condensed").text.strip(' \t\n\r').split("/")
        repository = "{}/{}".format(repo_organization.strip(), repo_name.strip())

        repo_desc_info = item.find("p", class_="col-9 text-gray my-1 pr-4")
        language_info = item.find("span", itemprop="programmingLanguage")
        stars_info = item.find("a", class_="muted-link d-inline-block mr-3")

        repo_desc = strip_and_get(repo_desc_info)
        repo_language = strip_and_get(language_info)
        repo_stars = strip_and_get(stars_info)

        trending[repository] = {
            "rank": index + 1,
            "description": repo_desc,
            "language": repo_language,
            "stars": repo_stars,
            "url": "https://github.com/{}".format(repository.strip())
        }

    return trending


def get_developers(list_items):
    """
    Get developer name, id, repo name and description
    :param list_items: Contains list of DOM elements containing developer information
    :return: K-V of developer information
    """
    trending = OrderedDict()
    for index, item in enumerate(list_items):
        container = item.find("div", class_="col-sm-8 d-md-flex")

        user_name = container.find("h1", class_="h3 lh-condensed").text.strip(' \t\n\r')
        user_id_info = container.find("p", class_="f4 text-normal mb-1")
        repo_desc_info = item.find("div", class_="f6 text-gray mt-1")
        repo_name_info = item.find("h1", class_="h4 lh-condensed")

        user_id = strip_and_get(user_id_info, user_name)
        repo_name = strip_and_get(repo_name_info)
        repo_desc = strip_and_get(repo_desc_info)

        trending[user_name] = {
            "rank": index + 1,
            "user_id": user_id,
            "repository": repo_name,
            "description": repo_desc,
            "url": "https://github.com/{}".format(user_id)
        }

    return trending


def print_repositories(trending, format_="default"):
    """
    Print trending repositories in the requested output format
    :param trending: List of trending items
    :param format_: output format to use
    :return:
    """
    if format_ == "default":
        for key, value in trending.items():
            repo_name = key
            description = value["description"] if value["description"] != "" else "<Unknown Description>"
            language = value["language"] if value["language"] != "" else "<Unknown Language>"
            stars = value["stars"]
            print("➜ {} [{}, ★ {}]:  {}".format(colored(repo_name, Colors.GREEN),
                                                colored(language, Colors.BLUE),
                                                colored(stars, Colors.YELLOW),
                                                colored(description, Colors.RED)))
    elif format_ == "json":
        print(json.dumps(trending, indent=4))
    elif format_ == "table":
        tbl = PrettyTable()
        tbl.field_names = ["Rank", "Repository", "URL", "Language", "Stars"]
        for key, value in trending.items():
            repo_name = key
            url = value["url"]
            rank = value["rank"]
            language = value["language"]
            stars = value["stars"]
            tbl.add_row([rank, repo_name, url, language, stars])
        tbl.align = "l"
        print(tbl)
    else:
        print("Unknown format")


def print_developers(trending, format_="default"):
    """
    Print trending developers in the requested output format
    :param trending: List of trending items
    :param format_: output format to use
    :return:
    """
    if format_ == "default":
        for key, value in trending.items():
            user_name = key
            user_id = value["user_id"] if value["user_id"] != "" else "<Unknown>"
            repository = value["repository"] if value["repository"] != "" else "<Unknown Repository>"
            description = value["description"] if value["description"] != "" else "<Unknown Description>"
            print("➜ {} ({})\n  {}: {}".format(colored(user_name, Colors.GREEN),
                                               colored(user_id, Colors.GREEN),
                                               colored(repository, Colors.BLUE),
                                               colored(description, Colors.RED)))
    elif format_ == "json":
        print(json.dumps(trending, indent=4))
    elif format_ == "table":
        tbl = PrettyTable()
        tbl.field_names = ["Rank", "User", "User ID", "URL", "Repository"]
        for key, value in trending.items():
            user_name = key
            rank = value["rank"]
            user_id = value["user_id"]
            url = value["url"]
            repository = value["repository"]
            tbl.add_row([rank, user_name, user_id, url, repository])
        tbl.align = "l"
        print(tbl)
    else:
        print("Unknown format")


def check_if_list_valid(list_items, content_type):
    if len(list_items) < 1:
        print("Could not get trending {} from the page.".format(content_type))
        print("ERROR: Raise an issue on https://github.com/manojkarthick/git-trend/issues")
        exit(1)


def cli():
    parser = ArgumentParser(
        description='This tool allows you to look at Github trending repositories and developers')
    parser.add_argument('--repos', action='store_true', help='to view trending repositories')
    parser.add_argument('--devs', action='store_true', help='to view trending developers')
    parser.add_argument('--period', type=str, choices=["daily", "monthly", "weekly"], default='daily',
                        help='time period of results')
    parser.add_argument('--language', type=str, default=None, help='the language whose trends you want to fetch',
                        choices=SUPPORTED_LANGUAGES)
    parser.add_argument("--format", type=str, choices=["default", "json", "table"], default="default",
                        help="Output format")
    parser.add_argument('--languages', action='store_true', help='print list of languages supported')
    parser.add_argument('--version', action='store_true', help="Package version")
    args = parser.parse_args()

    if args.version:
        print("git-trend v{}".format(pkg_resources.require("git-trend")[0].version))
        exit(0)

    if args.languages:
        if args.repos or args.devs or args.language:
            print('ERROR: languages option cannot be used alongside other options. Omit --languages.')
            exit(1)
        else:
            print(colored('Languages currently supported: ', 'blue') + str(SUPPORTED_LANGUAGES))
            exit(0)
    else:
        if args.language:
            lang = args.language
        else:
            lang = None

        if args.repos and not args.devs:
            content_type = Constants.REPOSITORIES

        if args.devs and not args.repos:
            content_type = Constants.DEVELOPERS

        if args.repos and args.devs:
            print("ERROR: Use either repos or devs flag, not both.")
            exit(1)

        if not args.repos and (not args.devs):
            print("ERROR: Use either repos or devs flag.")
            exit(1)

        soup = get_github_soup(content_type, args.period, lang)

        main_content = soup.find("main")
        info_box = main_content.find_all("div", class_="Box")

        if len(info_box) != 1:
            print("ERROR: Could not parse.")
            exit(1)

        box_content = info_box[0]

        try:

            if content_type == Constants.REPOSITORIES:
                list_items = box_content.find_all('article', class_="Box-row")
                check_if_list_valid(list_items, content_type)

                trending = get_repositories(list_items)
                print_repositories(trending, args.format)

            if content_type == Constants.DEVELOPERS:
                list_items = box_content.find_all('article', class_="Box-row d-flex")
                check_if_list_valid(list_items, content_type)

                trending = get_developers(list_items)
                print_developers(trending, args.format)

        except Exception as e:
            print("ERROR: Could not parse elements of the GitHub page: {}".format(e))
            exit(1)
