# -*- coding: utf-8 -*-
import socket
import platform
LOGIN_PROVIDER = 1
LOGIN_LOCATION = socket.gethostbyname(socket.gethostname())
LOGIN_DEVICE_NAME = str(
	platform.python_implementation()) + "-" + str(platform.python_version())

BASE_URL = 'https://gd2.line.naver.jp:443'
OBS_URL = 'http://obs-jp.line-apps.com'

WAIT_FOR_MOBILE_PATH = '/Q'


MAIN_PATH = '/api/v4/TalkService.do'
AUTH_PATH = '/api/v4p/rs'

NORMAL_PATH  = '/S4' #/F4
POLLING_PATH = '/P4'
CALL_PATH = '/V4'
CHANNEL_PATH = '/CH4'
BUDDY_PATH   = '/BUDDY4'

TSHOP_PATH   = '/TSHOP4'
SHOP_PATH    = '/SHOP4'

CONN_PATH    = '/LF1'
SQUARE_PATH  = '/SQS1'
LIFF_PATH    = '/LIFF1'
CARRIER     = '51089, 1-0'


LINE_TIMELINE = "1341209850"
LINE_WEBTOON = "1401600689"
LINE_TODAY = "1518712866"
LINE_STORE = "1376922440"
LINE_MUSIC = "1381425814"
LINE_SERVICES = "1459630796'"