import matplotlib.pyplot as plt
import pandas as pd

def generate_feature_graph_for_repo():

	data = None
	data = pd.read_csv('./features/repo_all_issue_without_milestones.csv', sep=',', )

	max_bins = data['Repo_No'].max()

	x = [0,1,2]
	my_xticks = data['Repo_No']
	plt.xticks(x, my_xticks)
	
	plt.bar(x, data['Issues_Without_Milestones'])
	plt.xlabel('Groups')
	plt.ylabel('Issues without milestone')
	plt.title('Issues without milestone for all groups')

	plt.savefig('./results/repo_all_issue_without_milestones.png')
	plt.close()

generate_feature_graph_for_repo()

print 'feature plots saved in results directory!'