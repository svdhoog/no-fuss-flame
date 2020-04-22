import os
import shutil

def create_folder(f):
    if not os.path.exists(f):
        os.makedirs(f)


def delete_folder(f):
    if os.path.exists(f):
        shutil.rmtree(f)


def get_label_from_corr_pair(corr_pair):
    agent0 = list(corr_pair[0].keys())[0]
    var0 = corr_pair[0][agent0]
    agent1 = list(corr_pair[1].keys())[0]
    var1 = corr_pair[1][agent1]

    label = agent0 + "_" + var0 + "-" + agent1 + "_" + var1

    return label
