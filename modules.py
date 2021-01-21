import pandas as pd
import matplotlib.pyplot as plt

# Quelle der nachfolgenden Funktion ist:
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


def print_count_of_values_relation(df: pd.DataFrame, progressBar: bool, plot: bool):
    """
    Print how many values could be found in each row.
    :param progressBar:     - Required  :  progressbar printout (bool)
    :param df:              - Required  :  dataFrame (pandas.DataFrame)
    :param plot:            - Required  :  plot as linechart (bool)
    """
    #To explain the resulting graphs: The X - Axis shows the index of all values.We
    # The Y - Axis shows if a row is filled with a actual value.
    # Not NaN Values are displayed as 1, NaN values are displayed as 0.

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

def invokes_influence_is_influenced_by_stacked_bar_chart(dataFrameToAnalyze=pd.DataFrame,
                                                         invokesInfluence=str,
                                                         isInfluencedBy=str,
                                                         CountOfTopValuesInvokesInfluence=int,
                                                         CountOfTopValuesIsInfluencedBy=int,
                                                         sortAlphabetically=False,
                                                         orderedLegend=None,
                                                         medianLineInt=None,
                                                         barh = False):

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

    if sortAlphabetically == True:
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
        if barh == True:
            ax = df_top_normalized_case_status.plot.barh(stacked=True, figsize=(20, 10))
            ax.set_xlim(xmax=100)
            ax.invert_yaxis()

            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles, labels, loc="center left", bbox_to_anchor=(1, 0.5))
        else:
            ax = df_top_normalized_case_status.plot.bar(stacked=True, figsize=(20, 10))
            ax.set_ylim(ymax=100)

            #Die Label soll vertauscht werden um die Lesbarkeit des Graphen zu vereinfachen
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(reversed(handles), reversed(labels), loc="center left", bbox_to_anchor=(1, 0.5))


        #Die Legende soll außerhalb des Graphen angezeigt werden
        #https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
        # Shrink current axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

    else:
        # Die Label werden umgekehrt der angezeigten Reihenfolge in der Legende angezeigt. Das wird hiermit umgekehrt.
        legend = list(df_top_normalized_case_status.loc[:, df_top_normalized_case_status.columns != 'count'].columns)

        if barh == True:
            ax = df_top_normalized_case_status[legend].plot.barh(stacked=True, figsize=(20, 10))
            ax.set_xlim(xmax=100)
            ax.invert_yaxis()
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles, labels, loc="center left", bbox_to_anchor=(1, 0.5))

        else:
            ax = df_top_normalized_case_status[legend].plot.bar(stacked=True, figsize=(20, 10))
            ax.set_ylim(ymax=100)

            #Die Label soll vertauscht werden um die Lesbarkeit des Graphen zu vereinfachen
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(reversed(handles), reversed(labels), loc="center left", bbox_to_anchor=(1, 0.5))

        # Die Legende soll außerhalb des Graphen angezeigt werden
        # https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
        # Shrink current axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

    if medianLineInt is not None:
        plt.axhline(medianLineInt, color='r', linestyle='--')

        if barh == True:
            plt.axvline(medianLineInt, color='r', linestyle='--')
        else:
            plt.axhline(medianLineInt, color='r', linestyle='--')

    plt.show()

def areTwoColumnsOverlapping(df=pd.DataFrame, firstColumn = str, secondColumn = str):
    return (~(df[firstColumn].isna() + df[secondColumn].isna())).sum() > 0

