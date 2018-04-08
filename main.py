import requests
from time import sleep
import json

TOKEN_VK = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'


class VKController:
    def __init__(self, token):
        self.token = token
        self.version = '5.73'

    def get_request(self, method_name, params = None):
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

    @classmethod
    def save_to_json(cls, file_name, data):
        with open('{}.json'.format(file_name), 'w') as f:
            json.dump(data, f, ensure_ascii = False, indent = 4)
        print('Список групп доступен в файле {}.json.'.format(file_name))


class VKUser(VKController):
    def __init__(self, token, user):
        super().__init__(token)
        self.user_id = user

    def get_different_groups(self):
        different_groups = set()
        user_friends = set(self.get_request_response_items('friends.get', {
            'user_ids': self.user_id
        }))
        for group in self.get_request_response_items('groups.get', {
            'user_ids': self.user_id
        }):
            group_members = set(self.get_request_response_items('groups.getMembers', {
                'group_id': group
            }))
            if not (group_members & user_friends):
                different_groups.add(str(group))
        return different_groups

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
    user.save_to_json('groups', user.get_group_info(user.get_different_groups()))


main()
