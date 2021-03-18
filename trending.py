import json
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from collections import OrderedDict
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from pkg_resources import require
from prettytable import PrettyTable
from termcolor import colored

import utils
from enums import Colors, ContentTypes


class Trends(ABC):
    @abstractmethod
    def __init__(self, content_type, period, language=None, spoken_language=None):
        """
        Initialize the trends base class that contains information common to repos and developers
        :param content_type: Type of content to parse
        :param period: Time period to use for extracting statistics
        :param language: Filter data on a particular programming language
        """

        self.content_type = content_type
        self.period = period
        self.language = language
        self.spoken_language = spoken_language
        self.content = None

    def get_url(self):
        """
        Get URLs for repository/developer information with optional time period
        :return: URL for processing
        """
        base_url = "https://github.com/trending{t}{l}".format(
            t="" if self.content_type == ContentTypes.REPOSITORIES else "/{}".format(ContentTypes.DEVELOPERS),
            l="" if not self.language else "/{}".format(self.language)
        )

        params = {}

        if self.period:
            params["since"] = self.period
        if self.spoken_language:
            params["spoken_language_code"] = self.spoken_language

        if params:
            return "{u}?{q}".format(
                u=base_url,
                q=urlencode(params)
            )
        else:
            return base_url

    def get_github_soup(self):
        """
        Parse web page using BeautifulSoup's HTML parser
        :return:
        """
        url = self.get_url()
        try:
            req = requests.get(url)
            page_content = req.text
            return BeautifulSoup(page_content, 'html.parser')
        except requests.exceptions.Timeout:
            print("ERROR: Request timed out while querying the URL: {}".format(url))
            print("Please check if the URL is valid.")
            exit(1)
        except requests.exceptions.TooManyRedirects:
            print("ERROR: Too many redirects when querying the URL: {}".format(url))
            print("Please check if the URL is valid.")
            exit(1)
        except requests.exceptions.RequestException as e:
            print("ERROR: Could not get the requested page: {}".format(url))
            print(utils.get_traceback_string(e))
            raise SystemExit(e)
        except ImportError:
            print("ERROR: No HTML parser found. Please check your install of BeautifulSoup")
            exit(1)
        except Exception as e:
            print(utils.get_traceback_string(e))
            raise SystemExit(e)

    def parse_content(self):
        """
        Parse web page's content and extract the enclosing div Box containing the trending content
        :return:
        """
        soup = self.get_github_soup()

        main_content = soup.find("main")
        info_box = main_content.find_all("div", class_="Box")

        if len(info_box) != 1:
            print("ERROR: Could not parse.")
            exit(1)

        self.content = info_box[0]

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def print(self, format_):
        pass


class Repositories(Trends):
    def __init__(self, period, language=None, spoken_language=None):
        """
        Get Trending repositories data
        :param period: Time period to use for extracting statistics
        :param language: Filter data on a particular programming language
        """
        super().__init__(
            content_type=ContentTypes.REPOSITORIES,
            period=period,
            language=language,
            spoken_language=spoken_language
        )
        super().parse_content()

        items = self.content.find_all('article', class_="Box-row")
        status = utils.check_if_list_valid(items, self.content_type)

        if not status:
            try:
                blankslate = self.content.find_all('div', class_="blankslate")
                if len(blankslate) == 1:
                    print("There were no trending repositories for your selection.")
                    exit(1)
            except Exception as e:
                print("Could not get trending {} from the page.".format(self.content_type))
                print("Encountered Error: {}".format(utils.get_traceback_string()))
                print("ERROR: Raise an issue on https://github.com/manojkarthick/git-trend/issues")
                sys.exit(1)

        self.items = items
        self.trending = OrderedDict()

    def parse(self):
        """
        Get repository information such as name, description, language and stars
        :return:
        """
        for index, item in enumerate(self.items):
            repo_organization, repo_name = item.find("h1", class_="h3 lh-condensed").text.strip(' \t\n\r').split("/")
            repository = "{}/{}".format(repo_organization.strip(), repo_name.strip())

            repo_desc_info = item.find("p", class_="col-9 color-text-secondary my-1 pr-4")
            language_info = item.find("span", itemprop="programmingLanguage")
            stars_info = item.find("a", class_="Link--muted d-inline-block mr-3")

            repo_desc = utils.strip_and_get(repo_desc_info)
            repo_language = utils.strip_and_get(language_info)
            repo_stars = utils.strip_and_get(stars_info)

            self.trending[repository] = {
                "rank": index + 1,
                "description": repo_desc,
                "language": repo_language,
                "stars": repo_stars,
                "url": "https://github.com/{}".format(repository.strip())
            }

    def print(self, format_="default"):
        """
        Print trending repositories in the requested output format
        :param format_: output format to use
        :return:
        """
        if format_ == "default":
            for key, value in self.trending.items():
                repo_name = key
                description = value["description"] if value["description"] != "" else "<Unknown Description>"
                language = value["language"] if value["language"] != "" else "<Unknown Language>"
                stars = value["stars"]
                print("➜ {} [{}, ★ {}]:  {}".format(colored(repo_name, Colors.GREEN),
                                                    colored(language, Colors.BLUE),
                                                    colored(stars, Colors.YELLOW),
                                                    colored(description, Colors.RED)))
        elif format_ == "json":
            print(json.dumps(self.trending, indent=4))
        elif format_ == "table":
            tbl = PrettyTable()
            tbl.field_names = ["Rank", "Repository", "URL", "Language", "Stars"]
            for key, value in self.trending.items():
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


class Developers(Trends):
    def __init__(self, period, language=None):
        """
        Get Trending developers data
        :param period: Time period to use for extracting statistics
        :param language: Filter data on a particular programming language
        """
        super().__init__(
            content_type=ContentTypes.DEVELOPERS,
            period=period,
            language=language
        )
        super().parse_content()

        items = self.content.find_all('article', class_="Box-row d-flex")
        utils.check_if_list_valid(items, self.content_type)

        self.items = items
        self.trending = OrderedDict()

    def parse(self):
        """
        Get developer information such as name, id, repo name and description
        :return:
        """

        for index, item in enumerate(self.items):
            container = item.find("div", class_="col-sm-8 d-md-flex")

            user_name = container.find("h1", class_="h3 lh-condensed").text.strip(' \t\n\r')
            user_id_info = container.find("p", class_="f4 text-normal mb-1")
            repo_desc_info = item.find("div", class_="f6 color-text-secondary mt-1")
            repo_name_info = item.find("h1", class_="h4 lh-condensed")

            user_id = utils.strip_and_get(user_id_info, user_name)
            repo_name = utils.strip_and_get(repo_name_info)
            repo_desc = utils.strip_and_get(repo_desc_info)

            self.trending[user_name] = {
                "rank": index + 1,
                "user_id": user_id,
                "repository": repo_name,
                "description": repo_desc,
                "url": "https://github.com/{}".format(user_id)
            }

    def print(self, format_="default"):
        """
        Print trending developers in the requested output format
        :param format_: output format to use
        :return:
        """
        if format_ == "default":
            for key, value in self.trending.items():
                user_name = key
                user_id = value["user_id"] if value["user_id"] != "" else "<Unknown>"
                repository = value["repository"] if value["repository"] != "" else "<Unknown Repository>"
                description = value["description"] if value["description"] != "" else "<Unknown Description>"
                print("➜ {} ({})\n  {}: {}".format(colored(user_name, Colors.GREEN),
                                                   colored(user_id, Colors.GREEN),
                                                   colored(repository, Colors.BLUE),
                                                   colored(description, Colors.RED)))
        elif format_ == "json":
            print(json.dumps(self.trending, indent=4))
        elif format_ == "table":
            tbl = PrettyTable()
            tbl.field_names = ["Rank", "User", "User ID", "URL", "Repository"]
            for key, value in self.trending.items():
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


def cli():
    parser = ArgumentParser(
        description='This tool allows you to look at Github trending repositories and developers')
    parser.add_argument('--repos', action='store_true', help='to view trending repositories')
    parser.add_argument('--devs', action='store_true', help='to view trending developers')
    parser.add_argument('--period', type=str, choices=utils.get_supported_periods(), default='daily',
                        help='time period of results')
    parser.add_argument('--language', type=str, default=None,
                        help='the language whose trends you want to fetch. Use --languages flag to see supported languages.',
                        choices=utils.get_supported_languages(), metavar='<language_code>')
    parser.add_argument('--spoken-language', type=str, default=None,
                        help='spoken language you want to filter results on. Use --spoken-languages flag to see supported spoken languages.',
                        choices=utils.get_supported_spoken_languages(), metavar='<spoken_language_code>')
    parser.add_argument("--format", type=str, choices=utils.get_supported_formats(), default="default",
                        help="Output format")
    parser.add_argument('--languages', action='store_true', help='print list of languages supported')
    parser.add_argument('--spoken-languages', action='store_true', help='print list of spoken languages supported')
    parser.add_argument('--version', action='store_true', help="Package version")
    args = parser.parse_args()

    if args.version:
        print("git-trend v{}".format(require("git-trend")[0].version))
        exit(0)

    if args.languages:
        if args.repos or args.devs or args.language:
            print('ERROR: languages option cannot be used alongside other options. Omit --languages.')
            exit(1)
        else:
            print("Languages currently supported: {}")
            utils.print_supported_languages("programming")
            exit(0)

    if args.spoken_languages:
        if args.repos or args.devs or args.language or args.spoken_language:
            print('ERROR: spoken-languages option cannot be used alongside other options. Omit --spoken-languages.')
            exit(1)
        else:
            print("Languages currently supported: ")
            utils.print_supported_languages("spoken")
            exit(0)

    else:
        if args.repos and not args.devs:
            content_type = ContentTypes.REPOSITORIES
        elif args.devs and not args.repos:
            content_type = ContentTypes.DEVELOPERS
        elif args.repos and args.devs:
            print("ERROR: Use either repos or devs flag, not both.")
            exit(1)
        elif not args.repos and (not args.devs):
            print("ERROR: Use either repos or devs flag.")
            exit(1)
        else:
            print("ERROR: Ambiguous input, please select either repos or devs")
            exit(1)

        if content_type == ContentTypes.DEVELOPERS and args.spoken_language:
            print("ERROR: --spoken-language option is only supported for repos")
            exit(1)

        try:
            if content_type == ContentTypes.REPOSITORIES:
                repositories = Repositories(
                    period=args.period,
                    language=args.language,
                    spoken_language=args.spoken_language
                )

                repositories.parse()
                repositories.print(format_=args.format)

            if content_type == ContentTypes.DEVELOPERS:
                developers = Developers(
                    period=args.period,
                    language=args.language
                )

                developers.parse()
                developers.print(format_=args.format)

        except Exception as e:
            print("ERROR: Could not parse elements of the GitHub page")
            print(utils.get_traceback_string(e))
            exit(1)
