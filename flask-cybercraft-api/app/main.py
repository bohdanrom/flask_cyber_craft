# Test task(API with GraphQL) for CyberCraft
import requests

from flask import Flask, render_template, request, jsonify
from flask_graphql import GraphQLView
from schema import schema


app = Flask(__name__)


@app.route('/graphql', methods=["POST", "GET"])
def graphql():
    """This function receives data from input field by AJAX and send JSON response"""
    if request.referrer is not None and request.referrer.find("/main") != 1:
        if request.method == "POST":
            url = "https://api.github.com/graphql"
            query = request.get_data().decode('utf-8')
            headers = {"Authorization": "token ",
                       "Content-Type": "application/json"}
            response = requests.post(url=url, json={"query": query}, headers=headers)
            response_json = response.json().get("data").get("user")
            return jsonify({
                "github_name": response_json.get("name"),
                "github_repos": [repo.get("name") for repo in response_json.get("repositories").get("nodes")]
            })
    else:
        return GraphQLView.as_view('graphiql', schema=schema, graphiql=True)()


@app.get('/main')
def main():
    """
    This is the function for main page in this site,
    which displays info about github user: his or her github name and repositories names.
    """
    return render_template("index.html")
