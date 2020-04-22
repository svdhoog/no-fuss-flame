import prettytable as pt
import csv

def write_corr_matrix(data, header, save_as_file=None, show=False):

    field_names = ["Correlation"] + header

    table = pt.PrettyTable()
    table.field_names = field_names

    for i in range(0, len(header)):
        row = [header[i]]
        for c in data[i]:
            row.append(c)

        table.add_row(row)
    if save_as_file is not None:
        with open(save_as_file + ".txt", "w") as file:
            file.write(table.get_string())

    if show:
        print(table.get_string())

def write_corr_table(data, header, first_col, pvalues=None, save_as_file=None, show=False):

    if pvalues is None:
        field_names = ["Correlation"] + header
    else:
        field_names = ["Correlation"]
        for h in header:
            field_names = field_names + [h, h + " (p-value)"]

    table = pt.PrettyTable()
    table.field_names = field_names

    for i in range(0, len(first_col)):
        row = [first_col[i]]
        for j in range(0, len(data[i])):
            row.append(round(data[i][j], 4))
            if pvalues is  not None:
                row.append(round(pvalues[i][j], 4))
        table.add_row(row)

    if save_as_file is not None:
        with open(save_as_file + ".txt", "w") as file:
            file.write(table.get_string())

    if show:
        print(table.get_string())


def write_dataseries_csv(data, header, filename):
    mod_header = []

    for h in header:
        for y in range(0, len(data[0])):
            mod_header.append(h + "_" + str(y))

    with open(filename + ".csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(mod_header)

        for z in range(0,len(data[0][0])):
            row = []
            for x in range(0, len(data)):
                for y in range(0, len(data[0])):
                    row.append(data[x][y][z])
            csvwriter.writerow(row)


def write_corr_matrix_csv(data, header, filename):
    with open(filename + ".csv", 'w') as csvfile:
        field_names = ["Correlation"] + header

        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(field_names)

        for i in range(0, len(header)):
            row = [header[i]]
            for c in data[i]:
                row.append(c)
            csvwriter.writerow(row)


def write_corr_table_csv(data, header, first_row, filename, pvalues=None):
    with open(filename + ".csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        if pvalues is None:
            csvwriter.writerow(["Correlation"] + header)
        else:
            field_names = ["Correlation"]
            for h in header:
                field_names = field_names + [h, h + " (p-value)"]
            csvwriter.writerow(field_names)

        for i in range(0, len(first_row)):
            row = [first_row[i]]
            for j in range(0, len(data[i])):
                row.append(data[i][j])
                if pvalues is not None:
                    row.append(pvalues[i][j])
            csvwriter.writerow(row)
