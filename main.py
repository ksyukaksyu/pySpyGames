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
        # print('    Request {}... '.format(method_name))
        params['v'] = self.version
        params['access_token'] = self.token
        return requests.get(
            'https://api.vk.com/method/{}?'.format(method_name),
            params = params
        ).json()

    def get_request_response_items(self, method_name, params):
        response = self.get_request(method_name, params)
        if 'response' in response:
            return response['response']['items']
        else:
            return []

    @classmethod
    def save_to_json(cls, file_name, data):
        with open('{}.json'.format(file_name), 'w') as f:
            json.dump(data, f, ensure_ascii = False, indent = 4)
        print('Список групп доступен в файле {}.json.'.format(file_name))


class VKUser(VKController):
    def __init__(self, token, user):
        super().__init__(token)
        if not user.isdigit():
            print("Getting user's details...")
            response = self.get_request('users.get', {
                'user_ids': user
            })
            if 'error' in response:
                print("User \"{}\" not found".format(user))
                self.found = False
                return
            self.user_id = response['response'][0]['id']
            self.found = True
        else:
            self.user_id = user

    '''Вы должны взять группы жертвы и его список друзей. После этого у каждого друга спросить его группы. 
       Вычесть группы жертвы из групп друзей. В итоге останутся только уникальные'''

    def get_different_groups(self):
        user_friends = set(self.get_request_response_items('friends.get', {
            'user_ids': self.user_id
        }))
        user_groups = set(self.get_request_response_items('groups.get', {
            'user_id': self.user_id
        }))
        # print(user_friends)
        common_groups = set()
        step = 100 / len(user_friends)
        progress = 0
        print("Getting friends data...")
        for friend in user_friends:
            progress += step
            print("[FRIENDS] Loading: {:2.1%}".format(progress / 100))
            # print('id друга', friend)
            groups_of_friend = set(self.get_request_response_items('groups.get', {
                'user_id': friend
            }))
            # print('группы друга', groups_of_friend)
            common_groups |= groups_of_friend
            # print('группы друзей', friends_groups)
        return user_groups - common_groups

    def get_group_info(self, data):
        group_info_list = []
        step = 100 / len(data)
        progress = 0
        print("Getting groups data...")
        for group in data:
            progress += step
            print("[GROUPS] Loading: {:2.1%}".format(progress / 100))
            group_info = self.get_request('groups.getById', {
                'group_id': group
            })
            if not 'response' in group_info:
                continue
            group_members = self.get_request('groups.getMembers', {
                'group_id': group
            })
            if not 'response' in group_members:
                continue
            group_data = {
                'name': group_info['response'][0]['name'],
                'gid': str(group),
                'members_count': group_members['response']['count'],
            }
            group_info_list.append(group_data)
        return group_info_list


def main():
    user = VKUser(TOKEN_VK, input('Введите id или короткий адрес пользователя VK: '))
    if user.found:
        user.save_to_json('groups', user.get_group_info(user.get_different_groups()))


main()
