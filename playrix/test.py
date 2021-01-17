#!/usr/bin/python

import argparse
from typing import Dict, Union

def get_arg_dict() -> Dict[str, Union[str, int, None]]:
    parser = argparse.ArgumentParser(description="Statistic of repository contributors, pull requests and issues. "
                                                 "Collects statistic for contributors, PR and issues in "
                                                 "the given time period (optional) and "
                                                 "the given branch (default is master) - contributors and PR only")
    parser.add_argument("url", type=str, help="URL of a github repository. "
                                              "Expects url in form https://github.com/OWNER/REPOSITORY")
    parser.add_argument("--since", "-s", type=str,
                        help="Since which date collect statistic for contributors and PR statistic. "
                             "Expects date in github form: YYYY-MM-DD. "
                             "If not set, collects statistic since first record/the big bang")
    parser.add_argument("--until", "-u", type=str,
                        help="Until which date collect statistic for contributors and PR statistic "
                             "Expects date in github form: YYYY-MM-DD. "
                             "If not set, collects statistic until last record/university heat death")
    parser.add_argument("--branch", "-b", type=str, default="master",
                        help="Name of a branch for contributors and PR statistic, default - master")
    parser.add_argument("--top_contributors", "-tc", type=int, default=30,
                        help="Number of required top contributors. The default value is 30")
    parser.add_argument("--pr_days_to_old", "-pro", type=int, default=30,
                        help="If an PR is created in the given time period and still be opened for days_to_old "
                             "or more it's consider to be an old one. The default value is 30")
    parser.add_argument("--issue_days_to_old", "-io", type=int, default=14,
                        help="If an issue is created in the given time period and still be opened for "
                             "issue_days_to_old or more it's consider to be an old one. The default value is 14")
    parser.add_argument("--visual_progress", "-vp", type=bool, default=True,
                        help="Visual progress. Each request takes from 1 to 10 seconds. To visualize that the script "
                             "is working print's a dot with each get request. The default value is True")

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = get_arg_dict()
    print(type(args))
    print(args)
