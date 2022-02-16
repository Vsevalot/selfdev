A python script working with [GITHUB REST API](https://docs.github.com/en/rest)
to analyse repositories. Takes a link to any open GitHub repository,
since(optional), until(optional) date, branch name(optional)
and collect statistic of:
  * Top N contributors for the given time period. N is configurable through script flags, default 20
  * Number of the opened pull requests, number of closed PR for the given time period. 
  The number of old: PRs which were opened in the given time period and still be opened for N days. N is configurable through script flags, default 14
  * Number of opened issues, number of closed issues for the given time period. 
  The number of old issues - same as for PRs

The script can work in 2 mods: lazy and async (default). Run script 
with -h flag to read more.
  
  ```
  .../repo-statistic-asyncio$ python cly.py -h
 usage: cli.py [-h] [--since SINCE] [--until UNTIL] [--branch BRANCH]
              [--token TOKEN] [--top_contributors TOP_CONTRIBUTORS]
              [--days_to_old DAYS_TO_OLD] [-l]
              url

Statistic of repository contributors, pull requests and issues. Collects
statistic for contributors, PR and issues in the given time period (optional)
and the given branch (default is repo main branch) - contributors and PR only

positional arguments:
  url                   URL of a github repository. Expects URL in form
                        https://github.com/OWNER/REPOSITORY

options:
  -h, --help            show this help message and exit
  --since SINCE, -s SINCE
                        Since which date collect statistic. Expects date in
                        next forms: YYYY-MM-DD / DD.MM.YYYY / DD.MM.YY.
                        Collects statistic since the big bang if not set
  --until UNTIL, -u UNTIL
                        Until which date collect statistic. Expects date in
                        next forms: YYYY-MM-DD / DD.MM.YYYY / DD.MM.YY.
                        Collects statistic until current time if not set
  --branch BRANCH, -b BRANCH
                        Name of a branch for contributors. Default - repo main
                        branch
  --token TOKEN, -t TOKEN
                        Your personal github token to authorize and increase
                        the number of request from 60 to 5000 per hour
  --top_contributors TOP_CONTRIBUTORS, -top_n TOP_CONTRIBUTORS
                        The number of top contributors to be printed. Default
                        value is 20
  --days_to_old DAYS_TO_OLD, -dto DAYS_TO_OLD
                        If a PR/ISSUE is created in the given time period and
                        still be opened for this number of days or more, it's
                        consider to be an old one. The default value is 14
  -l                    Collect statistic lazy. Works slower, but consumes
                        less memory

```

Example:

```
.../repo-statistic-asyncio$ python cli.py https://github.com/aio-libs/aiohttp \ 
-t YOUR_TOKEN -top_n=30

Top 30 contributors for: https://github.com/aio-libs/aiohttp
Branch - main repository branch
Time period: for all time

Login                         | Commits made
____________________________________________
asvetlov                      |         4382
fafhrd91                      |          775
dependabot[bot]               |          418
webknjaz                      |          269
dependabot-preview[bot]       |          235
Nikolay Kim                   |          212
pyup-bot                      |          206
patchback[bot]                |           99
kxepal                        |           79
popravich                     |           72
Dreamsorcerer                 |           45
jashandeep-sohi               |           45
samuelcolvin                  |           37
aio-libs-github-bot[bot]      |           33
mind1m                        |           33
pfreixes                      |           28
arthurdarcet                  |           27
derlih                        |           25
jettify                       |           25
rutsky                        |           23
l1storez                      |           22
socketpair                    |           22
github-actions[bot]           |           20
redixin                       |           19
andrewleech                   |           19
Marco Paolini                 |           19
greshilov                     |           17
argaen                        |           17
alexdutton                    |           16
scop                          |           13

Pull requests statistic for: https://github.com/aio-libs/aiohttp
Time period: for all time
State       | Number
____________________
open        |     84
closed      |   3883
old         |     48

Issues statistic for: https://github.com/aio-libs/aiohttp
Time period: for all time
State       | Number
____________________
open        |    407
closed      |   6093
old         |    361

main_async run in 432.89013147354126

```

  


QUESTIONS:
- Isn't it weird that _get_async returns all pages at once?
- Can I make a single wrapper for both sync and async functions?
- What is the type hint for async stopwatch?
- defaultdict(lambda: 0) ... rly? I just want a default 0
- PR and Issue relations. PR is basically an issue. Now I just use params from
issues. It looks wrong. But I don't want to duplicate code.
- Isn't there too many for the Github client?
- How to write get functions without code duplication?
- Sorting in dunder str doesn't look good
- Validation and argument parsing messed up