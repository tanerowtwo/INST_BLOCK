import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = 123456
api_hash = "your_api_hash"
session = "YOUR_STRING_SESSION"

FRIEND_ID = 123456789

client = TelegramClient(StringSession(session), api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    
    # только сообщения от друга
    if sender.id != FRIEND_ID:
        return
    
    text = (event.message.message or "").lower()
    
    if "instagram.com" in text or "instagr.am" in text:
        await event.delete()
        print("Удалено сообщение с Instagram")

async def main():
    await client.start()
    print("Бот работает...")
    await client.run_until_disconnected()

asyncio.run(main())