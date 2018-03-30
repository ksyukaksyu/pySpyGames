import requests
import time
import pprint
import json


# ВОПРОС 1: нужно ли писать авторизацию? Или это только для приложения в вк?

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


class VKController:
    def __init__(self, token):
        self.token = token
        self.params = {
            'v': '5.73',
            'access_token': self.token,
        }

    def get_request(self, method_name):
        return set(requests.get(
            'https://api.vk.com/method/{}?'.format(method_name),
            params=self.params
        ))

    def get_request_response_items(self, method_name):
        return set(requests.get(
            'https://api.vk.com/method/{}?'.format(method_name),
            params=self.params
        ).json()['response']['items'])


class VKUser(VKController):
    def __init__(self, token, user):
        super().__init__(token)
        self.params['user_ids'] = user

    # ВАРИАНТ 2
    def get_unmutual_groups(self):
        unmutual_groups = set()
        for group in self.get_request_response_items('groups.get'):
            self.params['filter'] = 'friends'
            self.params['group_id'] = group
            time.sleep(0.3)
            if not self.get_request_response_items('groups.getMembers'):
                unmutual_groups.add(str(group))
        return unmutual_groups


y = VKUser(TOKEN_VK, 5030613)

# get_user_friends = set(requests.get(
#     'https://api.vk.com/method/friends.get?',
#     params=user_params
# ).json()['response']['items'])

print('ID друзей юзера:', len(y.get_request_response_items('friends.get')), y.get_request_response_items('friends.get'))

# get_user_groups = set(requests.get(
#     'https://api.vk.com/method/groups.get?',
#     params=user_params
# ).json()['response']['items'])

print('ID групп юзера:', len(y.get_request_response_items('groups.get')), y.get_request_response_items('groups.get'))

# ВОПРОС 2: Нашла 2 варианта решения задачи поиска групп, в которых не состоят друзья юзера. В первом варианте
# (закомменчен) мы ищем соотвествие между членами группы и друзьями юзера через множества. Если пересечения нет,
# запоминаем id группы. Во втором варианте мы, используя параметры api, получаем только тех участников, кто дружит
# с юзером.
# Проблема: в первом варианте получается групп больше, неясно, почему. Во втором варианте групп меньше, но эти группы
# являются подмножеством множества результатов от первого варианта.
# Я выбрала второй вариант решения, потому что, на мой взгляд, он более бережливый. Но меня смущает разница в
# результатах. Буду рада, если вы поможете разобраться.

# unmutual_groups = set()

# ВАРИАНТ 1
# for group in get_user_groups:
#     group_params = {
#         'group_id': group,
#         'v': '5.73',
#         'access_token': TOKEN_VK,
#     }
#     time.sleep(0.3)
#     get_group_members = set(requests.get(
#         'https://api.vk.com/method/groups.getMembers?',
#         params=group_params
#     ).json()['response']['items'])
#
#     if not get_group_members & get_user_friends:
#         unmutual_groups.add(str(group))

# ВАРИАНТ 2
# for group in get_user_groups:
#     group_params = {
#         'group_id': group,
#         'filter': 'friends',
#         'v': '5.73',
#         'access_token': TOKEN_VK,
#     }
#     time.sleep(0.3)
#     get_group_members = set(requests.get(
#         'https://api.vk.com/method/groups.getMembers?',
#         params=group_params
#     ).json()['response']['items'])
#
#     if not get_group_members:
#         unmutual_groups.add(str(group))

print('ID групп юзера, где нет друзей:', y.get_unmutual_groups())

# fre = {}
# count = None
# ginfo = None
# lits = []
# for g in unmutual_groups:
#     group_params2 = {
#         'group_id': g,
#         'v': '5.73',
#         'access_token': TOKEN_VK,
#     }
#     time.sleep(0.3)
#
#     ginfo = requests.get(
#         'https://api.vk.com/method/groups.getById?',
#         params=group_params2
#     ).json()['response']
#
#     time.sleep(0.3)
#
#     count = requests.get(
#         'https://api.vk.com/method/groups.getMembers?',
#         params=group_params2
#     ).json()['response']['count']
#
#     d = {
#         'name': ginfo[0]['name'],
#         'gid': str(g),
#         'members_count': count,
#     }
#     lits.append(d)
#
# pprint.pprint(lits)
#
# with open('groups.json', 'w') as f:
#     json.dump(lits, f)
