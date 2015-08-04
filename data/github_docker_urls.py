import pandas
from pandas.core.series import Series
from pandas.core.frame import DataFrame

data_files_path = 'data/github'

repos_with_kw_docker_2011_to_2014_filepath = data_files_path + \
    'repos_with_docker_2011_to_2014.csv'

repos_with_kw_docker_2015_filepath = data_files_path + \
    'repos_with_docker_2015.csv'


df_github_repos_with_kw_docker_2011_to_2014 = DataFrame(pandas.read_csv(
    repos_with_kw_docker_2011_to_2014_filepath
)['repository_url'])


def apiurl_to_repourl(apiurl):
    return apiurl.replace('api.', '').replace('repos/', '')

df_repos_2015 = pandas.read_csv(repos_with_kw_docker_2015_filepath)['repo_url']
df_github_repos_with_kw_docker_2015 = DataFrame({
        'repository_url': map(apiurl_to_repourl, df_repos_2015)
    })

df_repo_urls_with_kw_docker_2011_to_2015 = \
    df_github_repos_with_kw_docker_2011_to_2014.append(
        df_github_repos_with_kw_docker_2015,
        ignore_index=True
    )
