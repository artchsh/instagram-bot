import json, time, os
from instagrapi import Client
from os import walk

f = open('settings.json')
settings = json.load(f)
IG_USERNAME = settings["username"]
IG_PASSWORD = settings["password"]
IG_CREDENTIAL_PATH = './ig_settings.json'
SLEEP_TIME = int(settings["sleepPost"])
IG_ID = int(settings["id"])
f.close()
cl = Client()

def init():
    os.system("cls")
    try:
        if os.path.exists(IG_CREDENTIAL_PATH):
            cl.load_settings(IG_CREDENTIAL_PATH)
            cl.login(IG_USERNAME, IG_PASSWORD)
        else:
            cl.login(IG_USERNAME, IG_PASSWORD)
            cl.dump_settings(IG_CREDENTIAL_PATH)
        print('Logged in as {username}'.format(username = IG_USERNAME))
    except:
        raise Exception('Incorrent login details')

def newPost():
    n = 0
    filesNames = []
    while True:
        mypath = './'
        filenames = next(walk(mypath), (None, None, []))[2]
        for filename in filenames:
            f = 0
            filenameList = filename.split('.')
            isPerson = filenameList[0]
            if isPerson == 'IMG':
                filesNames.append(filename)
                n += 1 
                f += 1
                print(filename)
                time.sleep(SLEEP_TIME)
                try:
                    cl.photo_upload(filename,"#анонимноепризнаниевлюбви")
                    print(f'Posted #{n} photo')
                    os.remove(filename)
                    writeToPerson(filenameList[2])
                except:
                    print('Could not upload a photo')
            if f == 0:
                print('No new photos to publish have found')
                time.sleep(SLEEP_TIME)

def writeToPerson(thread):
    cl.direct_answer(thread, 'Ваше признание в любви было опубликовано!')

if __name__ == '__main__':
    init()
    newPost()