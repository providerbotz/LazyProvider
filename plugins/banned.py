from pyrogram import Client, filters
from utils import temp
from pyrogram.types import Message
from database.users_chats_db import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import SUPPORT_CHAT


async def banned_users(_, client, message: Message):
    return (
        message.from_user is not None or not message.sender_chat
    ) and message.from_user.id in temp.BANNED_USERS


banned_user = filters.create(banned_users)


async def disabled_chat(_, client, message: Message):
    return message.chat.id in temp.BANNED_CHATS


disabled_group = filters.create(disabled_chat)


@Client.on_message(filters.private & banned_user & filters.incoming)
async def ban_reply(bot, message):
    ban = await db.get_ban_status(message.from_user.id)
    await message.reply(
        "🚫 **ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ**\n\n"
        "⚠️ sᴏʀʀʏ, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ.\n\n"
        f"📝 **ʀᴇᴀsᴏɴ:** `{ban['ban_reason']}`\n\n"
        "💡 ɪꜰ ʏᴏᴜ ᴛʜɪɴᴋ ᴛʜɪs ɪs ᴀ ᴍɪsᴛᴀᴋᴇ, ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ."
    )


@Client.on_message(filters.group & disabled_group & filters.incoming)
async def grp_bd(bot, message):
    buttons = [[
        InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=f"https://telegram.me/{SUPPORT_CHAT}")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)

    vazha = await db.get_chat(message.chat.id)

    k = await message.reply(
        text=(
            "🚫 **ᴄʜᴀᴛ ʀᴇsᴛʀɪᴄᴛᴇᴅ**\n\n"
            "⚠️ ᴛʜɪs ɢʀᴏᴜᴘ ɪs ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ.\n"
            "👮‍♂️ ᴀᴅᴍɪɴs ʜᴀᴠᴇ ʀᴇsᴛʀɪᴄᴛᴇᴅ ᴍʏ ᴀᴄᴄᴇss ʜᴇʀᴇ.\n\n"
            f"📝 **ʀᴇᴀsᴏɴ:** <code>{vazha['reason']}</code>\n\n"
            "📞 ꜰᴏʀ ᴍᴏʀᴇ ɪɴꜰᴏ, ᴘʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ."
        ),
        reply_markup=reply_markup
    )

    try:
        await k.pin()
    except:
        pass

    await bot.leave_chat(message.chat.id)
