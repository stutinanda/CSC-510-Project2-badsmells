import matplotlib.pyplot as plt
import pandas as pd

def generate_feature_graph_for_repo(repo_count):

	plt.rc('axes', prop_cycle=(plt.cycler('color', ['r', 'g', 'b', 'k']) + plt.cycler('linestyle', ['--', '--', '--', '--'])))
	for per in xrange(1,5):

		data = None
		data = pd.read_csv('./features/repo_'+str(repo_count)+'_person_'+str(per)+'_uneven_person_commits.csv', sep=',', )

		max_bins = data['Week_No'].max()

		plt.plot(data['Week_No'], data['Commit_Count'], label="Person" + str(per))

	
	plt.ylabel('Commit Count Per Person')
	plt.xlabel('Week Number')
	plt.title('Early Commit Smoke Per Person for Repo ' + str(repo_count))
	plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1, ncol=4, mode="expand", borderaxespad=0.)

	plt.savefig('./results/repo_'+str(repo_count)+'_early_commit_smoke.png')
	plt.close()

for repo_count in xrange(1,4):
	generate_feature_graph_for_repo(repo_count)

print 'feature plots saved in results directory!'