A small python script working with [GITHUB REST API](https://docs.github.com/en/rest). 
Uses only standart library and requests module. Takes a link to any open github repository, since(optional), until(optional) date, 
branch name(optional, default - master) and collect statistic of:
  * Top N contributors for the given time period and branch. N is confugable through sript flags, default 30
  * Number of opened pull request, number of closed PR for the given time period and branch. 
  Number of old PR - that were opened in the given time period and still be opened for M days. N is confugable through sript flags, default 30
  * Number of opened issues, number of closed issues for the given time period and branch. 
  Number of old issues - that were opened in the given time period and still be opened for K days. K is confugable through sript flags, default 14
  

  
  The script uses argparse to handle all parameters and flags. Run script with -h flag to print help.
  ```
  python repo_statistic.py -h
  
Statistic of repository contributors, pull requests and issues. Collects
statistic for contributors, PR and issues in the given time period (optional)
and the given branch (default is master) - contributors and PR only

positional arguments:
  url                   URL of a github repository. Expects URL in form
                        https://github.com/OWNER/REPOSITORY

optional arguments:
  -h, --help            show this help message and exit
  --since SINCE, -s SINCE
                        Since which date collect statistic for contributors
                        and PR statistic. Expects date in github form: YYYY-
                        MM-DD. If not set, collects statistic since first
                        record/the big bang
  --until UNTIL, -u UNTIL
                        Until which date collect statistic for contributors
                        and PR statistic Expects date in github form: YYYY-MM-
                        DD. If not set, collects statistic until last
                        record/universe heat death
  --branch BRANCH, -b BRANCH
                        Name of a branch for contributors and PR statistic,
                        default - master
  --username USERNAME, -un USERNAME
                        You can pass your github username to authorize and
                        increase the number of request from 60 to 5000 per
                        hour
  --token TOKEN, -t TOKEN
                        You can pass your personal github token to authorize
                        and increase the number of request from 60 to 5000 per
                        hour
  --top_contributors TOP_CONTRIBUTORS, -tc TOP_CONTRIBUTORS
                        Number of required top contributors. The default value
                        is 30
  --pr_days_to_old PR_DAYS_TO_OLD, -pro PR_DAYS_TO_OLD
                        If an PR is created in the given time period and still
                        be opened for pr_days_to_old or more it's consider to be
                        an old one. The default value is 30
  --issue_days_to_old ISSUE_DAYS_TO_OLD, -io ISSUE_DAYS_TO_OLD
                        If an issue is created in the given time period and
                        still be opened for issue_days_to_old or more it's
                        consider to be an old one. The default value is 14
  --request_timeout REQUEST_TIMEOUT, -rto REQUEST_TIMEOUT
                        Each request takes from 1 to inf seconds. If a server
                        needs more time to respond, you can modify number of
                        seconds for request timeout. Default value is 10
                        seconds
  --visual_progress VISUAL_PROGRESS, -vp VISUAL_PROGRESS
                        Visual progress. Each request takes from 1 to inf
                        seconds. To visualize that the script is working
                        prints a dot with each get request. The default value
                        is True
```

Example:

```
python repo_statistic.py https://github.com/octocat/hello-world -u=2020-01-01
Collecting data for https://github.com/octocat/hello-world until 2020-01-01, master

Collecting contributors data. It might take a few minutes.
.
List of the most active contributors until 2020-01-01 for master
Login                                   contributions
-----------------------------------------------------
octocat                                             1
Spaceghost                                          1

Collecting pull requests data. It might take a few minutes.
....
Pull request data until 2020-01-01 for master:
Opened:           273
Closed:            66
Old:              200

Collecting issues data. It might take a few minutes.
........
Issues data until 2020-01-01:
Opened:           551
Closed:           172
Old:              370

Process finished with exit code 0

```
