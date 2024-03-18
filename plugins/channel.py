from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
            mozhi = ", ".join(languages)
            cap = f"<b>#MovieUpdate:\n\n🧿 <u>𝚃𝙸𝚃𝙻𝙴</u> : <code>{movie_name}</code>\n📆 <u>𝚁𝙴𝙻𝙴𝙰𝚂𝙴</u> : {year}🎙️<u>𝙻𝙰𝙽𝙶𝚄𝙰𝙶𝙴</u> : {mozhi}\n\nCopy & Paste In Group To Search\n---»<a href=https://t.me/isaimini_updates/110> ᴍᴏᴠɪᴇ sᴇᴀʀᴄʜɪɴɢ ɢʀᴏᴜᴘ ʟɪɴᴋs </a>«---</b>"
            search = f"{movie_name} {year}"
            movies = await get_poster(search)
            btn = [[
                InlineKeyboardButton('📥 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐍𝐎𝐖 📥', url=f"http://t.me/{temp.U_NAME}?start")
            ]]
            markup = InlineKeyboardMarkup(btn)
            if movies and movies.get('poster'):
                await bot.send_photo(
                    chat_id=UPDATES_CHNL,
                    photo=movies.get('poster'),
                    caption=cap,
                    reply_markup=markup,
                    disable_web_page_preview=True,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await bot.send_message(
                    chat_id=UPDATES_CHNL,
                    text=cap,
                    disable_web_page_preview=True,
                    parse_mode=enums.ParseMode.HTML
                )
