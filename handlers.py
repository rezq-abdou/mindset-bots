from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import CATEGORIES, CATEGORY_ORDER

router = Router()

def reply_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📋 القائمة الرئيسية")]],
        resize_keyboard=True
    )
    return kb

def main_keyboard():
    kb = InlineKeyboardBuilder()
    for key in CATEGORY_ORDER:
        cat = CATEGORIES[key]
        kb.button(text=cat["name_ar"], callback_data=f"cat_{key}")
    kb.adjust(2)
    return kb.as_markup()

WELCOME = (
    "📱 *اختر مجالك:*\n"
)

HELP = (
    "🎓 *Mindset Learning Channels*\n\n"
    "الأمر /start — عرض القائمة الرئيسية\n"
    "الأمر /help — هذه المساعدة\n\n"
    "اختر مجالاً وستظهر لك القنوات مرتبة حسب المستوى."
)

@router.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.answer(WELCOME, reply_markup=main_keyboard())

@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer(HELP, reply_markup=reply_menu())

@router.message(F.text == "📋 القائمة الرئيسية")
async def menu_button(msg: Message):
    await msg.answer(WELCOME, reply_markup=main_keyboard())

@router.message()
async def any_message(msg: Message):
    await msg.answer(WELCOME, reply_markup=main_keyboard())

@router.callback_query(F.data == "main_menu")
async def cb_main_menu(cq: CallbackQuery):
    await cq.message.edit_text("📱 *اختر مجالك:*", reply_markup=main_keyboard())

@router.callback_query(F.data.startswith("cat_"))
async def cb_show_channels(cq: CallbackQuery):
    cat_key = cq.data[4:]
    if cat_key not in CATEGORIES:
        await cq.answer("القسم غير موجود", show_alert=True)
        return
    cat = CATEGORIES[cat_key]

    kb = InlineKeyboardBuilder()
    idx = 0
    for level in cat["levels"]:
        for ch in level["channels"]:
            kb.button(text=f"📺 {ch['name']}", callback_data=f"ch_{idx}_{cat_key}")
            idx += 1
    if cat.get("top_picks"):
        kb.button(text="🏆 أفضل الاختيارات", callback_data=f"top_{cat_key}")
    if cat.get("extra_resources"):
        kb.button(text="📚 مصادر إضافية", callback_data=f"ext_{cat_key}")
    kb.button(text="🏠 القائمة الرئيسية", callback_data="main_menu")
    kb.adjust(1)

    await cq.message.edit_text(
        f"🎯 *{cat['name_ar']}*\nاختر القناة لعرض التفاصيل:",
        parse_mode="Markdown",
        reply_markup=kb.as_markup()
    )

@router.callback_query(F.data.startswith("top_"))
async def cb_top_picks(cq: CallbackQuery):
    cat_key = cq.data[4:]
    cat = CATEGORIES[cat_key]
    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 الرجوع للقنوات", callback_data=f"cat_{cat_key}")
    kb.button(text="🏠 القائمة الرئيسية", callback_data="main_menu")
    kb.adjust(1)
    await cq.message.edit_text(
        f"🏆 *أفضل الاختيارات*\n{cat['top_picks']}",
        parse_mode="Markdown",
        reply_markup=kb.as_markup()
    )

@router.callback_query(F.data.startswith("ext_"))
async def cb_extra(cq: CallbackQuery):
    cat_key = cq.data[4:]
    cat = CATEGORIES[cat_key]
    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 الرجوع للقنوات", callback_data=f"cat_{cat_key}")
    kb.button(text="🏠 القائمة الرئيسية", callback_data="main_menu")
    kb.adjust(1)
    await cq.message.edit_text(
        f"📚 *مصادر إضافية*\n{cat['extra_resources']}",
        parse_mode="Markdown",
        reply_markup=kb.as_markup()
    )

@router.callback_query(F.data.startswith("ch_"))
async def cb_show_channel(cq: CallbackQuery):
    rest = cq.data[3:]
    idx_str, cat_key = rest.split("_", 1)
    idx = int(idx_str)
    if cat_key not in CATEGORIES:
        await cq.answer("القسم غير موجود", show_alert=True)
        return
    cat = CATEGORIES[cat_key]

    flat = []
    for level in cat["levels"]:
        for ch in level["channels"]:
            flat.append(ch)
    if idx >= len(flat):
        await cq.answer("القناة غير موجودة", show_alert=True)
        return
    ch = flat[idx]

    url = ch['url']
    if url.startswith('https://www.youtube.com/@') or url.startswith('https://youtube.com/@'):
        url += '/about'

    text = (
        f"📺 *{ch['name']}*\n"
        f"💡 {ch['why']}\n"
        f"📚 {ch['content']}\n"
        f"👤 {ch['for']}\n\n"
        f"🔗 {url}"
    )
    if "preview_url" in ch:
        text += f"\n{ch['preview_url']}"

    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 الرجوع للقنوات", callback_data=f"cat_{cat_key}")
    kb.button(text="🏠 القائمة الرئيسية", callback_data="main_menu")
    kb.adjust(1)

    await cq.message.edit_text(text, parse_mode="Markdown", reply_markup=kb.as_markup(), disable_web_page_preview=False)
