#  gitabel
#  the world's smallest project management tool
#  reports relabelling times in github (time in seconds since epoch)
#  thanks to dr parnin
#  todo:
#    - ensure events sorted by time
#    - add issue id
#    - add person handle

"""
You will need to add your authorization token in the code.
Here is how you do it.

1) In terminal run the following command

curl -i -u <your_username> -d '{"scopes": ["repo", "user"], "note": "OpenSciences"}' https://api.github.com/authorizations

2) Enter ur password on prompt. You will get a JSON response. 
In that response there will be a key called "token" . 
Copy the value for that key and paste it on line marked "token" in the attached source code. 

3) Run the python file. 

     python gitable.py

"""
 
from __future__ import print_function
import urllib2
import json
import re,datetime
import sys
import pandas as pd
 
class L():
  "Anonymous container"
  def __init__(i,**fields) : 
    i.override(fields)
  def override(i,d): i.__dict__.update(d); return i
  def __repr__(i):
    d = i.__dict__
    name = i.__class__.__name__
    return name+'{'+' '.join([':%s %s' % (k,pretty(d[k])) 
                     for k in i.show()])+ '}'
  def show(i):
    lst = [str(k)+" : "+str(v) for k,v in i.__dict__.iteritems() if v != None]
    return ',\t'.join(map(str,lst))

  
def secs(d0):
  d     = datetime.datetime(*map(int, re.split('[^\d]', d0)[:-1]))
  epoch = datetime.datetime.utcfromtimestamp(0)
  delta = d - epoch
  return delta.total_seconds()
  
def dumpCommits(u, commits, token):
  request = urllib2.Request(u, headers={"Authorization" : "token "+token})
  v = urllib2.urlopen(request).read()
  w = json.loads(v)
  if not w: return False
  for commit in w:
    sha = commit['sha']
    if None == commit['author']:
      user = anonymous[commit['commit']['author']['name']]
    else:
      user = anonymous[commit['author']['login']]
    time = secs(commit['commit']['author']['date'])
    message = commit['commit']['message']
    commitObj = L(sha = sha,
                user = user,
                time = time,
               message = message)
    commits.append(commitObj)
  return True
  
def dumpComments(u, comments, token):
  request = urllib2.Request(u, headers={"Authorization" : "token "+token})
  v = urllib2.urlopen(request).read()
  w = json.loads(v)
  if not w: return False
  for comment in w:
    user = anonymous[comment['user']['login']]
    identifier = comment['id']
    issueid = int((comment['issue_url'].split('/'))[-1])
    comment_text = comment['body']
    created_at = secs(comment['created_at'])
    updated_at = secs(comment['updated_at'])
    commentObj = L(ident = identifier,
                issue = issueid, 
                user = user,
                text = comment_text,
                created_at = created_at,
                updated_at = updated_at)
    comments.append(commentObj)
  return True
 
def dump(u, data, dumpwhat):
  try:
    if dumpwhat is 'comments':
        return dumpComments(u, data, "503acda4198160f49d849be9a555ea439f47b08f")
    else:
        return dumpCommits(u, data, "503acda4198160f49d849be9a555ea439f47b08f")
  except Exception as e: 
    print(e)
    print("Contact TA")
    return False

def extractComments(repo):
  page = 1
  comments = []
  commentTuples = []
  while(True):
    doNext = dump(repo + '/issues/comments?page=' + str(page), comments, 'comments')
    page += 1
    if not doNext : break
  for comment in comments:
    commentTuples.append([comment.issue, comment.user, comment.created_at, comment.updated_at, comment.text, comment.ident])

  columns = ['Issue', 'User', 'Created at', 'Updated at', 'Text', 'Identifier']
  df = pd.DataFrame(data = commentTuples, columns = columns)
  df.to_csv('data/' + anonymous[repo] + '_comments.csv')
  
def extractCommits(repo):
  page = 1
  commits = []
  commitTuples = []
  while(True):
    doNext = dump(repo + '/commits?page=' + str(page), commits, 'commits')
    page += 1
    if not doNext : break
  for commit in commits:
    commitTuples.append([commit.time, commit.sha, commit.user, commit.message])

  columns = ['Time', 'Sha', 'User', 'Message']
  df = pd.DataFrame(data = commitTuples, columns = columns)
  df.to_csv('data/' + anonymous[repo] + '_commits.csv', encoding='utf-8')

def launchExtractor():
  global anonymous
  for line in open("data/anonimize.txt"):
    anonymous[line.split('=')[0]] = line.split('=')[1].rstrip('\n')

  repos = ['https://api.github.com/repos/jordy-jose/CSC_510_group_d', 'https://api.github.com/repos/ankitkumar93/csc510-se-project', 
  'https://api.github.com/repos/nikraina/CSC510-Group-M']
  for repo in repos:
      extractComments(repo)
      extractCommits(repo)

anonymous = {}
launchExtractor()

