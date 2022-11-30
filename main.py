from instagrapi import Client
import os, math, sqlite3 as sl, json
from time import sleep, time
from imageCreate import pil_CreateImage as PCI
f = open('settings.json')
settings = json.load(f)

IG_USERNAME = settings["username"]
IG_PASSWORD = settings["password"]
IG_CREDENTIAL_PATH = './ig_settings.json'
SLEEP_TIME = int(settings["sleep"])
IG_ID = int(settings["id"])
f.close()
cl = Client()
connection = sl.connect('users.db')
cursor = connection.cursor()

def listToString(s: list):
    str1 = ""
    for ele in s:
        str1 = str1 + ele + ' '
    return str1

def cmd(msg):
    print('[] ' + msg)

def init():
    connection.execute("""
        CREATE TABLE IF NOT EXISTS USER (
            id INTEGER PRIMARY KEY ,
            person CHAR(255),
            time CHAR(255),
            answered INTEGER
        );
    """)
    os.system("cls")
    try:
        if os.path.exists(IG_CREDENTIAL_PATH):
            cl.load_settings(IG_CREDENTIAL_PATH)
            cl.login(IG_USERNAME, IG_PASSWORD)
        else:
            cl.login(IG_USERNAME, IG_PASSWORD)
            cl.dump_settings(IG_CREDENTIAL_PATH)
    except:
        cmd('Incorrent login details')
        return None
    menu()

def menu():
    if connection:
        print(f'You logged in as {IG_USERNAME}\n Choose option: \n[1] - Get your account info\n[2] - Get someone\'s profile info\n[3] - Activate Bot')
    option = int(input('> '))
    if option == 1:
        getMyAccInfo()
    elif option == 2:
        getSomeoneAccountInfo()
    elif option == 3:
        activateBot()

def getMyAccInfo():
    print(cl.account_info().dict())

def getSomeoneAccountInfo():
    os.system("cls")
    USERNAME_ACCOUNT = str(input('Write user\'s username\n'))
    UID_ACCOUNT = ''
    try:
        UID_ACCOUNT = cl.user_id_from_username(USERNAME_ACCOUNT)
    except:
        cmd('User not found. Try again')
    os.system("cls")
    print('[1] - Get all media (photos)\n[2] - soon')
    option = int(input('> '))
    if option == 1:
        getAllPhotos(UID_ACCOUNT)
    elif option == 2:
        cmd('soon')

def getAllPhotos(id):
    medias = cl.user_medias(id)
    print(medias)
    raise Exception('Try betterlol')

def activateBot():
    while True:
        inbox1 = cl.direct_threads(20, "flagged", 1)
        inbox2 = cl.direct_pending_inbox(20)
        inboxFormatted1 = getMessages(inbox1)
        inboxFormatted2 = getMessages(inbox2)
        print(inboxFormatted1, inboxFormatted2)
        if inboxFormatted2 == None:
            sendAnswer(inboxFormatted1)
        else:
            inboxFormattedTotal = inboxFormatted1 + inboxFormatted2
            sendAnswer(inboxFormattedTotal)
        sleep(SLEEP_TIME)

def getMessages(inbox):
    try:
        direct = list(inbox[0])
        messages = list(direct[2])[1]
        messagesFormatted = []
        for message in messages:
            msg = list(message)
            # text - 7
            # user id - 1
            # thread id - 2
            MESSAGE_AUTHOR = msg[1][1]
            MESSAGE_THREAD = msg[2][1]
            if MESSAGE_AUTHOR != IG_ID:
                messageArray = []
                satisfied = []
                for text in messages:
                    txt = list(text)
                    if MESSAGE_THREAD == txt[2][1]:
                        if txt[1][1] != IG_ID:
                            messageArray.append(txt[7][1])
                            satisfied.append(txt[2][1])
                inBOX = {
                    "thread": MESSAGE_THREAD,
                    "author": MESSAGE_AUTHOR,
                    "text": messageArray
                }
                messagesFormatted.append(inBOX)
        formattedArrayOfMessages = []
        for messageOne in messagesFormatted:
            if messageOne not in formattedArrayOfMessages:
                formattedArrayOfMessages.append(messageOne)
        # sendAnswer(formattedArrayOfMessages)
        return formattedArrayOfMessages
    except:
        print('Inbox is empty')

def sendAnswer(messages):
    if messages:
        print('118')
        print(messages)
        for message in messages:
            msg_texts = message["text"]
            for msg_text in msg_texts:
                args = msg_text.split()
                if  args[0] == 'love' or args[0] == 'help':
                    personArray = args[1:]
                    person = listToString(personArray)
                    canYouLoveAgain = loveAgain(message["author"], person)
                    print('127')
                    print(canYouLoveAgain)
                    if canYouLoveAgain == True:
                        if args[0] == 'love':
                            cl.direct_answer(message['thread'], f'Отлично! Теперь вы в очереди. Пожалуйста, ожидайте, когда ваше сообщение опубликуются, я вам напишу!')
                            sql_UpdateTime(message["author"])
                            sql_UpdateAnswer(0, message["author"])
                            PCI(person, message["thread"], 20)
                            # cl_newPostFromImage(fileName)
                        elif args[0] == 'help':
                            cl.direct_answer(message['thread'], 'Чтобы анонимно признаться в любви, напишите команду "love <сообщение>"\n Например "love Billie Eilish"')
                    elif canYouLoveAgain == False:
                        cl.direct_answer(message['thread'], 'С момента последнего признания в любви еще не прошло 7 дней.')
                        sql_UpdateAnswer(1, message["author"])
                    sleep(SLEEP_TIME)
            sleep(SLEEP_TIME)

def loveAgain(id, person):
    query = """SELECT * FROM USER"""
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        n = 0
        for record in records:
            if id == record[0]:
                n = n + 1
                timediff = time() - float(record[2])
                if timediff >= 604800:
                    return True
                else:
                    print('154')
                    print(record[3])
                    if record[3] == 1:
                        return None
                    elif record[3] == 0:
                        return False
        if n == 0:
            sql_AddUser(id, person)
            return True
    except sl.Error as error:
        print("186: Failed to perform selection from table", error)
    except:
        return None
    
def sql_UpdateAnswer(integer, id):
    try:
        query = """Update USER set answered = ? where id = ?"""
        values = (integer, id)
        cursor.execute(query, values)
    except sl.Error as error:
        print("196: Failed to update row with Python variable", error)
    connection.commit()

def sql_AddUser(id, person):
    try:
        query = """INSERT INTO USER (id, person, time) VALUES (?, ?, ?)"""
        values = (id, person, str(math.ceil(time())))
        cursor.execute(query, values)
    except sl.Error as error:
        print("205: Failed to insert Python variable into sqlite table", error)
    connection.commit()

def sql_UpdateTime(id): 
    try:
        query = """Update USER set time = ? where id = ?"""
        seconds = time()
        values = (seconds, id)
        cursor.execute(query, values)
    except sl.Error as error:
        print("215: Failed to update row with Python variable", error)
    connection.commit()

# def cl_newPostFromImage(filename: str):
#     cl.photo_upload(f"{filename}.jpg","#анонимноепризнаниевлюбви")

init()