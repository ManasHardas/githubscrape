# -*- coding: utf-8 -*-
import scrapy
import requests
import unicodedata
from bs4 import BeautifulSoup
from ..data.github.docker.urls import df_repo_urls_with_kw_docker_2011_to_2015


class DockerfileSpider(scrapy.Spider):
    name = "dockerfilespider"
    allowed_domains = ["github.com"]
    # start_urls = df_repo_urls_with_kw_docker_2011_to_2015
    start_urls = 'https://github.com/grokkerlab/celery27'

    def parse(self, response):
                # only parse dockerfile pages; rest ignore
        soup = BeautifulSoup(response.body, 'html.parser')

        title_uni = soup.title.get_text()
        title_str = uni_to_str(title_uni)

        if 'Dockerfile' not in title_str:
            pass
        else:
            filename = make_dockerfile_name_from_pagetitle(title_str)
            # print filename

            _filepath = r'../scraped_dockerfiles/' + filename
            f = open(_filepath, 'w')
            f.write('NAME ' + filename + '\n')

            for line in soup.find_all('td'):
                stripped_line = uni_to_str(line.get_text()).strip()
                # print stripped_line
                if stripped_line:
                    f.write(stripped_line + '\n')


def make_dockerfile_name_from_pagetitle(title_str):
    return title_str.split()[3].replace('/', '-')


def uni_to_str(uni):
    return unicodedata.normalize('NFKD', uni).encode('ascii', 'ignore')
