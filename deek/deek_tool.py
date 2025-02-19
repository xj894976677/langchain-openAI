import json
import requests
from typing import Optional, List

class DeekAPI:
    """ Deek API 实现"""
    def __init__(self):
        pass
        
    def getDeekTweets(self, username: str) -> str:
        """
            获取指定用户在deek平台的最新100条推文。按照发布时间倒序排列
            :param username: 用户名
            :return: 以json的形式返回当前用户的100条推文内容
            """
        try:
            url = 'https://api.deek.network/v1/feed/wish/timeline'
            params = {
                'nextToken': '',
                'limit': 10,
                'customerId': username,
                'role': 'MAKER'
            }
            # 请求头
            headers = {
                'jwt_token': '',
                'chain_id': '80084',
                'saas_id': 'zeek',
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Accept': '*/*',
                'Host': 'api.deek.network',
                'Connection': 'keep-alive'
            }

            # 发送 GET 请求
            response = requests.get(url, headers=headers, params=params)

            # 获取第一部分数据
            json_object = json.loads(response.text)
            tweets = json_object['obj']['rows']
            
            # 收集所有 bizId
            biz_ids = [tweet['bizId'] for tweet in tweets]
            print(biz_ids)
            # 获取详细内容
            tweets_content = self.getDeekTweetContent(biz_ids)

            if (tweets_content == None):
                print("接口失败，返回默认数据")
                return [{"title": "web3行业趋势"},{"title": "deek上市"},{"title": "2025 双鱼座运势"},{"title": "今年购买什么虚拟货币能赚钱"},{"title": "论母猪养殖与郁金香繁育"}]
            # 提取指定字段
            if tweets_content and 'data' in tweets_content and 'rows' in tweets_content['data']:
                formatted_content = []

                for item in tweets_content['data']['rows']:
                    formatted_item = {
                        'title': item.get('title', ''),
                        'summary': item.get('summary', ''),
                        'created': item.get('created', ''),
                        'content': item.get('content', '')
                    }
                    formatted_content.append(formatted_item)
                print("formatted_content", formatted_content)
                return formatted_content
            return []
        except Exception as e:
            print(f"获取推文时出错: {e}")
            return json.dumps(["hello every ony,are you ok?", "how are you", "hahahhahaha", "wow it is nice" , "i like this"])


    def getDeekFollowers(self, username: str) -> str:
        """
            获取指定用户在deek平台上的关注用户信息
            :param username: 用户名
            :return: 以数组的形式返回关注用户的id
            """
        try:
            import requests

            # 请求 URL 和参数
            url = 'https://api.opensocial.fun/v2/relations/profiles/0x488a/followers'
            params = {
                'with_reverse': 'true',
                'with_profile': 'true',
                'limit': 20,
                'ranking': 'CREATED'
            }

            # 请求头
            headers = {
                'sec-ch-ua-platform': '"macOS"',
                'authorization': '',
                'Referer': 'https://m.deek.network/',
                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'OS-Guest-Id-Marketing': '3141597425322673',
                'OS-App-Id': '94811268837278228',
                'OS-Chain-Id': '80084',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'a': '[object Object]'
            }

            # 发送 GET 请求
            response = requests.get(url, headers=headers, params=params)
            # 打印响应内容
            json_object = json.loads(response.text)
            print([item['handle'] for item in json_object['data']['rows']])
            return self.getDeekFollowersByCustomerId([item['handle'] for item in json_object['data']['rows']])
        except Exception as e:
            print(f"获取关注用户时出错: {e}")
            return


    def getDeekTweetContent(self, bizIds: List[str]) -> dict:
        # 构建请求 URL 和参数
        base_url = "https://api.opensocial.fun/v2/feed/batch/ids"
        params = {
            'limit': 10,
            'next_token': '',
            'enrich.enable': 'true',
            'enrich.with_reaction_counts': 'true',
            'enrich.with_own_reaction_kinds': 'VOTE',
            'enrich.reaction_limit': 1,
            'enrich.children_limit': 1,
            'enrich.with_profile': 'true',
            'enrich.with_community': 'true',
            'enrich.with_profile_joining_role': 'false'
        }
        
        # 添加多个 ids 参数
        # 将所有 bizIds 放入数组中
        params['ids'] = bizIds
        print("bizIds", bizIds)
        # 构建请求头
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'authorization': '',
            'cache-control': 'no-cache',
            'origin': 'https://m.deek.network',
            'os-app-id': '94811268837278228',
            'os-chain-id': '80084',
            'os-guest-id-marketing': '3141597425322673',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://m.deek.network/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        }
        
        try:
            # 发送 GET 请求
            response = requests.get(base_url, headers=headers, params=params)
            
            # 解析响应
            if response.status_code == 200:
                return response.json()
            else:
                print(f"请求失败，状态码: {response.status_code}")
                print(response)
                return None
        except Exception as e:
            print(f"获取推文内容时出错: {e}")
            return None


    def getDeekFollowersByCustomerId(self, customerIds: List[str]) -> List[str]:
        # 请求 URL
        url = 'https://api.deek.network/v1/profile'

        # 请求头
        headers = {
            'sec-ch-ua-platform': '"macOS"',
            'Referer': 'https://m.deek.network/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'jwt_token': '',
            'chain_id': '80084',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'saas_id': 'zeek',
            'Content-Type': 'application/json'
        }

        # 请求体数据
        data = {
            "idList": customerIds,
            "badgeStrategy": "HNWI",
            "needBadgeInfo": True,
            "needOpenSocialInfo": False
        }

        # 发送 POST 请求
        response = requests.post(url, headers=headers, json=data)

        # 打印响应内容
        print([item['basic']['customerId'] for item in response.json()['obj']['rows']])
        return [item['basic']['customerId'] for item in response.json()['obj']['rows']]