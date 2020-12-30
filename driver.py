'''
William Zhu (wzhu4@uchicago.edu)

'''

from markov import identify_speaker
import sys
import os
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt


def normal(text1, text2, unknown, k, state):
    '''
    The normal function takes in text1, text2, unknown, k, and state.
    It prints out the probability of unknown text belonging to text1 and text2,
    as well as the text that is closest to unknown.
    '''
    out = identify_speaker(text1, text2, unknown, k, state)
    out_text = f'''
    Speaker A: {out[0]}
    Speaker B: {out[1]}

    Conclusion: Speaker {out[2]} is most likely
    '''
    print(out_text)


def pmeasure(text1, text2, unknown, k, run):
    '''
    The pmeasure function takes in text1, text2, unknown, k and run.
    It creates a dataframe of run time by running identify_speaker from markov for 
    different k value and number of run trials.
    It visualizes the mean of run time for Hashtable vs runtime at different k.
    The final seaborn plot is saved as "execution_graph.png". 
    '''
    df = pd.DataFrame(columns = ['Implementation', 'K', 'Run', 'Time'])
    row = 0
    #Hashtable
    for i in range(1, k+1):
        for j in range(1, run+1):
            start = time.perf_counter()
            tup = identify_speaker(text1, text2, unknown, i, 0)
            end = time.perf_counter()
            elapsed_time = float(f'{end - start:0.4f}')
            df.loc[row] = ['Hashtable', i, j, elapsed_time]
            row += 1


    #Dictionary
    for i in range(1, k+1):
        for j in range(1, run+1):
            start = time.perf_counter()
            tup = identify_speaker(text1, text2, unknown, i, 1)
            end = time.perf_counter()
            elapsed_time = float(f'{end - start:0.4f}')
            df.loc[row] = ['dict', i, j, elapsed_time]
            row += 1
    
    print(df)
    
    #groupby and ploting the graph
    dfmean = df.groupby(['Implementation', 'K'], as_index=False).mean()
    sns.set(style="darkgrid")
    graph = sns.pointplot(x='K', y='Time', data = dfmean, linestyle='-', marker='o', hue='Implementation')
    graph.set_title('HashTable vs Python dict')
    graph.set_ylabel(f'Average Time (Runs={run})')
    graph.set_xlabel('K')
    graph.legend(loc = 'center right', title = 'Lines')
    graph.yaxis.grid(True, color = 'lightgrey')
    graph.xaxis.grid(True, color = 'lightgrey')
    plt.savefig("execution_graph.png")


def open_file(filename):
    '''
    Copied from test_markov.py. 
    The function takes in a filename, it opens and reads the file.
    '''
    contents = []
    if not os.path.isfile(filename):
        print("Bad file name:" + filename)
        sys.exit(0)
    with open(filename, "r") as file:
        contents = file.read()
    return contents



if __name__ == "__main__":
    if sys.argv[1] != 'p':
        speaker1 = open_file(sys.argv[1])
        speaker2 = open_file(sys.argv[2])
        speaker3 = open_file(sys.argv[3])
        normal(speaker1, speaker2, speaker3, int(sys.argv[4]), int(sys.argv[5]))

    else:
        speaker1 = open_file(sys.argv[2])
        speaker2 = open_file(sys.argv[3])
        speaker3 = open_file(sys.argv[4])
        pmeasure(speaker1, speaker2, speaker3, int(sys.argv[5]), int(sys.argv[6]))
