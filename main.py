import requests
import time

# AUTH_URL = 'https://oauth.vk.com/authorize?'
#
# params = {
#     'client_id': '',
#     'display': 'page',
#     'redirect_uri': 'https://oauth.vk.com/blank.html',
#     'scope': 'friends',
#     'response_type': 'token',
#     'v': '5.52',
# }
# auth = requests.get(AUTH_URL, params=params)
# print(auth.url)

TOKEN_VK = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'

user_params = {
    'user_ids': 'tim_leary',
    # or '5030613'
    'v': '5.73',
    'access_token': TOKEN_VK,
}

get_user_friends = set(requests.get(
    'https://api.vk.com/method/friends.get?',
    params=user_params
).json()['response']['items'])

print('ID друзей юзера:', len(get_user_friends), get_user_friends)

get_user_groups = set(requests.get(
    'https://api.vk.com/method/groups.get?',
    params=user_params
).json()['response']['items'])

print('ID групп юзера:', len(get_user_groups), get_user_groups)

mutual_groups = set()

for group in get_user_groups:
    group_params = {
        'group_id': group,
        'v': '5.73',
        'access_token': TOKEN_VK,
    }
    time.sleep(0.3)
    get_group_members = set(requests.get(
        'https://api.vk.com/method/groups.getMembers?',
        params=group_params
    ).json()['response']['items'])

    if get_group_members & get_user_friends:
        mutual_groups.add(str(group))

group_params2 = {
    'group_ids': ', '.join(mutual_groups),
    'v': '5.73',
    'access_token': TOKEN_VK,
}
print(requests.get(
    'https://api.vk.com/method/groups.getById?',
    params=group_params2
).json()['response'])

get_group_members2 = requests.get(
    'https://api.vk.com/method/groups.getMembers?',
    params=group_params2
).json()
print(get_group_members2)
