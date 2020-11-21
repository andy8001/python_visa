import pandas

def print_count_of_values_relation(df = pandas.DataFrame):
    index = df.index
    number_of_rows = len(index)

    headers = list(df)

    for x in list(df):
        column = (headers.pop(0))
        print(column)
        # display(Markdown("# " + column_object))
        print(
            str(df[column].count()) + "/" + str(number_of_rows) + " " + str("{:.0%}".format(df[column].count() / number_of_rows) ))
        print('')

