import pickle
import itchat
from itchat.content import *
import time
from glob import glob
import os
from guang.Utils.toolsFunc import path
from datetime import datetime
from multiprocessing import Process
from multiprocessing import Pool
import threading
from concurrent.futures import ThreadPoolExecutor
from guang.Utils.symbols import fstring
from guang.Utils.toolsFunc import rm
import mdmail
import psutil

def get_all_info():
    """get all my friends' information """
    nickNames = []

    for friend in itchat.get_friends():
        nickNames.append(friend.NickName)
        # print(nickNames)
    return nickNames


def get_userName(*name_list):
    UserNames = {}
    for name in name_list:
        friends = itchat.search_friends(name=name)

        if len(friends) == 1:
            UserNames[name] = friends[0].UserName
        else:
            print(f'name: “{name}” is NOT unique')
            raise Exception('')
    return UserNames


def save_userName():
    name_list = ['爸爸', '妈妈',
                 '被冻结的光', 'caloi']
    userNames = get_userName(*name_list)
    with open('userNames.pkl', 'wb') as fo:
        pickle.dump(userNames, fo)


def load_userName():
    with open('userNames.pkl', 'rb') as fi:
        userNames = pickle.load(fi)


def get_list(lis=[''], count=[0]):
    '''get msg list and count'''

    @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO])
    def reply(msg):
        lis[0] = msg
        count[0] = count[0] + 1
        return

    return lis[0], count[0]


count_n = 0
def get_content(l, count):
    global count_n
    if count == count_n:
        count_n += 1
        return l
    else:
        return False


def get_msg():
    #     global = count_n
    l, count = get_list()
    message = get_content(l, count)
    if message:
        return message
    else:
        return None


def dynamic_msg():
    '''Dynamic acquisition of anyone's message
    Once acquired, the program releases'''
    while 1:
        msg = get_msg()
        if msg == None:
            time.sleep(.6)
            itchat.configured_reply()
            continue
        else:
            return msg


def dynamic_specified_msg(userName=None):
    '''
    Dynamic acquisition of specified user's message
    Once acquired, the program releases
    '''
    while 1:
        msg = get_msg()
        try:
            msg_userName = msg.user.userName
        except:
            msg_userName = None

        if msg_userName == None or msg_userName != userName:
            time.sleep(.6)
            itchat.configured_reply()
            continue
        else:
            return msg


flag_get_txt = True
MY_USER_NAME = None
def _txt(msg, MyName="被冻结的光"):
    global flag_get_txt, MY_USER_NAME
    if flag_get_txt:
        MY_USER_NAME = get_userName(MyName)[MyName]
        # print(MY_USER_NAME)
        flag_get_txt = False
    tpath = os.path.join('wechat_download', msg.User.NickName, 'text')
    if not os.path.exists(tpath):
        os.makedirs(tpath)
    nowTime = datetime.now()
    nowTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
    out_text = fstring(msg.text, 100, '<', flag='en')
    if msg['FromUserName'] != MY_USER_NAME:
        out_name = fstring(msg.User.NickName, 10, '<')
    else:
        out_name = fstring(MyName, 10, '<')
    text = f"{out_name}   :{out_text}{nowTime: >10}\n"
    with open(path(tpath + '/dialogue.txt'), 'a+', encoding='utf-8') as fw:
        fw.write(text)
    return msg

def write_txt(name_list, MyName="被冻结的光", fileDir="itchat.pkl", cmdQR=False):
    """name_list such as ['filehelper', 'caloi']"""
    lock = threading.Lock()
    def relogin(fileDir):
        # global lock
        sleepTime = 1200
        while (True):
            lock.acquire()
            print("lock acquire")
            if os.path.exists(fileDir) and time.time() - os.path.getatime(fileDir) > 2*sleepTime:
                rm(fileDir)
            print("................loading....................")
            if itchat.load_login_status(fileDir):
                pass
            else:
                if cmdQR:
                    itchat.login(enableCmdQR=2)
                else:
                    picDir = 'QR.png'
                    itchat.login(picDir=picDir)
                    # to modified: miniconda3/lib/python3.7/site-packages/itchat/utils.py
            itchat.dump_login_status(fileDir=fileDir)
            print("................load success ................")
            print("lock release")
            lock.release()
            time.sleep(sleepTime)

            pid = os.getpid()
            p = psutil.Process(pid)
            p.kill()


    def run(nickName):
        # global lock
        print(nickName, ":start")
        @itchat.msg_register([TEXT])
        def write2file(msg):
            userName = get_userName(nickName)[nickName]
            if msg.user.userName == userName:
                _txt(msg,MyName)
        lock.acquire()
        # itchat.auto_login(hotReload=True, statusStorageDir=fileDir, enableCmdQR=2)
        itchat.run(debug=True)

    try:
        #  ----------------------------------------------------------------------
        # t0 = threading.Thread(target=relogin, args=(fileDir))
        # t = [threading.Thread(target=run, args=(name,)) for name in name_list]
        # t0.start()
        # [i.start() for i in t]

        # ----------------------------------------------------------------------
        # with Pool(len(name_list)) as pool:  # process pool
        #     pool.map(run, name_list)
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # Thread pools without locks can result in multiple writes
        with ThreadPoolExecutor(max_workers=len(name_list) + 5) as executor:
            res0 = executor.submit(relogin, fileDir)
            res = [executor.submit(run, name) for name in name_list]

    except:
        print("try is not successful !")

def download_file(msg, fileType='mp3'):
    '''
    Param
    -----
        fileType : 'attachment' ,'mp3', 'mp4', 'png'
        and ATTACHMENT,  of which include various file types.
    Returns
    -------
        msg, file_path
    '''
    #     msg = dynamic_specified_msg(username)
    file_name = msg.fileName.split('.')
    sufname = file_name[-1]
    prename = '.'.join(file_name[:-1])

    if fileType == 'attachment':  # 'attachment':
        tpath = os.path.join('wechat_download', msg.User.NickName, 'attachment')
        if not os.path.exists(tpath):
            os.makedirs(tpath)
        msg.download(os.path.join(tpath, msg.fileName))
    elif sufname == 'png' and fileType == 'png':
        tpath = os.path.join('wechat_download', msg.User.NickName, 'picture')
        if not os.path.exists(tpath):
            os.makedirs(tpath)
        msg.download(os.path.join(tpath, msg.fileName))
    elif sufname == 'mp3' and fileType == 'mp3':
        tpath = os.path.join('wechat_download', msg.User.NickName, 'voice')
        if not os.path.exists(tpath):
            os.makedirs(tpath)
        msg.download(os.path.join(tpath, msg.fileName))
    elif sufname == 'mp4' and fileType == 'mp4':
        tpath = os.path.join('wechat_download', msg.User.NickName, 'video')
        if not os.path.exists(tpath):
            os.makedirs(tpath)
        msg.download(os.path.join(tpath, msg.fileName))

    #     os.remove(msg.fileName) # remove 当前文件夹下的下载文件
    return msg, tpath


def d_time(d_t, t0=[]):
    """
    The unit of dt is seconds.
    Returns 1 when current time in `d_t` duration
    Returns 0 when current time out duration
    """
    if not t0:
        t0.append(time.time())
    t1 = time.time()
    if t1 - t0[0] < d_t:
        return True
    else:
        return False



if __name__ == '__main__':
    statusDir = "itchat.pkl"
    name_list = ['妈妈','caloi']
    while True:
        t_i = Process(target=write_txt, args=(name_list, "被冻结的光", statusDir, False) )
        t_i.start()
        t_i.join()



    # itchat.auto_login(hotReload=True)
    # while d_time(60):
    #     msg = dynamic_specified_msg(get_userName('光')['光'])
    #     msg = download_file(msg, fileType='mp3')


