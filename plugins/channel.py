import asyncio
import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import BadRequest
from info import CHANNELS, UPDATES_CHNL
from database.ia_filterdb import save_file
from utils import add_chnl_message, get_poster, temp

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
        mv_naam, year, languages = await add_chnl_message(text)
        logger.info(
                f'{mv_naam} {year} - STEP 2'
            )
        if mv_naam is not None:
            languages_str = " ".join(languages) if languages else None
            logger.info(
                f'{languages_str} - STEP 3'
            )
            if year.isdigit():
                caption = f"<b>#MovieUpdate:\n🧿 <u>𝚃𝙸𝚃𝙻𝙴</u> : <code>{mv_naam}</code>\n📆 <u>YEAR</u> : {year}\n"
            else:
                caption = f"<b>#SeriesUpdate:\n🧿 <u>𝚃𝙸𝚃𝙻𝙴</u> : <code>{mv_naam}</code>\n📆 <u>SEASON</u> : {year}\n"
            if languages_str:
                caption += f"🎙️<u>𝙻𝙰𝙽𝙶𝚄𝙰𝙶𝙴</u> : {languages_str}\n"
            caption += "\nCopy & Paste In Group To Search\n---»<a href=https://t.me/isaimini_updates/110> ᴍᴏᴠɪᴇ sᴇᴀʀᴄʜɪɴɢ ɢʀᴏᴜᴘ ʟɪɴᴋs </a>«---</b>"
            logger.info(
                f'{caption} - STEP 4'
            )
            search = f"{mv_naam} {year}" if year is not None else mv_naam
            logger.info(
                f'{search} - STEP 5'
            )
            movies = await get_poster(search)
            search_with_underscore = search.replace(" ", "_")
            btn = [[
                InlineKeyboardButton('◦•●◉✿📥 ᴅᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ 📥✿◉●•◦', url=f"http://t.me/{temp.U_NAME}?start=SEARCH-{search_with_underscore}")
            ]]
            markup = InlineKeyboardMarkup(btn)
            if movies and movies.get('poster'):
                try:
                    logger.info(
                        f'SENDING POSTER - STEP 6'
                    )
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
                    logger.info(
                        f'POSTER SENT - STEP 7'
                    )
            else:
                logger.info(
                    f'SENDING CAPTION - STEP 6'
                )
                await bot.send_message(
                    chat_id=UPDATES_CHNL,
                    text=caption,
                    reply_markup=markup,
                    parse_mode=enums.ParseMode.HTML
                )
                logger.info(
                    f'CAPTION SENT - STEP 7'
                )
            return
