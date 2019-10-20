import requests,json,base64,urllib,re,threading,time
Base_url = "https://api.ace-captcha.com/CreateTask"

key = "Ajex"
server = "15282"
userid = "Ajex"

def ACE(base64):
    data = {
    "keyAuthorize":key,
    "body": ""
    }
    data['body'] = base64
    image = requests.post(Base_url,json=data).json()
    if image['errorID'] == 0:
        return image['solvedText']

def post_image(self,data_vote, proxies):
    try:
        vote = requests.post(self.update_psv["submit"],headers=self.update_psv["header"],data=data_vote,proxies=proxies).json()
        return vote
    except:
        return False

def get_image(self,proxies):
    try:
        rid = requests.post(self.update_psv["getimage"], headers=self.update_psv["header"],proxies=proxies).json()
        IMAGE_ID = rid['checksum']
        IMAGECT = requests.get(self.update_psv["u_image"] + IMAGE_ID, headers=self.update_psv["header"],proxies=proxies)
        base64pic = base64.b64encode(IMAGECT.content).decode('utf-8')
        if base64pic.find('iVBORw0KGgoAAAANSUhE') > -1:
            IMAGE = {'id':IMAGE_ID,
            'base64':base64pic}
            return IMAGE
        else:
            return False
    except :
        return False

def loop_vote(self,proxies):
    next_time = None
    dle_time = 0
    while True:
        b = get_image(self,proxies)
        if b:
            solvedText = ACE(b['base64'])
            if next_time:
                get_time = time.time()
                if get_time - dle_time < next_time:
                    tiem_x = int(get_time - dle_time)
                    time.sleep(next_time-tiem_x)
            data_vote = {'server_id':server ,'captcha': solvedText, 'gameid': userid, 'checksum': b['id']}
            c = post_image(self,data_vote,proxies)
            if c:
                next_time = int(c["wait"])
                dle_time = time.time()
                print(c,b['id'],solvedText)
        else:
            break

def autovote(self):
    with open('proxy.txt','r') as fp:
        loop = asyncio.get_event_loop()
        check = []
        px = fp.read().splitlines()
        for x in px:
            if x not in check:
                check.append(x)
                proxies = {'http': ('http://'+x),'https': ('https://'+x), 'ftp': ('ftp://'+x)}
                threading.Thread(target = loop_vote, args = (self,proxies)).start()

def update_psv(self):
    try:
        unpack1 = requests.get(self.update_psv["u_server"]+server)
        unpack2 = re.search(self.update_psv["u_vote"]+'(.+?)"',unpack1.text)
        unpack_unicode = (unpack2.group(1))
        unpack_fn = urllib.parse.quote(unpack_unicode)
        self.update_psv["getimage"] =  ("http://playserver.co/index.php/Vote/ajax_getpic/"+unpack_fn)
        self.update_psv["submit"] = ("http://playserver.co/index.php/Vote/ajax_submitpic/"+unpack_fn)
        self.update_psv["header"] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate",
            "Referer": (self.update_psv["cb_vote"]+unpack_fn)
        }
    except:
        print("check your sever id !!")


class Playserver_test(object):
    def __init__(self):
        self.update_psv = {
            "u_server" : "https://playserver.in.th/index.php/Server/",
            "u_vote" : "https://playserver.in.th/index.php/Vote/prokud/",
            "u_image" : "http://playserver.co/index.php/VoteGetImage/",
            "cb_vote" : "http://playserver.in.th/index.php/Vote/prokud/",
        }
        update_psv(self)
        autovote(self)

Playserver_test()
