import datetime, time, random, hashlib, requests, hmac, urllib, json, pytz, sys, os

def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

def gen_date():
    return [datetime.datetime.now(pytz.timezone('Asia/Hong_Kong')).strftime("%d-%m-%Y"), datetime.datetime.now(pytz.timezone('Asia/Hong_Kong')).strftime("%H:%M:%S")]

def save_file(data,file,opt="w"):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, opt) as f:
        f.write(data)

def file_get_contents(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        f = open(filename, "r")
        return f.read()
    except FileNotFoundError:
        f = open(filename, "w")
        f.write("")
        return ""
    
def parse_cookie(cookie):
    cookies = {}
    dat = cookie.split(";")
    for i in range(int(len(dat))-1):
        data = dat[i].split('=')
        cookies.update({data[0]:data[1]})
    return cookies

def generate_useragent(sign_version = '107.0.0.27.121'):
    resolusi = ['1080x1776','1080x1920','720x1280','320x480','480x800','1024x768','1280x720','768x1024','480x320']
    versi = ['GT-N7000','SM-N9000','GT-I9220','GT-I9100']
    dpi = ['120','160','320','240']
    return 'Instagram ' + sign_version + ' Android (' + str(random.randint(10, 11)) + '/' + str(random.randint(1, 3)) + '+' + str(random.randint(3, 5)) + '.' + str(random.randint(0, 5)) + '; ' + str(random.choice(dpi)) + '; ' + str(random.choice(resolusi)) + '; Samsung; ' + str(random.choice(versi)) + '; ' + str(random.choice(versi)) + '; smdkc210; en_US)'

def generate_device_id():
    return 'android-' + hashlib.md5(str(random.randint(1000, 9999)).encode()).hexdigest() + str(random.randint(2, 9))

def generate_guid(tipe = 0):
    guid = "%04x%04x-%04x-%04x-%04x-%04x%04x%04x" % (random.randint(0, 65535),random.randint(0, 65535),random.randint(0, 65535),random.randint(16384, 20479),random.randint(32768, 49151),random.randint(0, 65535),random.randint(0, 65535),random.randint(0, 65535))
    if tipe:
        return guid
    else:
        return guid.replace('-','')

def hook(data):
    sign = hmac.new(b'5d406b6939d4fb10d3edb4ac0247d495b697543d3f53195deb269ec016a67911', data.encode(), hashlib.sha256).hexdigest()
    return 'ig_sig_key_version=4&signed_body=' + sign + '.' + urllib.parse.quote_plus(data)

def post_request(ver, ighost, useragent, url, cookie = False, data = 0, httpheader = {}):
    ses = requests.Session()
    if useragent:
        ses.headers["User-Agent"] = useragent
    if ighost:
        url = 'https://i.instagram.com/api/v'+str(ver)+'/' + url
    if cookie:
        cookies = parse_cookie(cookie)
        r = ses.post(url,data=data,headers=httpheader,cookies=cookies)
    else:
        r = ses.post(url,data=data,headers=httpheader)
    return r

def get_request(ighost, useragent, url, cookie = False, data = 0, httpheader = {}):
    ses = requests.Session()
    if useragent:
        ses.headers["User-Agent"] = useragent
    if ighost:
        url = 'https://i.instagram.com/api/v1/' + url
    if cookie:
        cookies = parse_cookie(cookie)
        r = ses.get(url,headers=httpheader,cookies=cookies)
    else:
        r = ses.get(url,headers=httpheader)
    return r