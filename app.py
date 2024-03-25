# app.py

from flask import Flask, render_template, send_from_directory, request, jsonify
import utils.utils
from utils.vuln import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')
@app.route('/smalllogo.png')
def banner_img():
    return send_from_directory(path="banner.png", directory="templates")
@app.route("/results", methods=["POST"])
def results():
    form_dt_github = request.form.get("SubmitRepoLinkText")
    form_dt_file = request.form.get("SubmitDependencyFile")
    dt_op_git = form_dt_github.split("/")[3] + "/" + form_dt_github.split("/")[4]
    return render_template("results.html", github=form_dt_github, name=dt_op_git)

@app.route("/api/get_deps")
def rt():
    qrs = request.args.get("github")
    reqs = utils.utils.get_reqs_github(qrs)
    return {"data": reqs}
@app.route("/api/get_subdeps")
def mks():
    qrs = request.args.get("dep")
    ver = request.args.get("ver")
    reqs = utils.utils.get_dep_tree(qrs, ver)
    reqs1 = utils.utils.get_tree_rec(qrs)
    print(reqs1)
    return {"data": reqs1}
@app.route('/api/get_subdeps/tv')
def mkstv():
    qrs = request.args.get("dep")
    ver = request.args.get("ver")
    reqs = utils.utils.get_tree_rec(qrs)
    return {"data": reqs}

@app.route("/api/get_scores")
def get_scores_route():
    library = request.args.get("dep")
    version = request.args.get("ver")
    if not library or not version:
        return {"error": "Please provide both 'library' and 'version' query parameters."}, 400
    scores = utils.utils.createscore(library, version)
    return {"data": scores}


@app.route('/api/get_vuln_data')
def get_vuln_data_route():
    # Get library name, version, and package manager from query parameters
    library = request.args.get('dep')
    version = request.args.get('ver')
    pckmanager = request.args.get('pckmanager', 'pypi')  # Default to 'pypi'

    # Call the get_vuln_data function to fetch vulnerability data
    vuln_data = get_vuln_data(library, version, pckmanager)

    # Return the vulnerability data as a JSON response
    return jsonify({'data': vuln_data})


if __name__ == '__main__':
    app.run(debug=True)
