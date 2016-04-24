import github3
import csv
import sys

repo_count = 1
per_repo_unassigned_issues = {}

for i in xrange(1,4):
	per_repo_unassigned_issues.setdefault(i,0)

def find_issue_without_milestones(repo):

	issues = github3.issues_on(repo[0], repo[1], state='all')
	
	## Since pull requests are also captured as issues creating 
	## the list the list pull requests for comparison with issues
	repo = github3.repository(repo[0], repo[1])
	pull_requests = repo.pull_requests(state='all')

	pull_request_map = {}
	for pull_request in pull_requests:
		pull_request_map[pull_request.number] = pull_request.title

	for issue in issues:
		if issue.milestone is None:
			if not pull_request_map.has_key(issue.number):
				per_repo_unassigned_issues[repo_count] += 1
			#print '=========================================================='




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


def write_combined_csv():
	
	f = open('./features/repo_all_issue_without_milestones.csv', 'wt')
	try:
		writer = csv.writer(f)
		writer.writerow( ('Repo_No', 'Issues_Without_Milestones'))

		for (key, value) in per_repo_unassigned_issues.items():
			writer.writerow( ('Repo ' + str(key), value))
	finally:
	    f.close()


repo_details = read_anonymized_repos()

for repo in repo_details:
	find_issue_without_milestones(repo)
	repo_count += 1

write_combined_csv()

print 'Feature csv files saved in features directory!'
