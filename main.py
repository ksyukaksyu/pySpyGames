import requests
from time import sleep
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
        self.version = '5.73'

    def get_request(self, method_name, params = {}):
        sleep(0.3)
        print('    Request {}... '.format(method_name))
        params['v'] = self.version
        params['access_token'] = self.token
        return requests.get(
            'https://api.vk.com/method/{}?'.format(method_name),
            params = params
        ).json()

    def get_request_response_items(self, method_name, params):
        return self.get_request(method_name, params)['response']['items']

    def save_to_json(self, file_name, data):
        with open('{}.json'.format(file_name), 'w') as f:
            json.dump(data, f, ensure_ascii = False, indent = 4)
        print('Список групп доступен в файле {}.json.'.format(file_name))


class VKUser(VKController):
    def __init__(self, token, user):
        super().__init__(token)
        self.user_id = user

    def get_unmutual_groups(self):
        unmutual_groups = set()
        for group in self.get_request_response_items('groups.get', {
            'user_ids': self.user_id
        }):

            if not self.get_request_response_items('groups.getMembers', {
                'filter': 'friends',
                'group_id': group
            }):
                unmutual_groups.add(str(group))
        return unmutual_groups

    def get_group_info(self, data):
        group_info_list = []
        for group in data:
            group_main_info = self.get_request('groups.getById', {
                'group_id': group
            })
            group_count = self.get_request('groups.getMembers', {
                'group_id': group
            })
            group_info = {
                'name': group_main_info['response'][0]['name'],
                'gid': str(group),
                'members_count': group_count['response']['count'],
            }
            group_info_list.append(group_info)
        return group_info_list


def main():
    user = VKUser(TOKEN_VK, input('Введите id или короткий адрес пользователя VK: '))
    user.save_to_json('groups', user.get_group_info(user.get_unmutual_groups()))


main()

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
