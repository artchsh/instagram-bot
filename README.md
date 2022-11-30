# Instagram Love Bot
## Libraries
 - PIL
 - instagrapi
## How to run
1) Check your python version, my python version is 3.11, but i hope it should work fine on versions 3.x
2) Install all the libraries that i used
3) Copy `settings.example.json` and rename it to `settings.json`, and change values to your login credentials
4) Run the first program by cmd `python main.py`
5) Run the second program by cmd `python InstagramPost.py`
## FAQ
#### What `main.py` do?
`main.py` is a main file for a bot. It responds to commands, and creating an image with text
#### What `InstagramPost.py` do?
`InstagramPost.py` is a second instance of bot. It's just publishing the images, that were created by `main.py`, and responding to users that their message has been published.
#### Why you did put sleep almost everywhere?
Because, i dont want to my, or yours, account get banned. Because bots is against the Instagram's policy.
#### Why bot is not responding?
Because, it gets a list of messages every 3-5 minutes. instagrapi does not have events, so i have to figure out a way to respond to a command. You can change it in `settings.json`
#### Why bot has not published my message?
Because, bot takes one image, that was created by main instance of bot, and publishing it once in 15 minutes. You can also change it in `settings.json`
