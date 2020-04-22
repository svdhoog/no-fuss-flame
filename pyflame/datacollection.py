import os
import xml.etree.ElementTree as et
import sys

def collect_run(path, variables, burn_in_its=0, max_its = 1000000000000):
    # Collect iteration numbers
    its = []
    for file in os.listdir(path):
        if file.endswith(".xml"):
            it = file[:-4]
            if it.isdigit():
                if int(it) >= burn_in_its and int(it) <= max_its:
                    its.append(int(it))
    its.sort()

    # Prepare data dict
    data = {}
    for a in variables:
        data[a] = {}
        for v in variables[a]:
            data[a][v]=[]

    for it in its:
        tree = et.parse(path + "/" + str(it) + ".xml")
        root = tree.getroot()

        for a in variables:
            for v in variables[a]:
                values_dict = dict()
                for xagent in root.findall('xagent'):
                    if xagent.find('name').text == a:
                        try:
                            id = int(xagent.find("id").text)
                            values_dict[id] = float(xagent.find(v).text)
                        except:
                            pass

                values = []
                keylist = list(values_dict.keys())
                keylist.sort()

                for k in keylist:
                    values.append(values_dict[k])

                data[a][v].append(values)

    return data


def aggregate_agents(data, function):
    agg = {}
    for a in data:
        agg[a] = {}
        for v in data[a]:
            values = list(map(lambda l : function(l), data[a][v]))
            agg[a][v] = values

    return agg


def aggregate_runs(data, function):
    agg = {}
    for a in data[0]:
        agg[a] = {}
        for v in data[0][a]:
            temp = []
            for i in range(0,len(data)):
                temp.append(data[i][a][v])
            agg[a][v] = function(temp)

    return agg

