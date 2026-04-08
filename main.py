import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from aiohttp import web

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
string_session = os.environ["STRING_SESSION"]

# список друзей
FRIEND_IDS = list(map(int, os.environ.get("FRIEND_IDS", "").split(",")))

# === HTTP сервер ===
async def handle(request):
    return web.Response(text="OK", content_type="text/plain")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(
        runner,
        "0.0.0.0",
        int(os.environ.get("PORT", 8080))
    )
    await site.start()
    print("🌐 Web server started")


async def main():
    client = TelegramClient(StringSession(string_session), api_id, api_hash)

    @client.on(events.NewMessage)
    async def handler(event):
        try:
            if not event.is_private:
                return

            sender = await event.get_sender()

            # фильтр по списку друзей
            if sender.id not in FRIEND_IDS:
                return

            text = (event.message.message or "").lower()

            # фильтр instagram
            if "instagram.com" in text or "instagr.am" in text:
                await asyncio.sleep(0.3)
                await event.delete()
                print(f"❌ Удалено сообщение от {sender.id}: {text}")

        except Exception as e:
            print(f"⚠️ Ошибка: {e}")

    print("🚀 Starting client...")
    await client.start()
    print("🤖 Бот запущен")

    asyncio.create_task(web_server())

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
