import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from aiohttp import web

# === ENV ===
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
string_session = os.environ["STRING_SESSION"]

# список друзей
FRIEND_IDS = list(map(int, os.environ.get("FRIEND_IDS", "").split(","))) if os.environ.get("FRIEND_IDS") else []

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

# === TELEGRAM ЛОГИКА ===
async def start_telegram():
    while True:
        try:
            print("🚀 Starting client...")

            client = TelegramClient(
                StringSession(string_session),
                api_id,
                api_hash
            )

            @client.on(events.NewMessage)
            async def handler(event):
                try:
                    if not event.is_private:
                        return

                    sender = await event.get_sender()

                    # проверка по списку
                    if sender.id not in FRIEND_IDS:
                        return

                    text = (event.message.message or "").lower()

                    if "instagram.com" in text or "instagr.am" in text:
                        await asyncio.sleep(0.3)
                        await event.delete()
                        print(f"❌ Удалено сообщение от {sender.id}: {text}")

                except Exception as e:
                    print(f"⚠️ Handler error: {e}")

            await client.start()
            print("🤖 Бот запущен")

            await client.run_until_disconnected()

        except Exception as e:
            print(f"💥 Telegram crashed: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            await asyncio.sleep(5)

# === MAIN ===
async def main():
    print("🟡 Starting services...")

    await web_server()

    asyncio.create_task(start_telegram())

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
