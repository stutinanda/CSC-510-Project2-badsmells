from __future__ import print_function
import urllib2
import json
import re
import pandas as pd
from pylab import *

row_list = []

class L():
    "Anonymous container"
    def __init__(i, **fields):
        i.override(fields)

    def override(i, d): i.__dict__.update(d); return i

    def __repr__(i):
        d = i.__dict__
        name = i.__class__.__name__
        return name + '{' + ' '.join([':%s %s' % (k, pretty(d[k]))
                                      for k in i.show()]) + '}'

    def show(i):
        lst = [str(k) + " : " + str(v) for k, v in i.__dict__.iteritems() if v != None]
        return ',\t'.join(map(str, lst))


def secs(d0):
    d = datetime.datetime(*map(int, re.split('[^\d]', d0)[:-1]))
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = d - epoch
    return delta.total_seconds()


def dump1(u, issues):
    global row_list
    token = "b7814cf93fbc3f0fb2d370b1325f59a02e91b0d5"  # <===
    request = urllib2.Request(u, headers={"Authorization": "token " + token})
    v = urllib2.urlopen(request).read()
    w = json.loads(v)
    if not w: return False
    for event in w:
        group_id = event['issue']["repository_url"]
        issue_id = event['issue']['number']
        if not event.get('label'): continue
        title = event['issue']["title"]
        state = event['issue']["state"]
        created_at = secs(event['created_at'])
        if event['issue']['closed_at'] != None:
            closed_at = secs(event['issue']['closed_at'])
        else:
            closed_at = -1
        action = event['event']
        label_name = event['label']['name']
        user = event['actor']['login']

        milestone = event['issue']['milestone']
        if milestone != None:
            milestone_id = milestone['number']
            milestone_title = milestone['title']
            milestone_creator = milestone['creator']['login']
            milestone_open_issues = milestone['open_issues']
            milestone_closed_issues = milestone['closed_issues']
            if milestone['closed_at'] != None:
                milestone_created_at = secs(milestone['created_at'])
            else:
                milestone_created_at = -1
            if milestone['closed_at'] != None:
                milestone_closed_at = secs(milestone['closed_at'])
            else:
                milestone_closed_at = -1
            if milestone['due_on'] != None:
                milestone_due_on = secs(milestone['due_on'])
            else:
                milestone_due_on = -1
            milestone_state = milestone['state']
        else:
            milestone_id = "None"
            milestone_title = "None"
            milestone_creator = "None"
            milestone_open_issues = "None"
            milestone_closed_issues = "None"
            milestone_created_at = "None"
            milestone_closed_at = "None"
            milestone_due_on = "None"
            milestone_state = "None"
        eventObj = L(group_id=group_id, issue_id=issue_id, title=title, state=state,
                     created_at=created_at, closed_at=closed_at, action=action,
                     label_name=label_name, user=user, milestone_id=milestone_id,
                     milestone_title=milestone_title, milestone_creator=milestone_creator,
                     milestone_open_issues=milestone_open_issues, milestone_closed_issues=milestone_closed_issues,
                     milestone_created_at=milestone_created_at, milestone_closed_at=milestone_closed_at,
                     milestone_due_on=milestone_due_on, milestone_state=milestone_state)
        dict = {'group_id':group_id, 'issue_id':issue_id, 'title':title, 'state':state,
                     'created_at':created_at, 'closed_at':closed_at, 'action':action,
                     'label_name':label_name, 'user':user, 'milestone_id':milestone_id,
                     'milestone_title':milestone_title, 'milestone_creator':milestone_creator,
                     'milestone_open_issues':milestone_open_issues, 'milestone_closed_issues':milestone_closed_issues,
                     'milestone_created_at':milestone_created_at, 'milestone_closed_at':milestone_closed_at,
                     'milestone_due_on':milestone_due_on, 'milestone_state':milestone_state}
        row_list.append(dict)
        all_events = issues.get(issue_id)
        if not all_events: all_events = []
        all_events.append(eventObj)
        issues[issue_id] = all_events
    return True


def dump(u, issues):
    try:
        return dump1(u, issues)
    except Exception as e:
        print(e)
        print("Contact TA")
        return False


def launchDumpAndAnonimize():
    global row_list
    # Give urls of the repos you want to pull data from
    urls = []
    for url in urls:
        page = 1
        issues = dict()
        while (True):
            doNext = dump(url + str(page), issues)
            page += 1
            if not doNext: break
    df = pd.DataFrame(row_list)
    value_dict = dict( l.rstrip().split('=') for l in open("data/anonimize.txt"))
    df['group_id'] = df['group_id'].replace(value_dict)
    df['milestone_creator'] = df['milestone_creator'].replace(value_dict)
    df['user'] = df['user'].replace(value_dict)
    total_issue, long_lived_issue, short_lived_issue, issue_person, issue_milestone = extract_features(df)

    for key in issue_person.keys():
        plot_issue_per_person(issue_person[key], key)

    for key in total_issue.keys():
        plot_lifetime_charts(total_issue[key], short_lived_issue[key], long_lived_issue[key], key)

    for key in issue_milestone.keys():
        plot_milestone_issues_bar_chart(issue_milestone[key], key)

    df.to_csv("data/issues.csv")
    print('Finish')

def extract_features(df):
    grouped = df.groupby('group_id')
    issue_person = {}
    issue_milestone = {}
    long_lived_issue = {}
    short_lived_issue = {}
    total_issue = {}

    for name, group in grouped:
        grouped_by_person = group.groupby("user")
        d = {}
        for n, g in grouped_by_person:
            if n != 'Person 0':
                d[n] = len(g)
        issue_person[name] = d

        grouped_by_milestone = group.groupby("milestone_id")
        md = {}
        for n, g in grouped_by_milestone:
            md[n] = len(g)
        issue_milestone[name] = md

        group_lifetime = group[group.closed_at != -1]
        group_lifetime_len = len(group_lifetime)
        avg_lifetime = (group_lifetime['closed_at'].sum() - group_lifetime['created_at'].sum())/group_lifetime_len
        group_lifetime['lifetime'] = group_lifetime['closed_at'] - group_lifetime['created_at']

        count_shortlived = 0
        count_longlived = 0
        for lt in group_lifetime['lifetime']:
            if lt < (avg_lifetime * 0.50):
                count_shortlived = count_shortlived + 1
            elif lt > (avg_lifetime * 1.50):
                count_longlived = count_longlived + 1

        group_not_closed = len(group[group.closed_at == -1])
        count_longlived = count_longlived + group_not_closed
        long_lived_issue[name] = count_longlived
        short_lived_issue[name] = count_shortlived
        total_issue[name] = len(group)

    return total_issue, long_lived_issue, short_lived_issue, issue_person, issue_milestone

def plot_issue_per_person(repo_issue_dict, repo):
    labels = repo_issue_dict.keys()
    fracs = repo_issue_dict.values()
    plt.pie(fracs, labels=labels, autopct='%.0f%%', shadow=False, radius=0.5)
    plt.savefig('data/issue_per_person_' + repo + '.png')
    plt.close()

def plot_lifetime_charts(total, short, long, repo):
    labels = ['Short-Lived Issues', 'Long-Lived Issues', 'Issues with Average Lifetime' ]
    fracs = [short, long, (total - (short + long))]
    plt.pie(fracs, labels=labels, autopct='%.0f%%', shadow=False, radius=0.5)
    plt.savefig('data/issues_lifetime_plot_' + repo + '.png')
    plt.close()

def plot_milestone_issues_bar_chart(repo_issue_milestone_dict, repo):
    x = repo_issue_milestone_dict.keys()
    y_pos = np.arange(len(x))
    y = repo_issue_milestone_dict.values()
    plt.bar(y_pos, y, align='center', alpha=0.5)
    plt.xticks(y_pos, x)
    plt.ylabel('Number of Issues')
    plt.title('Milestone ID')
    plt.savefig('data/milestone_issues_bar_chart_' + repo + '.png')
    plt.close()

launchDumpAndAnonimize()
