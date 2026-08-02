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
    "📱 *اختر مجالك:*"
)

HELP = (
    "📚 *Mindset Library*\n\n"
    "/start — عرض القائمة الرئيسية\n"
    "/help — هذه المساعدة\n\n"
    "اختر مجالاً، ثم كتاباً لقراءة الوصف وتحميل PDF."
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
async def cb_show_books(cq: CallbackQuery):
    cat_key = cq.data[4:]
    if cat_key not in CATEGORIES:
        await cq.answer("القسم غير موجود", show_alert=True)
        return
    cat = CATEGORIES[cat_key]

    kb = InlineKeyboardBuilder()
    for i, book in enumerate(cat["books"]):
        kb.button(text=f"📖 {book['title']}", callback_data=f"bk_{cat_key}_{i}")
    kb.button(text="🏠 القائمة الرئيسية", callback_data="main_menu")
    kb.adjust(1)

    await cq.message.edit_text(
        f"📚 *{cat['name_ar']}*\nاختر الكتاب:",
        parse_mode="Markdown",
        reply_markup=kb.as_markup()
    )

@router.callback_query(F.data.startswith("bk_"))
async def cb_show_book(cq: CallbackQuery):
    rest = cq.data[3:]
    cat_key, idx_str = rest.rsplit("_", 1)
    idx = int(idx_str)
    if cat_key not in CATEGORIES:
        await cq.answer("القسم غير موجود", show_alert=True)
        return
    books = CATEGORIES[cat_key]["books"]
    if idx >= len(books):
        await cq.answer("الكتاب غير موجود", show_alert=True)
        return
    book = books[idx]

    text = (
        f"📖 *{book['title']}*\n\n"
        f"{book['description']}\n\n"
        f"🔗 [اضغط هنا لتحميل PDF]({book['url']})"
    )

    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 رجوع للكتب", callback_data=f"cat_{cat_key}")
    kb.button(text="🏠 القائمة الرئيسية", callback_data="main_menu")
    kb.adjust(1)

    await cq.message.edit_text(text, parse_mode="Markdown", reply_markup=kb.as_markup(), disable_web_page_preview=False)
