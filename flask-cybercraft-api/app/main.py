# Test task(API with GraphQL) for CyberCraft

from flask import Flask, render_template, request
from flask_graphql import GraphQLView
from schema import schema, extract


app = Flask(__name__)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


@app.route('/main', methods=["GET", "POST"])
def main():
    """
    This is the function for main page in this site,
    which displays info about github user: his or her github name and repositories names.
    """
    if request.method == "POST":
        github_login = request.form.get("gitHubLogin")
        if github_login:
            api_response = extract(url=f"https://api.github.com/users/{github_login}")
            return render_template("index.html",
                                   github_name=api_response.get("github_name"),
                                   github_repos=api_response.get("github_repos"))
        return render_template("index.html")
    return render_template("index.html")
