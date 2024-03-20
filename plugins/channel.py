import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import BadRequest
from info import CHANNELS, UPDATES_CHNL
from database.ia_filterdb import save_file
from utils import add_chnl_message, get_poster, temp

media_filter = filters.document | filters.video

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    """Media Handler"""
    for file_type in ("document", "video"):
        media = getattr(message, file_type, None)
        if media is not None:
            break
    else:
        return

    media.file_type = file_type
    media.caption = message.caption
    text = await save_file(media)
    if text is not None:
        movie_name, year, languages = await add_chnl_message(text)
        if movie_name is not None:
            languages_str = " ".join(languages) if languages else None
            if year is not None:
                caption = f"<b>#MovieUpdate:\n🧿 <u>𝚃𝙸𝚃𝙻𝙴</u> : <code>{movie_name}</code>\n📆 <u>𝚁𝙴𝙻𝙴𝙰𝚂𝙴</u> : {year}\n"
            else:
                caption = f"<b>#MovieUpdate:\n🧿 <u>𝚃𝙸𝚃𝙻𝙴</u> : <code>{movie_name}</code>\n"
            if languages_str:
                caption += f"🎙️<u>𝙻𝙰𝙽𝙶𝚄𝙰𝙶𝙴</u> : {languages_str}\n"
            caption += "\nCopy & Paste In Group To Search\n---»<a href=https://t.me/isaimini_updates/110> ᴍᴏᴠɪᴇ sᴇᴀʀᴄʜɪɴɢ ɢʀᴏᴜᴘ ʟɪɴᴋs </a>«---</b>"
            search = f"{movie_name} {year}" if year is not None else movie_name
            movies = await get_poster(search)
            search_with_underscore = search.replace(" ", "_")
            btn = [[
                InlineKeyboardButton('◦•●◉✿📥 ᴅᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ 📥✿◉●•◦', url=f"http://t.me/{temp.U_NAME}?start=SEARCH-{search_with_underscore}")
            ]]
            markup = InlineKeyboardMarkup(btn)
            if movies and movies.get('poster'):
                try:
                    await bot.send_photo(
                        chat_id=UPDATES_CHNL,
                        photo=movies.get('poster'),
                        caption=caption,
                        reply_markup=markup,
                        parse_mode=enums.ParseMode.HTML
                    )
                except BadRequest as e:
                    await bot.send_message(
                        chat_id=UPDATES_CHNL,
                        text=caption,
                        reply_markup=markup,
                        parse_mode=enums.ParseMode.HTML
                    )
            else:
                await bot.send_message(
                    chat_id=UPDATES_CHNL,
                    text=caption,
                    reply_markup=markup,
                    parse_mode=enums.ParseMode.HTML
                )
            await asyncio.sleep(5)
