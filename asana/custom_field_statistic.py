import asana
from envparse import env
from collections import namedtuple, defaultdict

env.read_envfile()
TOKENS = env.tuple('TOKENS', default=('TOKENS HERE OR IN ENV', ))
WORKSPACE_GID = env.str('WORKSPACE_GID', default='656176460444')

Project = namedtuple('Project', 'name url')


def get_projects_with_custom_field(
        client,
        cf_gid: str,
) -> set[namedtuple]:
    payload = {
        'workspace': WORKSPACE_GID,
        'opt_fields': [
            'name',
            'custom_field_settings.custom_field.name',
            'permalink_url',
        ]
    }
    projects = set()
    for p in client.projects.get_projects(params=payload):
        for cfs in p['custom_field_settings']:
            if cfs['custom_field']['gid'] == cf_gid:
                projects.add(
                    Project(
                        name=p['name'],
                        url=p['permalink_url'],
                    )
                )
    return projects


if __name__ == '__main__':
    custom_field_gid = 'CUSTOM FIELD GID'

    projects_with_custom_field = defaultdict(list)
    for t in TOKENS:
        client = asana.Client.access_token(t)
        account_email = client.users.me()['email']
        print(f'Scanning projects with {account_email}')

        projects = get_projects_with_custom_field(client, custom_field_gid)
        for p in projects:
            projects_with_custom_field[p].append(account_email)

    result_path = f'projects_with_cf_{custom_field_gid}.csv'
    with open(result_path, 'w') as file:
        file.write('Project name;Project url;Accounts with access\n')
        for p, accounts in projects_with_custom_field.items():
            file.write(f'{p.name};{p.url};{", ".join(accounts)}\n')
    print(f'We are done! Check results in '
          f'{f"projects_with_cf_{custom_field_gid}.csv"}')
