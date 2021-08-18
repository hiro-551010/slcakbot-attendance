import os
import yaml


# with open(os.path.join('secrets', 'secret.yaml')) as file:
#     objs = yaml.safe_load(file)
#     for obj in objs:
#         os.environ[obj] = objs[obj]


#     API_TOKEN = os.environ['API_TOKEN']

#     DEFAULT_REPLY = "こんにちは、こちらは勤怠管理botです。"


# herokuのAPI_TOKENの設定
API_TOKEN = os.environ['API_TOKEN']
