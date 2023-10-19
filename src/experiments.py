import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# latex font
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# font sizes for full text
plt.rc('font', size=16)
plt.rc('axes', labelsize=12)# Set the axes labels font size
plt.rc('xtick', labelsize=11)
plt.rc('ytick', labelsize=11)

plt.rc('legend', fontsize=12)
# plt.rc('figure', titlesize=26)



def compare_vi(f1, f2):
    # Load the results from files using Pandas
    df1 = pd.read_csv(f1)
    df2 = pd.read_csv(f2)

    # Compare the results for the same mazes
    merged_df = pd.merge(df1, df2, on='Maze file', suffixes=('_1', '_2'))
    merged_df['Iterations_diff'] = merged_df['Iterations_1'] - merged_df['Iterations_2']
    merged_df['Reward_diff'] = merged_df['Total Reward_1'] - merged_df['Total Reward_2']
    print(merged_df)

def output_barplots(f1, f2, fname):
    df1 = pd.read_csv(f1)
    df2 = pd.read_csv(f2)

    # Compare the total rewards
    merged_df = pd.merge(df1, df2, on='Maze file', suffixes=('_1', '_2'))
    merged_df['Maze file'] = list(map(lambda x: x[:-4], merged_df['Maze file']))
    
    # Plot the bar plots
    merged_df.plot(x='Maze file', y=['Total Reward_1', 'Total Reward_2'], kind='bar')
    plt.xlabel('Maze Name')
    plt.ylabel('Average Rewards')
    plt.legend(['Value Iteration', 'FF Replan'])
    plt.grid(linestyle = '--', linewidth = 0.5)
    plt.tight_layout()
    plt.savefig(fname)
    plt.show()
    

if __name__=="__main__":
    vi1 = "logs/async_vi_0.99999_0.1.csv"
    vi2 = "logs/ffreplan.csv"

    # compare_vi(vi1, vi2)
    output_barplots(vi1, vi2, 'logs/total_rewards.pdf')
