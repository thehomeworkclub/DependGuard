# app.py

from flask import Flask, render_template, send_from_directory, request

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
    # TODO: Load page w/ no info -> loading symbol 

# TODO: Create new API Routes to do the following:
# TODO: Grab Github link -> Parse through parser
# TODO: Enter github link into api -> get files -> get requirements.txt, pom.xml
# TODO: If req.txt -> parse reqs and feed into vauln test (figure out if in cache/not)
# TODO: If pom.xml -> parse reqs and feed into vauln test (figure out if in cache/not)
    return "0"

if __name__ == '__main__':
    app.run(debug=True)
