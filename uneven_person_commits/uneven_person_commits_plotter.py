import matplotlib.pyplot as plt
import pandas as pd

def generate_feature_graph_for_repo(repo_count):

	data = None
	data = pd.read_csv('./features/repo_'+str(repo_count)+'_uneven_person_commits.csv', sep=',', )

	max_bins = data['Committer'].max()

	x = [0,1,2,3]
	my_xticks = data['Committer']
	plt.xticks(x, my_xticks)
	
	plt.bar(x, data['Commit_Count'])
	plt.ylabel('Commit Count')
	plt.xlabel('Person')
	plt.title('Uneven Person Commit Count for Repo ' + str(repo_count))

	plt.savefig('./results/repo_'+str(repo_count)+'_uneven_person_commits.png')
	plt.close()

for repo_count in xrange(1,4):
	generate_feature_graph_for_repo(repo_count)

print 'feature plots saved in results directory!'