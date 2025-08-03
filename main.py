import asyncio
import re
from telethon import TelegramClient, events

api_id = 22632110
api_hash = '10bbd38e84b3d4f603fe104dcea12029'
target_user = 'Rodi331'

client = TelegramClient('my_new_session2', api_id, api_hash)

def contains_phone_number(text):
    patterns = [
        r'\+?966\d{8,}',
        r'00966\d{8,}',
        r'05\d{7,}',
        r'7\d{7,}',
        r'\d{8,}'
    ]
    return any(re.search(pattern, text) for pattern in patterns)

async def forward_message(message):
    try:
        target = await client.get_entity(target_user)
        await message.forward_to(target)
        print(f"✅ تم تحويل الرسالة إلى {target_user}")
    except Exception as e:
        print(f"❌ خطأ أثناء تحويل الرسالة: {e}")

def check_for_keywords(message):
    text = message.text.strip().lower()

    if contains_phone_number(text):
        print("⏭ تجاهل رسالة تحتوي على رقم جوال")
        return

    keywords = [
        'سكليف', 'ابي سكليف', 'تعرفون حد يعطي سكليف',
        'عذر', 'يحل', 'واجبات', 'بحوث', 'مشروع',
        'مشاريع', 'كويز', 'يساعدني', 'يحل مشروع',
        'يسوي مشاريع', 'تسوي ابحاث', 'تحل', 'ميد',
        'اعذار', 'تسوي', 'خصوصي', 'خصوصية', 'خصوص'
    ]

    for keyword in keywords:
        if keyword in text:
            print(f"📌 تم العثور على كلمة: {keyword}")
            print(f"🔹 الرسالة: {text}")
            client.loop.create_task(forward_message(message))
            break

@client.on(events.NewMessage)
async def handler(event):
    message = event.message
    if message.text:
        check_for_keywords(message)

async def main():
    await client.start()
    print("✅ العميل يعمل... في انتظار الرسائل")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"⚠️ حدث خطأ: {e}")
