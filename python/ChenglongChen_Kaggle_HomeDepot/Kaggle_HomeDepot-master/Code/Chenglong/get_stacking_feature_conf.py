# -*- coding: utf-8 -*-
"""
@author: Chenglong Chen <c.chenglong@gmail.com>
@brief: generate stacking feature conf for 2nd and 3rd level models

"""

import os
import re
from optparse import OptionParser

import pandas as pd

import config
from utils import time_utils


def grab(pattern, text):
    pat = re.compile(pattern)
    group = re.findall(pat, text)
    return group


def check_valid(model):
    file = "%s/All/test.pred.%s.csv" % (config.OUTPUT_DIR, model)
    try:
        df = pd.read_csv(file)
        if df.shape[0] == config.TEST_SIZE:
            return True
        else:
            return False
    except:
        return False


def get_model_list(log_folder, topN):
    tasks_ens = []
    for file in sorted(os.listdir(log_folder)):
        if not os.path.isfile(os.path.join(log_folder, file)):
            continue
        text = open(os.path.join(log_folder, file), "r").read()

        # grab everything we need
        tasks = grab("(\[Feat@.*)", text)
        rmse_mean = grab("Mean: (.*)", text)
        rmse_std = grab("Std: (.*)", text)
        rmse_mean = [float(x) for x in rmse_mean]
        rmse_std = [float(x) for x in rmse_std]
        L = min(len(tasks), len(rmse_mean), len(rmse_std))
        d = dict(zip(tasks[:L], rmse_mean[:L]))

        # keep the top-N
        ds = sorted(d.items(), key=lambda x: float(x[1]))
        cnt = 0
        for t,v in ds:
            if check_valid(t):
                tasks_ens.append(t)
                print("Read %s : %.6f"%(t, v))
                cnt += 1
                if cnt >= topN:
                    break
        if cnt > 0:
            print("Read %d models from %s"%(cnt, file))

    return tasks_ens


header_pattern = """
# -*- coding: utf-8 -*-
\"\"\"
@author: Chenglong Chen <c.chenglong@gmail.com>
@brief: one stacking feature conf

Generated by
python %s -l %s -t %d -o %s

\"\"\"

feature_list = [

"""


def _create_feature_conf(level, topN, outfile):
    log_folder = "%s/level%d_models"%(config.LOG_DIR, level)
    feature_list = get_model_list(log_folder, topN)
    res = header_pattern%(__file__, level, int(topN), outfile)
    for feature in feature_list:
        res += '"%s",\n'%feature
    res += "]\n"
    with open(os.path.join(config.FEAT_CONF_DIR, outfile), "w") as f:
        f.write(res)


def main(options):
    _create_feature_conf(level=options.level, topN=options.topN, outfile=options.outfile)


def parse_args(parser):
    parser.add_option("-l", "--level", default=2, 
        type="int", dest="level", help="level")
    parser.add_option("-t", "--top", default=10, 
        type="int", dest="topN", help="top-N")
    parser.add_option("-o", "--outfile", 
        default="stacking_feature_conf_%s.py"%time_utils._timestamp(),
        type="string", dest="outfile", help="outfile")
    (options, args) = parser.parse_args()
    return options, args


if __name__ == "__main__":
    parser = OptionParser()
    options, args = parse_args(parser)
    main(options)