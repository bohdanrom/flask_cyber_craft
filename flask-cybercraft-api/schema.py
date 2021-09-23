# Module for GraphQl schema and API logic

import requests

import graphene
from flask import request


def extract(url: str) -> dict:
    """
    Function for receiving data(github name, repositories names from parameter <url>
    :param url String that contains url address for parsing in our case it's
    https://api.github.com/users/<GITHUB_LOGIN>
    or
    https://api.github.com/users/<GITHUB_LOGIN>/repos
    :return Dictionary with github name of account and his or her repositories names
    """
    headers = {"Authorization": "token"}
    if request.url.find("/receive_json") != -1:
        _url = "https://api.github.com/graphql"
        query = """
        query{
            user(login: "%s") {
                name
                repositories(first: 100) {
                    nodes {
                        name
                    }
                }
            }
        }
        """ % url[len("https://api.github.com/users/"):]
        headers["Content-Type"] = "application/json"
        response = requests.post(url=_url, json={"query": query}, headers=headers)
        response_json = response.json().get("data").get("user")
        return {
                    "github_name": response_json.get("name"),
                    "github_repos": [repo.get("name") for repo in response_json.get("repositories").get("nodes")]
        }
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
        extracted = extract(url)
        return GithubApi(url=url,
                         github_name=extracted.get("github_name"),
                         github_repos=extracted.get("github_repos"))


schema = graphene.Schema(query=Query)
