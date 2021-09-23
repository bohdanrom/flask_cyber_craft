# Test task(API with GraphQL) for CyberCraft

from flask import Flask, render_template, request, jsonify
from flask_graphql import GraphQLView
from schema import schema, extract


app = Flask(__name__)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


@app.post('/receive_json')
def receive_json():
    """This function receives data from input field by AJAX and send JSON response"""
    github_login = request.form.get("gitHubLogin")
    api_response = extract(url=f"https://api.github.com/users/{github_login}")
    return jsonify(api_response)


@app.get('/main')
def main():
    """
    This is the function for main page in this site,
    which displays info about github user: his or her github name and repositories names.
    """
    return render_template("index.html")
