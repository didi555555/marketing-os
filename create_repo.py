import requests, sys

token = 'ghp_YOUR_TOKEN_HERE'
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
data = {'name': 'marketing-os', 'description': 'منصة تسويق متكاملة - Marketing OS', 'private': False, 'auto_init': False}

r = requests.post('https://api.github.com/user/repos', headers=headers, json=data)
if r.status_code == 201:
    print('SUCCESS:', r.json()['clone_url'])
else:
    print(f'ERROR {r.status_code}: {r.json().get("message", r.text)}')
