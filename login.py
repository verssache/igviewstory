from library import config

print("[+] Instagram View Story - By: GidhanB.A\n")

userig = input("[+] Input your instagram username: ")
passig = config.igfunc.getpass.getpass("[+] Input your instagram password: ")

useragent = config.igfunc.generate_useragent()
device_id = config.igfunc.generate_device_id()

login = config.igfunc.post_request(1,1,useragent,'accounts/login/',0,config.igfunc.hook('{"device_id":"' + device_id + '","guid":"' + config.igfunc.generate_guid() + '","username":"' + userig + '","password":"' + passig + '","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}'),{
    "Accept-Language": "id-ID, en-US",
    "X-IG-Connection-Type": "WIFI",
    "Content-Type": "application/x-www-form-urlencoded"
})

cookie = ""
for c in login.cookies:
    cookie += c.name+'='+c.value+';'

res = config.igfunc.json.loads(login.text)
if res["status"] == "ok":
    print("[+] Login succesfuly!")
    config.igfunc.save_file(cookie+"|"+useragent,"data/"+config.cookieFile)
elif res["error_type"] == "checkpoint_challenge_required":
    print("[+] Challenge Required")
elif res["error_type"] == "bad_password":
    print("[+] Invalid password!")
else:
    print("[+] Unknown error: "+res["message"])
