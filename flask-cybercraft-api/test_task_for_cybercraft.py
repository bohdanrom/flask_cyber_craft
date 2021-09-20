# This is a module with testing our API using Pytest

import pytest

from schema import extract
from flask import current_app

from app.main import app


@pytest.mark.parametrize(
    "github_login_for_test, expected_result",
    [
        ("roykoand", {"github_name": "Andrii Roiko", "github_repos": []}),
        ("bohdanrom", {"github_name": None,
                       "github_repos": ["Bash", "flask_cyber_craft", "Game-Store",
                                        "project"]}),
        ("vitaliy026-00", {"github_name": "Vitalii",
                           "github_repos": ["Devops-SummerSchool", "gogs",
                                            "test_task_yalantis", "vitaliy026-00"]}),
        ("MixaKonan", {"github_name": "Mykhailo Konontsev",
                       "github_repos": ["Litter-WebApplication-UrlShortener",
                                        "Menhera", "Menherachan", "menherachan-frontend",
                                        "RivneDating-TeleBot", "ToM-ProxyApi",
                                        "ToM-TelegramBot", "Twitch-o-matic"]})
    ]
)
def test_extract_functions(github_login_for_test, expected_result):
    """ This is parametrize test-function for schema.extract function"""
    with app.app_context():
        with current_app.test_request_context():
            url = "https://api.github.com/users/"
            assert extract(url+github_login_for_test) == expected_result
