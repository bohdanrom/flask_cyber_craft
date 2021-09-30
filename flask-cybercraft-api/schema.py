# Module for GraphQl schema and API logic

import requests

import graphene


def extract_from_ide(url: str) -> dict:
    """
    Function for receiving data GraphQL IDE(github name, repositories names from parameter <url>
    :param url String that contains url address for parsing in our case it's
    https://api.github.com/users/<GITHUB_LOGIN>
    or
    https://api.github.com/users/<GITHUB_LOGIN>/repos
    :return Dictionary with github name of account and his or her repositories names
    """
    headers = {"Authorization": "token "}
    if url.endswith("/repos"):
        github_repos = [elem.get("name") for elem in requests.get(url, headers=headers).json()]
        github_name = requests.get(url[:url.find("/repos")], headers=headers).json().get("name")
        return {
                "github_name": github_name,
                "github_repos": github_repos
                }
    elif url.endswith("/repos") is False:
        github_name = requests.get(url, headers=headers).json().get("name")
        github_repos = [elem.get("name") for elem in requests.get(url + "/repos", headers=headers).json()]
        return {
            "github_name": github_name,
            "github_repos": github_repos
        }


class GithubApi(graphene.ObjectType):
    """ This class contains attributes from Github API response """
    url = graphene.String(required=True)
    github_name = graphene.String()
    github_repos = graphene.List(of_type=graphene.String)


class Query(graphene.ObjectType):
    """ This is a class that send queries to the Github API """
    website = graphene.Field(GithubApi, url=graphene.String(), required=True)

    def resolve_website(self, info, url: str) -> GithubApi:
        """
        Method which runs extract function and receives date from request
        :param info: info for query and schema meta information and per-request context
        :param url: String which contains url address
        :return: GithubApi class object
        with data from Github API: github name and repositories names
        """
        extracted = extract_from_ide(url)
        return GithubApi(url=url,
                         github_name=extracted.get("github_name"),
                         github_repos=extracted.get("github_repos"))


schema = graphene.Schema(query=Query)
