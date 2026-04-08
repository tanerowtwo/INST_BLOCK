import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from aiohttp import web

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
string_session = os.environ["STRING_SESSION"]

FRIEND_ID = int(os.environ["FRIEND_ID"])

client = TelegramClient(StringSession(string_session), api_id, api_hash)

# === УДАЛЕНИЕ СООБЩЕНИЙ В ЛС ===
@client.on(events.NewMessage)
async def handler(event):
    try:
        if not event.is_private:
            return

        sender = await event.get_sender()

        if sender.id != FRIEND_ID:
            return

        text = (event.message.message or "").lower()

        if "instagram.com" in text or "instagr.am" in text:
            await event.delete()
            print("❌ Удалено сообщение с Instagram")

    except Exception as e:
        print(f"⚠️ Ошибка: {e}")


# === HTTP сервер Render ===
async def handle(request):
    return web.Response(text="OK", content_type="text/plain")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8080)))
    await site.start()
    print("🌐 Web server started")


# === Heartbeat ===
async def heartbeat():
    while True:
        try:
            me = await client.get_me()
            print(f"💓 Heartbeat OK — {me.username}")
        except Exception as e:
            print(f"💔 Heartbeat failed: {e}")
        await asyncio.sleep(120)


# === MAIN ===
async def main():
    await client.start()
    print("🤖 Бот запущен (удаление Instagram ссылок)...")

    asyncio.create_task(web_server())
    asyncio.create_task(heartbeat())

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
