import matplotlib.pyplot as plt
import pandas as pd

def generate_feature_graph_for_repo(repo_count):

	date_type = ['Creation_Day', 'Due_Day', 'Closed_Day']
	
	plt.rc('axes', prop_cycle=(plt.cycler('color', ['r', 'g', 'b']) + plt.cycler('linestyle', ['--', '--', '--'])))
	for i in xrange(0,3):

		data = None
		data = pd.read_csv('./features/repo_'+str(repo_count)+'_early_smoke_milestone_completion_trend.csv', sep=',', )
		data = data.sort_values('Milestone_No', ascending=True)

		max_bins = data['Milestone_No'].max()

		plt.plot(data['Milestone_No'], data[date_type[i]], label=date_type[i])
		
		plt.ylim(0,110)

	
	
	plt.ylabel('Day Since Jan 1st, 2016')
	plt.xlabel('Milestone Number')
	plt.title('Early Smoke Indicating Delay In Milestone Completion For Repo ' + str(repo_count))
	plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1, ncol=3, mode="expand", borderaxespad=0.)

	plt.savefig('./results/repo_'+str(repo_count)+'_early_smoke_milestone_completion_trend.png')
	plt.close()

for repo_count in xrange(1,4):
	generate_feature_graph_for_repo(repo_count)

print 'feature plots saved in results directory!'