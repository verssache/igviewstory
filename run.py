from library import config

cookieData = config.igfunc.file_get_contents("data/"+config.cookieFile).split("|")
cookie, useragent = cookieData[0], cookieData[1]
loop = True

print("[+] Instagram View Story - By: GidhanB.A\n")
if cookie:
    getakun = config.igfunc.json.loads(config.igfunc.get_request(1,useragent,'accounts/current_user/',cookie).text)
    if getakun["status"] == "ok":
        getakunV2 = config.igfunc.json.loads(config.igfunc.get_request(1,useragent,'users/'+str(getakun["user"]["pk"])+'/info',cookie).text)
        print("[+] Login as @{}".format(getakun["user"]["username"]))
        print("[+] [Media : {}] [Followers : {}] [Following : {}]".format(str(getakunV2["user"]["media_count"]),str(getakunV2["user"]["follower_count"]),str(getakunV2["user"]["following_count"])))
        while loop:
                targets = config.igfunc.file_get_contents("data/"+config.targetFile).replace("\r","").split("\n")
                for target in targets:
                    try:
                        todays = config.igfunc.file_get_contents("data/daily/"+config.igfunc.gen_date()[0]+".txt").replace("\r","").split("\n")
                        print("\n[+] Get followers of @{}".format(target))
                        targetid = config.igfunc.json.loads(config.igfunc.get_request(1,useragent,'users/'+target+'/usernameinfo',cookie).text)["user"]["pk"]
                        gettarget = config.igfunc.json.loads(config.igfunc.get_request(1,useragent,'users/'+str(targetid)+'/info',cookie).text)
                        print("[+] [Media : {}] [Followers : {}] [Following : {}]".format(gettarget['user']['media_count'], gettarget['user']['follower_count'], gettarget['user']['following_count']))
                        jumlah = config.countTarget
                        if not jumlah.isnumeric():
                            limit = 1
                        elif int(jumlah) > gettarget["user"]["follower_count"] - 1:
                            limit = gettarget['user']['follower_count'] - 1
                        else:
                            limit = int(jumlah) - 1
                        gas = False
                        gas_id = 0
                        listid = []
                        while True:
                            if gas == True:
                                parameters = '?max_id='+str(gas_id)+''
                            else:
                                parameters = ''
                            req = config.igfunc.json.loads(config.igfunc.get_request(1,useragent,'friendships/'+str(targetid)+'/followers/'+parameters,cookie).text)
                            if req["status"] != "ok":
                                print(config.igfunc.json.dumps(req, indent=4, sort_keys=True))
                            for i in range(len(req["users"])):
                                if req["users"][i]["is_private"] == False and req["users"][i]["latest_reel_media"] and len(listid) <= limit:
                                    listid.append(req["users"][i]["pk"])
                            if req["next_max_id"]:
                                gas = True
                                gas_id = req["next_max_id"]
                            else:
                                gas = False
                                gas_id = 0
                            if len(listid) >= limit:
                                break
                        print("[+] Total {} followers of @{} collected\n".format(len(listid),target))
                        reels = []
                        reels_suc = []
                        for i in range(len(listid)):
                            getstory = config.igfunc.json.loads(config.igfunc.get_request(1,useragent,'feed/user/'+str(listid[i])+'/story/',cookie).text)
                            for storyitem in getstory["reel"]["items"]:
                                sleep_1 = config.igfunc.random.randint(1,10) # Jeda per view story
                                sleep_2 = config.igfunc.random.randint(15,45) # Jeda per view story 1 akun user
                                reels.append(storyitem["id"]+"_"+str(getstory["reel"]["user"]["pk"]))
                                stories = {}
                                stories.update({"id":storyitem["id"]})
                                stories.update({"reels":storyitem["id"]+"_"+str(getstory["reel"]["user"]["pk"])})
                                tstamp = int(config.igfunc.datetime.datetime.timestamp(config.igfunc.datetime.datetime.now().replace(microsecond=0)))
                                stories.update({"reel":str(storyitem["taken_at"])+"_"+str(tstamp)})
                                if stories["reels"] not in config.igfunc.file_get_contents("data/storyData.txt"):
                                    hook = '{"live_vods_skipped": {}, "nuxes_skipped": {}, "nuxes": {}, "reels": {"'+stories['reels']+'": ["'+stories['reel']+'"]}, "live_vods": {}, "reel_media_skipped": {}}'
                                    viewstory = config.igfunc.json.loads(config.igfunc.post_request(2,1,useragent,'media/seen/?reel=1&live_vod=0',cookie, config.igfunc.hook(''+hook+'')).text)
                                    if viewstory["status"] == "ok":
                                        reels_suc.append(str(storyitem["id"])+"_"+str(getstory["reel"]["user"]["pk"]))
                                        print("[~] ["+config.igfunc.gen_date()[1]+"] - Seen stories "+stories["id"])
                                        config.igfunc.save_file(stories["reels"]+"\n","data/storyData.txt","a")                              
                                        config.igfunc.save_file(stories["reels"]+"\n","data/daily/"+config.igfunc.gen_date()[0]+".txt","a")
                                    config.igfunc.time.sleep(sleep_1)
                            for i in config.igfunc.progressbar(range(sleep_2), "[!] ["+config.igfunc.gen_date()[1]+"] - Sleep for "+str(sleep_2)+" seconds: ", 30):
                                config.igfunc.time.sleep(1)
                    except:
                        print("[!] ["+config.igfunc.gen_date()[1]+"] - Story not found!")
                    print("[+] "+str(len(reels))+" story from "+target+" collected")
                    print("[+] "+str(len(reels_suc))+" story from "+target+" marked as seen")
                    for i in config.igfunc.progressbar(range(30), "[!] ["+config.igfunc.gen_date()[1]+"] - Sleep for 30 seconds: ", 30):
                        config.igfunc.time.sleep(1)
                    if len(todays) >= 2000:
                        print("[!] Limit Instagram API 2000 seen/day")
                        for i in config.igfunc.progressbar(range(72000), "[!] ["+config.igfunc.gen_date()[1]+"] - Sleep for 20 hours: ", 30):
                            config.igfunc.time.sleep(1)
                        print("[!] End sleep..\n")
    else:
        print("[!] Error: "+config.igfunc.json.dumps(getakun, indent=4, sort_keys=True))
else:
    print("[+] Please login first!")