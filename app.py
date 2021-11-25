import requests
import json
import flask
import oauth2
from flask import request,render_template,jsonify,url_for


app = flask.Flask(__name__)
app.config["DEBUG"] = True

#luser = 'mako-79'
#lrepo = 'WebBooksList-from-JSON'

luser = 'MartinHeinz'
#lrepo = 'python-project-blueprint'

# check pulls if not merged
def check_merged(pull_number,l_repo):
    lurl = "https://api.github.com/repos/{}/{}/pulls/{}/merge".format(luser,l_repo,pull_number)
    resp = requests.get(lurl)
    if resp.status_code == 404:
        return 1

# Home
@app.route('/')
def home():
    #return "<h1>TEST</h1><p>testing API</p>"
    return render_template("index.html")

### 
names = []  
@app.route('/repo_details')
def repo_details():
     url = "http://api.github.com/users/{}/repos".format(luser)
     data = {"type" : "all", "sort" : "full_name", "direction" : "desc"}
     resp = requests.get(url,data=json.dumps(data))
     if resp.status_code == 200:
        jobj = json.loads(resp.text)
        for item in jobj:
            names.append(item["name"])
        return render_template("index.html",repos=names)
     else:
        return render_template("index.html",resp="Ошибка 404")
###
@app.route('/repo_details/<repo_name>')
def get_reponame(repo_name):
    return  render_template("index.html",repo_name=repo_name)
    #return redirect(url_for('',guest = name))
###
allpulls = []        
@app.route('/list_all_pulls/<repo_name>')
def list_all_pulls(repo_name):
    url = "https://api.github.com/repos/{}/{}/pulls".format(luser,repo_name)
    data = {"state" : "all"}
    response = requests.get(url,data=json.dumps(data))
    if response.status_code == 200:
        output = json.loads(response.text)
        for i in output:
            allpulls.append(str(" id:")+str(i["id"])+str(" number:")+str(i["number"]))
        return render_template("index.html",repo_name=repo_name,items=allpulls)
    else:
        return render_template("index.html",resp="Ошибка 404")
###
not_merged = []        
@app.route('/list_not_merged/<repo_name>')
def list_not_merged(repo_name):
    url = "https://api.github.com/repos/{}/{}/pulls".format(luser,repo_name)
    data = {"state" : "all","direction" : "number"}
    response = requests.get(url,data=json.dumps(data))
    if response.status_code == 200:
        output = json.loads(response.text)
        for i in output:
            chpull_number = check_merged(i["number"],repo_name)
            if chpull_number == 1:
                not_merged.append(str(" id:")+str(i["id"])+str(" number:")+str(i["number"]))
        return render_template("index.html",repo_name=repo_name,items=not_merged)
    else:
        return render_template("index.html",resp="Ошибка 404")
###
issues = []            
@app.route('/list_issues/<repo_name>')
def list_issues(repo_name):
    url = "http://api.github.com/repos/{}/{}/issues?state=all".format(luser,repo_name)
    response = requests.get(url)
    if response.status_code == 200:
        output = json.loads(response.text)
        # выводим список
        for i in output:
            issues.append(str(" id:")+str(i["id"])+str(" number:")+str(i["number"])+str(" title:")+str(i["title"]))
            return render_template("index.html",repo_name=repo_name,items=issues)
    else:
        return render_template("index.html",resp="Ошибка 404")
###
forks = []            
@app.route('/list_forks/<repo_name>')
def list_forks():
    url = "https://api.github.com/repos/{}/{}/forks".format(luser,repo_name)
    response = requests.get(url)
    if response.status_code == 200:
        output = json.loads(response.text)
        # выводим список
        for i in output:
            forks.append(str(i["id"])+str(" name:")+str(i["name"]))
            return render_template("index.html",repo_name=repo_name,items=forks)
    else:
        return render_template("index.html",resp="Ошибка 404")


#with app.test_request_context():
    #print(url_for('home'))
    #print(url_for('repo_details'))
    #print(url_for('get_reponame'))
    #print(url_for('list_all_pulls'))
    #print(url_for('list_not_merged'))
    #print(url_for('list_issues'))

    
app.run()

