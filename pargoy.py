import requests
from pyrogram import Client, filters
from pyrogram.types import Message
import os
import pytz
from datetime import datetime


TOKEN=os.getenv("BOT_TOKEN", "5227572964:AAEFEL-skbXFvk0ZA2KPABXkt-ultuyrfWU")
session=os.getenv("SESSION", "BQAWid4NCnYwiVzujBWyprekfDI7yYJkAFfYeJj4kyrtt-OulSKynvtRs2ixL3Wn5quCK26glAcYxSi1l6GDFA1KZ1aaws0uadDM_Zv31JsbOudwS_cGazFvVjg7cE0xAPF8dRc3PrAIezHDIenPnCRKdvOX2SV3JqmfW8K9rkcPppogl_je6RmEDXvgdRw0G1d8qqr3RWZZtqrTarptcTTGBNe-7KZ8V-F6_vN0y0hYFynhitxU9gemZvYArweBF_3qHrXaDHeOh0QwBHYWK6DBUy_csgQCkpWuoqZlu6Wrgk8CSe1O-MwJ52DrqeJycVCZjZp294Yv1topnEnzg3hYAAAAAS2H7nMA")api_id = int(os.getenv("API_ID"))
api_id = int(os.getenv("API_ID", "19253868"))
api_hash = os.getenv("API_HASH", "8a4c72f378085050d667f5f3cb400576")
log_channel=os.getenv("LOG_CHANNEL", "-1001186371688")
myuserid=os.getenv("OWNER_UNAME", "@BLVCKCARDS")

BOT_url='https://api.telegram.org/bot'+TOKEN
app=Client(session, api_id, api_hash)


def utc_to_time(naive, timezone="Asia/Jakarta"):
    dt_object = datetime.fromtimestamp(naive)
    return dt_object.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))

async def dirup(message,pat,tgapi,otherr):
	pat=pat[:-1]
	tes =tgapi+'?caption='+otherr+ str(message.chat.username)+"\n**to** : "+str(message.chat.first_name) +"\n"+str(message.caption)+"\n"+str(utc_to_time(message.date))
	arr = os.listdir(pat)
	for files in arr:
		pathh=pat+"/"+str(files)
		file_size=os.stat(pathh).st_size
		if file_size<52428800 :
			botSend(pathh,tes,pat)
			os.remove(pathh)
		else:
			print('file size is too big')
			await message.forward(log_channel)

def botSend(fileName, tes ,pat):
    files = {pat: (fileName, open(fileName,'rb'))}  
    r = requests.post(BOT_url+tes+'&chat_id='+str(log_channel), files=files)
    print(r)



@app.on_message(filters.text & filters.private & ~filters.bot)
async def msg_text(client: Client, message: Message):
	print('text recived')
	if message.from_user.username == myuserid:
		tes ="From @"+myuserid+" to @"+ str(message.chat.username)+" "+str(message.chat.first_name) +"\n"+str(message.text)+"\n"+str(utc_to_time(message.date))
	else:
		tes ="@"+ str(message.from_user.username)+" "+str(message.chat.first_name) +"\n"+str(message.text)+"\n"+str(utc_to_time(message.date))
	g=requests.post(BOT_url+'/sendmessage' , json={"chat_id":log_channel,"text":tes})
	print(tes)
	print(g)

@app.on_message(filters.photo & filters.private & ~filters.bot)
async def msg_photo(client: Client, message: Message):
	print('photo recived')
	pat='photo/'
	tgapi='/sendPhoto'
	if message.from_user.username  == myuserid:
		otherr='From @'+myuserid+' to @'
	else:
		otherr=''
	await app.download_media(message,file_name=pat)
	await dirup(message,pat,tgapi,otherr)

@app.on_message(filters.video & filters.private & ~filters.bot)
async def msg_video(client: Client, message: Message):
	print('video recived')
	pat='video/'
	tgapi='/sendVideo'
	if message.video.file_size>50428800:
		await message.forward(log_channel)
	else:
		if message.from_user.username  == myuserid:
			otherr='From @'+myuserid+' to @'
		else:
			otherr=''
		await app.download_media(message,file_name=pat)
		await dirup(message,pat,tgapi,otherr)

@app.on_message(filters.audio & filters.private & ~filters.bot)
async def msg_audio(client: Client, message: Message):
	print('audio recived')
	pat='audio/'
	tgapi='/sendAudio'
	if message.from_user.username  == myuserid:
		otherr='From @'+myuserid+' to @'
	else:
		otherr=''
	await app.download_media(message,file_name=pat)
	await dirup(message,pat,tgapi,otherr)

@app.on_message(filters.media & filters.private & ~filters.bot & ~filters.photo & ~filters.video & ~filters.audio & ~filters.poll)
async def msg_document(client: Client, message: Message):
	print('document recived')
	pat='document/'
	tgapi='/sendDocument'
	if message.document.file_size>50428800:
		await message.forward(log_channel)
	else:
		if message.from_user.username  == myuserid:
			otherr='From @'+myuserid+' to @'
		else:
			otherr=''
		await app.download_media(message,file_name=pat)
		await dirup(message,pat,tgapi,otherr)


print('bot started\nBy @charindith')
app.run()
