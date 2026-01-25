from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.connections_mdb import add_connection, all_connections, if_active, delete_connection
from info import ADMINS
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@Client.on_message((filters.private | filters.group) & filters.command("connect"))
async def addconnection(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(
            "👤 **ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ᴅᴇᴛᴇᴄᴛᴇᴅ**\n\n"
            f"👉 ᴜsᴇ `/connect {message.chat.id}` ɪɴ ᴘʀɪᴠᴀᴛᴇ",
            quote=True
        )

    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        try:
            _, group_id = message.text.split(" ", 1)
        except:
            await message.reply_text(
                "❌ **ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ**\n\n"
                "✅ ᴜsᴀɢᴇ:\n<code>/connect group_id</code>\n\n"
                "ℹ️ ɢᴇᴛ ɢʀᴏᴜᴘ ɪᴅ ʙʏ ᴀᴅᴅɪɴɢ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ & ᴜsᴇ <code>/id</code>",
                quote=True
            )
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = message.chat.id

    try:
        st = await client.get_chat_member(group_id, userid)
        if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and userid not in ADMINS
        ):
            await message.reply_text(
                "🚫 **ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ**\n\n"
                "🔐 ʏᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ **ᴀᴅᴍɪɴ** ᴏꜰ ᴛʜɪs ɢʀᴏᴜᴘ",
                quote=True
            )
            return
    except Exception as e:
        logger.exception(e)
        await message.reply_text(
            "❌ **ɪɴᴠᴀʟɪᴅ ɢʀᴏᴜᴘ ɪᴅ**\n\n"
            "ℹ️ ᴍᴀᴋᴇ sᴜʀᴇ ɪ'ᴍ ᴀᴅᴅᴇᴅ ᴛᴏ ᴛʜᴇ ɢʀᴏᴜᴘ",
            quote=True
        )
        return

    try:
        st = await client.get_chat_member(group_id, "me")
        if st.status == enums.ChatMemberStatus.ADMINISTRATOR:
            ttl = await client.get_chat(group_id)
            title = ttl.title

            addcon = await add_connection(str(group_id), str(userid))
            if addcon:
                await message.reply_text(
                    f"✅ **ᴄᴏɴɴᴇᴄᴛᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ**\n\n"
                    f"🔗 **ɢʀᴏᴜᴘ:** `{title}`\n"
                    "💬 ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ɪᴛ ꜰʀᴏᴍ ᴘᴍ",
                    quote=True,
                    parse_mode=enums.ParseMode.MARKDOWN
                )

                if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    await client.send_message(
                        userid,
                        f"🔔 **ɢʀᴏᴜᴘ ᴄᴏɴɴᴇᴄᴛᴇᴅ**\n\n"
                        f"📌 `{title}`",
                        parse_mode=enums.ParseMode.MARKDOWN
                    )
            else:
                await message.reply_text(
                    "⚠️ **ᴀʟʀᴇᴀᴅʏ ᴄᴏɴɴᴇᴄᴛᴇᴅ**\n\n"
                    "ℹ️ ᴛʜɪs ɢʀᴏᴜᴘ ɪs ᴀʟʀᴇᴀᴅʏ ʟɪɴᴋᴇᴅ",
                    quote=True
                )
        else:
            await message.reply_text(
                "❗ **ᴀᴅᴍɪɴ ʀᴇQᴜɪʀᴇᴅ**\n\n"
                "➕ ᴘʟᴇᴀsᴇ ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ɪɴ ɢʀᴏᴜᴘ",
                quote=True
            )
    except Exception as e:
        logger.exception(e)
        await message.reply_text(
            "⚠️ **sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ**\n\n"
            "🔁 ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ",
            quote=True
        )
        return


@Client.on_message((filters.private | filters.group) & filters.command("disconnect"))
async def deleteconnection(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(
            "👤 **ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ**\n\n"
            f"👉 ᴜsᴇ `/connect {message.chat.id}` ɪɴ ᴘᴍ",
            quote=True
        )

    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        await message.reply_text(
            "📂 **ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘs**\n\n"
            "👉 ᴜsᴇ /connections ᴛᴏ ᴍᴀɴᴀɢᴇ",
            quote=True
        )

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = message.chat.id

        st = await client.get_chat_member(group_id, userid)
        if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
        ):
            return

        delcon = await delete_connection(str(userid), str(group_id))
        if delcon:
            await message.reply_text(
                "✅ **ᴅɪsᴄᴏɴɴᴇᴄᴛᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ**",
                quote=True
            )
        else:
            await message.reply_text(
                "⚠️ **ɴᴏ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ**\n\n"
                "👉 ᴜsᴇ /connect ᴛᴏ ʟɪɴᴋ ᴛʜɪs ɢʀᴏᴜᴘ",
                quote=True
            )


@Client.on_message(filters.private & filters.command("connections"))
async def connections(client, message):
    userid = message.from_user.id

    groupids = await all_connections(str(userid))
    if groupids is None:
        await message.reply_text(
            "📭 **ɴᴏ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴs**\n\n"
            "➕ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴀ ɢʀᴏᴜᴘ ꜰɪʀsᴛ",
            quote=True
        )
        return

    buttons = []
    for groupid in groupids:
        try:
            ttl = await client.get_chat(int(groupid))
            title = ttl.title
            active = await if_active(str(userid), str(groupid))
            act = " ✅" if active else ""
            buttons.append([
                InlineKeyboardButton(
                    text=f"{title}{act}",
                    callback_data=f"groupcb:{groupid}:{act}"
                )
            ])
        except:
            pass

    if buttons:
        await message.reply_text(
            "📋 **ʏᴏᴜʀ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘs**\n\n"
            "🔘 sᴇʟᴇᴄᴛ ᴀ ɢʀᴏᴜᴘ ᴛᴏ ᴍᴀɴᴀɢᴇ",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    else:
        await message.reply_text(
            "📭 **ɴᴏ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴs**",
            quote=True
      )
