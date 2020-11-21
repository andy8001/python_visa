import pandas
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


def print_count_of_values_relation(df: pandas.DataFrame, progressBar: bool, plot: bool):
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
