import github3
import csv
import sys
import dateutil.parser

repo_count = 1

def find_issues_exceeding_milestone_due_date(repo):

	weekly_commit_count = {}

	for i in  xrange(1,15):
		weekly_commit_count.setdefault(i,0)

	repo = github3.repository(repo[0], repo[1])
	all_commits = repo.commits()

	for commit in all_commits:
		commit_date = commit.commit.committer["date"]
		week_no = dateutil.parser.parse(commit_date).isocalendar()[1]
		#print repo.commit(commit1.sha).commit.committer["date"]
		
		if weekly_commit_count.has_key(week_no):
			weekly_commit_count[week_no] += 1
		else:
			weekly_commit_count[week_no] =1

	f = open('./features/repo_'+str(repo_count)+'_uneven_weekly_commits.csv', 'wt')
	
	try:
		writer = csv.writer(f)
		writer.writerow( ('Week_No', 'Commit_Count'))
	
		for (key, value) in weekly_commit_count.items():
			writer.writerow( (key, value))

	finally:
	    f.close()


## Function to Read the list of repos stored in repo_details.csv
## It should contain the details as shown in repo_details_sample.csv
## It should be present in the directory above the diretory of this python script
def read_anonymized_repos():
	w = 2
	h = 3
	repo_details = [[0 for x in range(w)] for y in range(h)]

	f = open('../repo_details.csv', 'rt')
	reader = None
	try:
	    reader = csv.reader(f)
	    i = 0
	    for row in reader:
			repo_details[i][0] = row[0]
			repo_details[i][1] = row[1]
			i += 1

	finally:
	    f.close()

	return repo_details

repo_details = read_anonymized_repos()

for repo in repo_details:
	find_issues_exceeding_milestone_due_date(repo)
	repo_count += 1

print 'Feature csv files saved in features directory!'
