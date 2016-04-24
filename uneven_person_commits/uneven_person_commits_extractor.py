import github3
import csv
import sys
import dateutil.parser
import os

repo_count = 1

g = github3.login(os.environ['git_username'], os.environ['git_password'])

def find_issues_uneven_person_commit(repo):

	committer_map = {}
	person_map = anonymize_persons()

	repo = g.repository(repo[0], repo[1])
	all_commits = repo.commits()

	for commit in all_commits:
		committer = commit.commit.committer["name"]
		
		if committer_map.has_key(person_map[committer]):
			committer_map[person_map[committer]] += 1
		else:
			committer_map[person_map[committer]] =1

	f = open('./features/repo_'+str(repo_count)+'_uneven_person_commits.csv', 'wt')
	
	try:
		writer = csv.writer(f)
		writer.writerow( ('Committer', 'Commit_Count'))
	
		for (key, value) in committer_map.items():
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

## Anonymize names of the contributors using the person_map
## It should contain details as shown in person_map.csv
## If the user contributed using different id's give 
## same Person #{Number} to both names
def anonymize_persons():

	person_map = {}
	f = open('../person_map.csv', 'rt')
	reader = None
	try:
	    reader = csv.reader(f)

	    for row in reader:
			person_map[row[0]] = row[1]

	finally:
	    f.close()

	return person_map

repo_details = read_anonymized_repos()

for repo in repo_details:
	find_issues_uneven_person_commit(repo)
	repo_count += 1

print 'Feature csv files saved in features directory!'
