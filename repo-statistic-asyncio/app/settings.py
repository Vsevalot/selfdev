from envparse import env

env.read_envfile()

GITHUB_TOKEN = env('GITHUB_TOKEN', '', cast=str)
if GITHUB_TOKEN == '':
    raise EnvironmentError("You must specify GITHUB_TOKEN to run analysis")
