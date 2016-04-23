import github3
import csv
import sys

repo_count = 1

def find_issues_exceeding_milestone_due_date(repo):

	issues = github3.issues_on(repo[0], repo[1], milestone='*', state='closed')
	#print issues

	f = open('./features/repo_'+str(repo_count)+'_issues_exceeding_milestone_due_date.csv', 'wt')
	try:
		writer = csv.writer(f)
		writer.writerow( ('Issue_No', 'Milestone_No'))

		for issue in issues:
			issue_no = issue.number

			if issue.milestone is not None:
				milestone_no = issue.milestone.number
				milestone_due_on = issue.milestone.due_on
				issue_closed_at = issue.closed_at
				if (issue.milestone is not None and issue.milestone.due_on is not None):
					if issue.closed_at is None or (issue.milestone.due_on < issue.closed_at):
						writer.writerow( (issue_no, milestone_no) )

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
