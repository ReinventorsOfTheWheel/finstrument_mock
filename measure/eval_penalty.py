#!/usr/bin/env python

import os
from matplotlib import rc
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import argparse


def plot(csetup, value, name):
    ind = np.arange(len(csetup)) + .5
    plt.barh(ind, value, align='center', height=0.6)
    plt.yticks(ind, csetup)

    plt.title(name)
    # plt.xlabel('seconds')
    #plt.ylabel('compiler setup')

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

    plt.show()


# Returns a dict for a result file
#  key: penalty name, e.g. 'Penalty'
#  value: penalty value
def parse_result_file(filename):
    result = {}
    with open(filename) as f:
        for line in f:
            key = ""
            value = -1.0
            if "Penalty" in line:
                parts = line.split(":")
                key = parts[0]
                value = float(parts[1].strip().split(" ")[0])
            else:
                continue
            assert len(key) > 0
            assert value >= 0.0
            result[key] = value
    return result


def plot_all_results():
    for dir in [
        'O2',
        'O0',
        'O2__fsanitize_mock',
        'O2__fsanitize_mock__fno-inline-functions',
        'O2__finstrument-functions'
    ]:
        result_file = os.path.join(dir, "report.txt")
        print result_file
        result = parse_result_file(result_file)
        compiler_setup = "-" + result_file.split(
            "/")[0].replace("__", " -").replace("_mock", "=mock")
        plot(result.keys(), result.values(), compiler_setup)

plot_all_results()
