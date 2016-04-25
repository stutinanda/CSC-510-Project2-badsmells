import github3
import csv
import sys
import dateutil.parser
from datetime import datetime

repo_count = 1

def find_issues_uneven_weekly_commits(repo):

	repo = github3.repository(repo[0], repo[1])
	all_milestones = repo.milestones(state='closed', sort='due_date', direction='asc')

	for per in xrange(1,5):
		f = open('./features/repo_'+str(repo_count)+'_early_smoke_milestone_completion_trend.csv', 'wt')
		
		try:
			writer = csv.writer(f)
			writer.writerow( ('Milestone_No', 'Creation_Day', 'Due_Day', 'Closed_Day'))
			relative_date = dateutil.parser.parse('2015-12-31T00:00:01Z')
				

			for milestone in all_milestones:
				if milestone.due_on is not None:
					milestone_no = milestone.number
					creation_day = (milestone.created_at - relative_date).days
					due_day = (milestone.due_on - relative_date).days
					closed_day = (dateutil.parser.parse(milestone.closed_at) - relative_date).days
					#print closed_day
					writer.writerow( (milestone_no, creation_day, due_day, closed_day))

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
	find_issues_uneven_weekly_commits(repo)
	repo_count += 1

print 'Feature csv files saved in features directory!'
