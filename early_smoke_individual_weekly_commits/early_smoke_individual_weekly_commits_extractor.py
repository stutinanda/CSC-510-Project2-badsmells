import github3
import csv
import sys
import dateutil.parser

repo_count = 1

def find_issues_uneven_weekly_commits(repo):

	person_map = anonymize_persons()

	weekly_commit_count_per_person=[]

	for p in xrange(0,4):
		weekly_commit_count = {} 
		for i in  xrange(1,16):
			weekly_commit_count.setdefault(i,0)
		weekly_commit_count_per_person.append(weekly_commit_count)
	
	print weekly_commit_count_per_person

	repo = github3.repository(repo[0], repo[1])
	all_commits = repo.commits()

	for commit in all_commits:
		commit_date = commit.commit.committer["date"]
		committer = commit.commit.committer["name"]
		week_no = dateutil.parser.parse(commit_date).isocalendar()[1]
		#print repo.commit(commit1.sha).commit.committer["date"]

		if weekly_commit_count_per_person[person_map[committer]-1].has_key(week_no):
			weekly_commit_count_per_person[person_map[committer]-1][week_no] += 1
		else:
			weekly_commit_count_per_person[person_map[committer]-1][week_no] = 1

	print (weekly_commit_count_per_person)

	for per in xrange(1,5):
		f = open('./features/repo_'+str(repo_count)+'_person_'+str(per)+'_uneven_person_commits.csv', 'wt')
		
		try:
			writer = csv.writer(f)
			writer.writerow( ('Week_No', 'Commit_Count'))
	
			for (key, value) in weekly_commit_count_per_person[per-1].items():
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
	    	value = str(row[1])
	    	person_map[row[0]] = int(value[-1:])

	finally:
	    f.close()

	return person_map

repo_details = read_anonymized_repos()

for repo in repo_details:
	find_issues_uneven_weekly_commits(repo)
	repo_count += 1

print 'Feature csv files saved in features directory!'
