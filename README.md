# selfdev
Self development projects

This repository contains projects that I made to train concepts, technologies, and libraries.

Completed projects:

## Repository statistic (_repo statistic_)
A small python script working with [GITHUB REST API](https://docs.github.com/en/rest). 
Uses only standart library and requests module. Takes a link to any open github repository, since(optional), until(optional) date, 
branch name(optional, default - master) and collect statistic of:
  * Top N contributors for the given time period and branch. N is confugable through sript flags, default 30
  * Number of opened pull request, number of closed PR for the given time period and branch. 
  Number of old PR - that were opened in the given time period and still be opened for M days. N is confugable through sript flags, default 30
  * Number of opened issues, number of closed issues for the given time period and branch. 
  Number of old issues - that were opened in the given time period and still be opened for K days. K is confugable through sript flags, default 14
  
