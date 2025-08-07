from flask import Flask, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import time

API_ID = 17570480
API_HASH = "18c5be05094b146ef29b0cb6f6601f1f"
STRING_SESSION = "1ApWapzMBu2IsjkbDrAa9bmN1jD0n8u56EL8siRToF3NFPO8OG9YELR4zqsZ8LtyYeGNE-aLYrkBjPV95S2J_9hsVg0NAUa0kCPVgNS_wMN_BzZSqocO2QYiE-4YR1euEuX-VuPysvrL8Gg5lcs373YbAOES8vDJy9iwmVNFXLY0SH5AvichPuaotRrLLHns9OYrd5qC_UpR81xyOa1iMU-QpF3q2Nu1NCRZYPjI_JPDhCdwAlXm1e7LRLpeQtdHR86uFUYmoaj9x4ERXYECA6RZZ_Uk82yvCF_FX8Jf_DZCPkDYSDw-N9H13ufSugiQoO-cAyVu5op_nQ5eE3ZojbTdL3NfrtL4="

app = Flask(__name__)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@app.route("/nabiapi/<komut>/<tc>")
def sorgu_yap(komut, tc):
    sonuc = loop.run_until_complete(sorgu_gonder(komut, tc))
    return jsonify(sonuc)

async def sorgu_gonder(komut, tc):
    mesajlar = []

    async with TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH) as client:
        try:
            sahmaran = await client.get_entity("SahmaranBot")

            messages = await client.get_messages(sahmaran, limit=1)
            last_message_id = messages[0].id if messages else 0

            await client.send_message(sahmaran, f"/{komut} {tc}")
            await asyncio.sleep(2)

            baslangic = time.time()
            while time.time() - baslangic < 20:
                new_messages = await client.get_messages(sahmaran, limit=10, min_id=last_message_id)
                for msg in new_messages:
                    if msg.text and tc in msg.text and msg.text not in mesajlar:
                        mesajlar.append(msg.text)
                        last_message_id = max(last_message_id, msg.id)
                await asyncio.sleep(2)

            return {
                "komut": komut,
                "tc": tc,
                "kayit_sayisi": len(mesajlar),
                "sonuclar": mesajlar
            }

        except Exception as e:
            return {"hata": str(e)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
