from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import requests
import unicodedata
from bs4 import BeautifulSoup
from data.github_docker_urls import make_test_dataset
# from data.github_docker_urls import df_repo_urls_with_kw_docker_2011_to_2015


class DockerfileSpider(CrawlSpider):
    name = "dockerfilespider"
    allowed_domains = ["github.com"]
    # start_urls = df_repo_urls_with_kw_docker_2011_to_2015
    start_urls = ['https://github.com/grokkerlab/celery27']

    rules = (Rule(
        LinkExtractor(
            allow=('(.*?)Dockerfile(.*?)$', ),
        ),
        callback='parse_dockerfile',
        follow=True
    ),
    )

    def parse_dockerfile(self, response):
                # only parse dockerfile pages; rest ignore
        soup = BeautifulSoup(response.body, 'html.parser')
        title_uni = soup.title.get_text()
        title_str = uni_to_str(title_uni)
        print 'PAGE TITLE: ', title_str

        if 'Dockerfile' in title_str:
            filename = make_dockerfile_name_from_pagetitle(title_str)
            print 'DOCKERFILE NAME: ', filename

            _filepath = r'scraped/dockerfiles/' + filename
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
