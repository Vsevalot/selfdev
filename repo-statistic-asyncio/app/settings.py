from envparse import env

env.read_envfile()

GITHUB_TOKEN = env('GITHUB_TOKEN', '', cast=str)
