import pandas as pd
import time
import matplotlib.pyplot as plt


# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/30740258
# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    # if iteration == total:
    #    print()


def print_count_of_values_relation(df: pd.DataFrame, progressBar: bool, plot: bool):
    """
    Print how many values could be found in each row.
    :param progressBar:     - Required  :  progressbar printout (bool)
    :param df:              - Optional  :  dataFrame (pandas.DataFrame)
    :param plot:            - Optional  :  plot as linechart (bool)
    """

    index = df.index
    number_of_rows = len(index)

    headers = list(df)

    for x in list(df):
        column = (headers.pop(0))
        print(column)
        # display(Markdown("# " + column_object))
        print(
            str(df[column].count()) + "/" + str(number_of_rows) + " " + str(
                "{:.0%}".format(df[column].count() / number_of_rows)))

        if progressBar == True:
            # Progress Bar
            l = len(list(range(0, number_of_rows)))
            printProgressBar(df[column].count(), l, prefix='Filled:', suffix='Rows', length=50)
            print('')

        if plot == True:
            df[column].notna().astype(int).plot(x='index', figsize=(16,4)).legend()
            plt.show()
            plt.close()

        print('')

def print_full(df = pd.DataFrame):
    pd.set_option('display.max_rows', len(df))
    print(df)
    pd.reset_option('display.max_rows')

def invokes_influenced_is_influenced_by_stacked_bar_chart(dataFrameToAnalyze=pd.DataFrame,
                                                invokesInfluence=str,
                                                isInfluencedBy=str,
                                                CountOfTopValuesInvokesInfluence=int,
                                                CountOfTopValuesIsInfluencedBy=int,
                                                binnedData=False,
                                                orderedLegend=None):

    # top columns of invokesInfluence
    topDf = dataFrameToAnalyze[invokesInfluence].value_counts().nlargest(
        CountOfTopValuesInvokesInfluence).reset_index()
    topDf.columns = [invokesInfluence, 'count']
    topDf = topDf.set_index([invokesInfluence])
    df_top = dataFrameToAnalyze.loc[
        dataFrameToAnalyze[invokesInfluence].isin(topDf.reset_index()[invokesInfluence])]

    # top columns of isInfluencedBy
    topDfInfluencedBy = dataFrameToAnalyze[isInfluencedBy].value_counts().nlargest(
        CountOfTopValuesIsInfluencedBy).reset_index()
    topDfInfluencedBy.columns = [isInfluencedBy, 'count']
    topDfInfluencedBy = topDfInfluencedBy.set_index([isInfluencedBy])
    df_top = df_top.loc[df_top[isInfluencedBy].isin(topDfInfluencedBy.reset_index()[isInfluencedBy])]

    df_top_normalized_case_status = df_top[isInfluencedBy].groupby(df_top[invokesInfluence]).value_counts(
        normalize=True).mul(100).reset_index(name='counts')

    df_top_normalized_case_status = df_top_normalized_case_status.pivot(index=invokesInfluence,
                                                                        columns=isInfluencedBy, values="counts")

    df_top_normalized_case_status = df_top_normalized_case_status.merge(topDf, left_on=invokesInfluence,
                                                                        right_on=invokesInfluence)

    if binnedData == True:
        df_top_normalized_case_status = df_top_normalized_case_status.sort_values(by=[invokesInfluence],
                                                                                  ascending=False)
    else:
        df_top_normalized_case_status = df_top_normalized_case_status.sort_values(by=['count'], ascending=False)

    df_top_normalized_case_status = df_top_normalized_case_status.fillna(0)

    del df_top_normalized_case_status["count"]

    # print(df_top_normalized_case_status.head(20))

    # df_top_normalized_case_status[dataFrameToAnalyze[isInfluencedBy].unique()].plot.bar(stacked=True, figsize=(10,5))

    #df_top_normalized_case_status[legend].plot.bar(stacked=True, figsize=(20,10))

    if orderedLegend is not None:
        df_top_normalized_case_status.unstack()

        df_top_normalized_case_status.columns = pd.CategoricalIndex(df_top_normalized_case_status.columns.values,
                                                                    ordered=True,
                                                                    categories=orderedLegend)

        df_top_normalized_case_status = df_top_normalized_case_status.sort_index(axis=1)

        ax = df_top_normalized_case_status.plot.bar(stacked=True, figsize=(20, 10))
        ax.set_ylim(ymax=100)

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(reversed(handles), reversed(labels))
    else:
        # Die Label werden umgekehrt der angezeigten Reihenfolge in der Legende angezeigt. Das wird hiermit umgekehrt.
        legend = list(df_top_normalized_case_status.loc[:, df_top_normalized_case_status.columns != 'count'].columns)
        ax = df_top_normalized_case_status[legend].plot.bar(stacked=True, figsize=(20, 10))
        ax.set_ylim(ymax=100)

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(reversed(handles), reversed(labels))

    plt.show()
