# Test task(API with GraphQL) for CyberCraft

from flask import Flask, render_template, request, jsonify
from flask_graphql import GraphQLView
from schema import schema, extract


app = Flask(__name__)


@app.route('/graphql', methods=["POST", "GET"])
def graphql():
    """This function receives data from input field by AJAX and send JSON response"""
    if request.referrer is not None and request.referrer.find("/main") != 1:
        if request.method == "POST":
            if request.form.get("gitHubLogin"):
                github_login = request.form.get("gitHubLogin")
                api_response = extract(url=f"https://api.github.com/users/{github_login}")
                return jsonify(api_response)
    else:
        return GraphQLView.as_view('graphiql', schema=schema, graphiql=True)()


@app.get('/main')
def main():
    """
    This is the function for main page in this site,
    which displays info about github user: his or her github name and repositories names.
    """
    return render_template("index.html")
