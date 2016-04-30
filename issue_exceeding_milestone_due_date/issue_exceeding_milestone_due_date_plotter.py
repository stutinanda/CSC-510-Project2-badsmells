import matplotlib.pyplot as plt
import pandas as pd

def generate_feature_graph_for_repo(repo_count):

	data = None
	data = pd.read_csv('./features/repo_'+str(repo_count)+'_issues_exceeding_milestone_due_date.csv', sep=',', )

	max_bins = data['Milestone_No'].max()

	data['Milestone_No'].hist(bins=max_bins)
	plt.xticks(data['Milestone_No'])
	plt.ylabel('Frequency')
	plt.xlabel('Milestone')
	plt.title('Issues exceeding Milestone due date for Repo ' + str(repo_count))

	plt.savefig('./results/repo_'+str(repo_count)+'_issues_exceeding_milestone_due_date_graph.png')
	plt.close()

for repo_count in xrange(1,4):
	generate_feature_graph_for_repo(repo_count)

print 'feature plots saved in results directory!'