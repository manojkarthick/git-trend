# -*- coding: utf-8 -*-
from termcolor import colored
from bs4 import BeautifulSoup
from collections import OrderedDict
import requests
import argparse

def cli():
    parser = argparse.ArgumentParser(description='This tool allows you to look at Github trending repositories and developers')
    parser.add_argument('--repos',action='store_true',help='to view trending repositories')
    parser.add_argument('--devs',action='store_true',help='to view trending developers' )
    parser.add_argument('--period',type=str,default='daily',help='time period of results. Opts: daily,weekly,monthly. defaults to daily.')
    parser.add_argument('--language',type=str,default=None,help='the language whose trends you want to fetch')
    parser.add_argument('--languages',action='store_true',help='print list of languages supported')
    args = parser.parse_args()

    list_languages = list()

    list_languages.append('python')
    list_languages.append('ruby')
    list_languages.append('c')
    list_languages.append('c++')
    list_languages.append('java')
    list_languages.append('javascript')
    list_languages.append('go')
    list_languages.append('rust')
    list_languages.append('lua')
    list_languages.append('haskell')

    def display_lang_list():
        print(colored('Languages currently supported: ','blue') + str(list_languages))

    url_list = [[0 for x in range(2)] for y in range(3)]

    def set_urls(lang_flag=False,language=None):
            url_list[0][0]='https://github.com/trending?since=daily'
            url_list[0][1]='https://github.com/trending/developers?since=daily'
            url_list[1][0]='https://github.com/trending?since=weekly'
            url_list[1][1]='https://github.com/trending/developers?since=weekly'
            url_list[2][0]='https://github.com/trending?since=monthly'
            url_list[2][1]='https://github.com/trending/developers?since=monthly'

            if lang_flag == True:
                for i in range(3):
                    for j in range(2):
                        url = str(url_list[i][j])
                        url = url.replace('?','/' + language + '?')
                        url_list[i][j] = url

    def get_github_soup(type,period):
            url = url_list[period-1][type-1]
            req = requests.get(url)
            page_content = req.text
            soup = BeautifulSoup(page_content, 'html.parser')
            return soup

    def get_repo_values(list_items):
            trending = OrderedDict()
            for item in list_items:
                heading = item.find("h3")
                anchor_tag = heading.find("a")
                title = anchor_tag.get('href')
                p_val = item.find("div", class_="py-1").find('p')
                extra_details = item.find("div",class_="f6 text-gray mt-2")
                programming_language_span = extra_details.find("span",class_="mr-3")
                repo_stars = extra_details.find("a",class_="muted-link tooltipped tooltipped-s mr-3").text
                if p_val != None:
                    if programming_language_span:
                        trending[title] = "{};{};{}".format(p_val.text.strip(' \t\n\r'),programming_language_span.text.strip(' \t\n\r'),repo_stars.strip(' \t\n\r'))
                    else:
                        trending[title] = "{};{}".format(p_val.text.strip(' \t\n\r'),repo_stars.strip(' \t\n\r'))
                else:
                    trending[title] = ''

            return trending

    def get_dev_values(list_items):
            trending = OrderedDict()
            for item in list_items:
                leaderboard_list_content = item.find("div",class_="leaderboard-list-content")
                anchor_tag = leaderboard_list_content.find("a")
                user_id = anchor_tag.get('href')
                username_val = leaderboard_list_content.find("span",class_="full-name")
                if username_val != None:
                    user_name = username_val.text.strip(' \t\n\r')
                user = '{} {}'.format(user_id,user_name)
                spandesc_val = item.find("span", class_="repo-snipit-description css-truncate-target")
                spanrepo_val = item.find("span", class_="repo")
                if spandesc_val != None:
                    repo_name = spanrepo_val.text.strip(' \t\n\r')
                    repo_desc = spandesc_val.text.strip(' \t\n\r')
                    trending[user] = '{};{}'.format(repo_name,repo_desc)
                else:
                    trending[user] = spanrepo_val.text.strip(' \t\n\r')
            return trending


    def scrape_data_from_page(soup):
            explore_content_div_rs = soup.find_all("div", class_="explore-content")

            if len(explore_content_div_rs) == 1:
                explore_content_div = explore_content_div_rs[0]

            list_items = explore_content_div.find_all('li')

            if type == 1:
                return get_repo_values(list_items)

            if type == 2:
                return get_dev_values(list_items)

    def print_trending(trending):
        key_color = 'green'
        desc_color = 'red'
        dev_repo_color = 'blue'
        stars_color = 'yellow'
        language_color = 'blue'
        if args.repos:
            for key,value in trending.items():
                value_items = value.split(';')
                description = value_items[0]
                if len(value_items) == 2:
                    stars = value_items[1]
                    #url_shorten.url_shortener("https://github.com"+key)
                    print("{} [★ {}]:  {}".format(colored(key,key_color),colored(stars.replace(',',''),stars_color),colored(description,desc_color)))
                else:
                    stars = value_items[2]
                    prog_language = value_items[1]
                    print("{} [{},★ {}]:  {}".format(colored(key,key_color),colored(prog_language,language_color),colored(stars.replace(',',''),stars_color),colored(description,desc_color)))

        if args.devs:
            for key,value in trending.items():
                value_items = value.split(';')
                repository_name = value_items[0]
                description = value_items[1]
                print("{}: {} - {}".format(colored(key,key_color),colored(repository_name,dev_repo_color),colored(description,desc_color)))

    if args.languages:
        if args.repos or args.devs or args.language:
            print('ERROR: languages option cannot be used alongside other options. Omit --languages.')
        else:
            display_lang_list()
        exit()
    else:
        if args.language:
            lang_flag = True
            lang = args.language
        else:
            lang_flag = False
            lang = None

        if args.repos and not args.devs:
            type = 1

        if args.devs and not args.repos:
            type = 2

        if args.repos and args.devs:
            print("ERROR: Use either repos or devs flag, not both.")
            exit()

        if args.period:
                if args.period == 'daily':
                    t_period = 1
                elif args.period == 'weekly':
                    t_period = 2
                elif args.period == 'monthly':
                    t_period = 3
                else:
                    print('Invalid period option. Exiting..')
                    exit()
        else:
            t_period = 1

        print("Fetching. Please wait....")

        set_urls(lang_flag,lang)
        soup = get_github_soup(type,t_period)
        trending = scrape_data_from_page(soup)
        print_trending(trending)