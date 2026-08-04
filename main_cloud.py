import asyncio
import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# ============================================================
#  BOT 1 DATA  (channels)
# ============================================================

CAT1 = {
    "german": {
        "name_ar": "🇩🇪 الألمانية",
        "name_en": "🇩🇪 German",
        "levels": [
            {
                "level": "🟢 المستوى الأول: المبتدئ (A1 - A2)",
                "channels": [
                    {"name": "الألمانية مع مستر شحاتة", "why": "أفضل قناة عربية لتأسيس اللغة من الصفر مع شرح مبسط للقواعد والمفردات", "content": "قواعد، مفردات، تأسيس", "for": "المبتدئين من الصفر", "url": "https://www.youtube.com/@mohammadshehata-official"},
                    {"name": "Deutsch mit Mira", "why": "شرح عربي حديث وممتع مع تركيز على المحادثة والنطق", "content": "محادثة، نطق، قواعد", "for": "المبتدئين", "url": "https://www.youtube.com/@DeutschmitMira"},
                    {"name": "Deutsch mit Hend", "why": "تعلم الألمانية مجاناً وبنظام وبساطة مع شرح عربي مناسب للمبتدئين", "content": "قواعد، محادثة، مبتدئين", "for": "المبتدئين", "url": "https://www.youtube.com/@FrauHendTaha"},
                    {"name": "Learn German", "why": "أفضل قناة أجنبية لبناء أساس قوي في القواعد والمفردات", "content": "قواعد، مفردات، تأسيس", "for": "بناء أساس قوي", "url": "https://www.youtube.com/@LearnGermanOriginal"},
                    {"name": "DW Learn German", "why": "منهج مجاني ورسمي من مؤسسة ألمانية، يغطي المستويات من A1 إلى C1", "content": "منهج متكامل، قواعد، تمارين", "for": "جميع المستويات", "url": "https://www.youtube.com/@dwlearngerman"},
                    {"name": "Lingoni German", "why": "دروس مرتبة وسهلة مع شرح واضح للقواعد والنطق", "content": "قواعد، نطق، دروس منظمة", "for": "الانتقال من A1 إلى B1", "url": "https://www.youtube.com/@lingonigerman"}
                ]
            },
            {
                "level": "🟡 المستوى الثاني: المتوسط (B1 - B2)",
                "channels": [
                    {"name": "Easy German", "why": "أفضل قناة لتحسين الاستماع والمحادثة من خلال مواقف واقعية مع متحدثين أصليين", "content": "استماع، محادثة، مقابلات", "for": "تطوير الاستماع والمحادثة", "url": "https://www.youtube.com/@EasyGerman"},
                    {"name": "Deutsch für Euch", "why": "شرح متعمق للقواعد والتعبيرات المستخدمة في الحياة والعمل", "content": "قواعد، تعبيرات، عمل", "for": "من يستعد للدراسة أو الوظيفة", "url": "https://www.youtube.com/@DeutschFuerEuch"},
                    {"name": "YourGermanTeacher", "why": "شرح احترافي للقواعد مع الكثير من الأمثلة", "content": "قواعد، أمثلة، نطق", "for": "المتوسطين", "url": "https://www.youtube.com/@YourGermanTeacher"},
                    {"name": "Deutsch mit Benjamin", "why": "يركز على تطوير الدقة اللغوية والتحدث بطلاقة", "content": "قواعد متقدمة، طلاقة", "for": "تطوير الدقة اللغوية", "url": "https://www.youtube.com/@DeutschmitBenjamin"},
                    {"name": "ثواني ألمانية مع إلهان", "why": "يركز على المحادثة والتعبيرات اليومية المستخدمة في ألمانيا", "content": "محادثة، تعبيرات يومية", "for": "الحياة اليومية في ألمانيا", "url": "https://www.youtube.com/@IlhanBozan"},
                    {"name": "Khaled Bozan", "why": "يجمع بين تعلم اللغة ونصائح الحياة والعمل في ألمانيا", "content": "لغة، حياة، عمل", "for": "من يريد العيش في ألمانيا", "url": "https://www.youtube.com/@KhaledBozan"}
                ]
            },
            {
                "level": "🔴 المستوى الثالث: المتقدم (C1 - C2)",
                "channels": [
                    {"name": "German with Laura", "why": "تشرح منطق اللغة الألمانية بعمق، ومناسبة للمستويات المتقدمة", "content": "قواعد متقدمة، منطق اللغة", "for": "المستويات المتقدمة", "url": "https://www.youtube.com/@GermanwithLaura"},
                    {"name": "DW Deutsch", "why": "أخبار وتقارير باللغة الألمانية تساعد على تطوير المفردات المهنية والأكاديمية", "content": "أخبار، تقارير، مفردات مهنية", "for": "الوصول إلى C1+", "url": "https://www.youtube.com/@dwdeutsch"},
                    {"name": "MrWissen2Go", "why": "محتوى ثقافي وتعليمي متقدم يساعد على توسيع المفردات", "content": "ثقافة، تعليم، مفردات", "for": "توسيع المفردات", "url": "https://www.youtube.com/@MrWissen2go"},
                    {"name": "ARD", "why": "برامج وتقارير باللغة الألمانية الفصحى", "content": "برامج، تقارير، لغة فصحى", "for": "الاستماع المتقدم", "url": "https://www.youtube.com/@ARD"},
                    {"name": "ZDFheute Nachrichten", "why": "أفضل قناة لمتابعة الأخبار وتطوير الاستماع باللغة الألمانية", "content": "أخبار، استماع، مفردات", "for": "متابعة الأخبار والاستماع", "url": "https://www.youtube.com/@ZDFheute"}
                ]
            },
            {
                "level": "💼 الألمانية للأعمال (Business German)",
                "channels": [
                    {"name": "Make it in Germany", "why": "القناة الرسمية للعمل والهجرة المهنية في ألمانيا، معلومات عن الوظائف، كتابة السيرة الذاتية، والمقابلات", "content": "وظائف، سيرة ذاتية، مقابلات", "for": "من يريد العمل في ألمانيا", "url": "https://www.youtube.com/channel/UCNzqd4kCgP523WInjCNQNQQ"},
                    {"name": "Bundesagentur für Arbeit", "why": "القناة الرسمية لوكالة التوظيف الألمانية، معلومات عن سوق العمل والتدريب المهني", "content": "سوق عمل، تدريب مهني", "for": "باحثين عن عمل في ألمانيا", "url": "https://www.youtube.com/user/Arbeitsagentur"}
                ]
            }
        ],
        "top_picks": "🥇 الألمانية مع مستر شحاتة\n🥇 DW Learn German\n🥇 Learn German\n4️⃣ Easy German\n5️⃣ Deutsch mit Mira\n6️⃣ Lingoni German\n7️⃣ Deutsch für Euch\n8️⃣ YourGermanTeacher\n9️⃣ Khaled Bozan\n🔟 Make it in Germany",
        "extra_resources": "📌 *مسار التعلم الموصى به:*\n\n1️⃣ ابدأ بقناة *الألمانية مع مستر شحاتة* لفهم الأساسيات بالعربية\n2️⃣ بالتوازي، تابع *DW Learn German* لتعتاد على الألمانية الأصلية\n3️⃣ بعد إنهاء مستوى A2، انتقل إلى *Easy German* لتحسين الاستماع والمحادثة\n4️⃣ في مستوى B1/B2، ركز على *Deutsch für Euch* و *YourGermanTeacher*\n5️⃣ إذا كان هدفك العمل في ألمانيا، أضف *Make it in Germany* و *Bundesagentur für Arbeit* لمعرفة لغة وسوق العمل"
    },
    "entrepreneurship": {
        "name_ar": "🚀 ريادة الأعمال",
        "name_en": "🚀 Entrepreneurship",
        "levels": [
            {
                "level": "⭐ قنوات مميزة",
                "channels": [
                    {"name": "Alex Hormozi", "why": "استراتيجيات بناء الشركات وزيادة الأرباح", "content": "تسويق، مبيعات، ريادة", "for": "رواد الأعمال", "url": "https://youtube.com/@alexhormozi"},
                    {"name": "Gary Vaynerchuk", "why": "تسويق رقمي وريادة أعمال ونصائح عملية", "content": "تسويق، علامة تجارية، ريادة", "for": "المسوقين وأصحاب المشاريع", "url": "https://youtube.com/@garyvee"},
                    {"name": "Y Combinator", "why": "نصائح من أكبر مسرعة شركات ناشئة في العالم", "content": "شركات ناشئة، تمويل، نمو", "for": "مؤسسي الشركات الناشئة", "url": "https://youtube.com/@ycombinator"},
                    {"name": "Stanford Entrepreneurship", "why": "محتوى أكاديمي من جامعة ستانفورد", "content": "ريادة، ابتكار، قيادة", "for": "من يريد تعليماً أكاديمياً", "url": "https://youtube.com/@stanfordgsb"},
                    {"name": "Noah Kagan", "why": "تجارب عملية في بناء المشاريع وزيادة الأرباح وبناء الثروة", "content": "مشاريع، أرباح، ثروة", "for": "رواد الأعمال", "url": "https://youtube.com/@noahkagan"}
                ]
            }
        ]
    },
    "ecommerce": {
        "name_ar": "🛒 التجارة الإلكترونية",
        "name_en": "🛒 E-commerce",
        "levels": [
            {
                "level": "🟢 المستوى الأول: المبتدئ",
                "channels": [
                    {"name": "ياسين زروال", "why": "من أفضل صناع المحتوى الجزائريين في التجارة الإلكترونية، يشرح بأسلوب عملي يناسب السوق الجزائري", "content": "تجارة إلكترونية، دروبشيبينغ، سوق جزائري", "for": "المبتدئين في العالم العربي", "url": "https://www.youtube.com/@YacineZeroual"},
                    {"name": "Ismail Rouji", "why": "شروحات عملية للتجارة الإلكترونية وبناء المتاجر وزيادة المبيعات", "content": "تجارة إلكترونية، متاجر، مبيعات", "for": "المبتدئين", "url": "https://www.youtube.com/@ismailrouji"},
                    {"name": "Shopify", "why": "القناة الرسمية لـ Shopify، شروحات احترافية لإنشاء وإدارة المتاجر الإلكترونية", "content": "Shopify، متاجر، إدارة", "for": "أصحاب المتاجر", "url": "https://www.youtube.com/@Shopify"},
                    {"name": "Oberlo", "why": "رغم توقف الخدمة، ما زال أرشيفها من أفضل المصادر لتعلم أساسيات التجارة الإلكترونية والدروبشيبينغ", "content": "دروبشيبينغ، أساسيات، أرشيف", "for": "تعلم الدروبشيبينغ", "url": "https://www.youtube.com/c/oberlo"},
                    {"name": "Learn With Shopify", "why": "تركز على بناء المتاجر، اختيار المنتجات، وزيادة المبيعات", "content": "بناء متاجر، منتجات، مبيعات", "for": "أصحاب المتاجر", "url": "https://www.youtube.com/@LearnWithShopify"}
                ]
            },
            {
                "level": "🟡 المستوى الثاني: المتوسط",
                "channels": [
                    {"name": "Alex Hormozi", "why": "أفضل قناة لفهم كيفية بناء العروض، التسعير، وزيادة الأرباح", "content": "عروض، تسعير، أرباح", "for": "رواد الأعمال", "url": "https://www.youtube.com/@AlexHormozi"},
                    {"name": "Flown Marketing", "why": "تركز على التسويق العملي، الإعلانات، واستراتيجيات تنمية المتاجر الإلكترونية", "content": "تسويق، إعلانات، استراتيجيات", "for": "أصحاب المتاجر", "url": "https://www.youtube.com/@flowndz"},
                    {"name": "HubSpot", "why": "تعلم التسويق، المبيعات، وإدارة العملاء — مهارات أساسية لنجاح أي متجر", "content": "تسويق، مبيعات، عملاء", "for": "جميع المستويات", "url": "https://www.youtube.com/@hubspotmarketing"},
                    {"name": "Google", "why": "تشرح أدوات Google التي يحتاجها أصحاب المتاجر مثل Analytics وMerchant Center", "content": "Google Analytics، أدوات، تحليلات", "for": "أصحاب المتاجر", "url": "https://www.youtube.com/@Google"},
                    {"name": "Meta for Business", "why": "المصدر الرسمي لتعلم إعلانات Facebook وInstagram", "content": "إعلانات، فيسبوك، إنستغرام", "for": "المعلنين", "url": "https://www.youtube.com/@MetaforBusiness"},
                    {"name": "Semrush", "why": "لتعلم SEO، وتحليل المنافسين، وزيادة الزيارات المجانية", "content": "SEO، تحليل منافسين", "for": "متخصصي التسويق", "url": "https://www.youtube.com/@semrush"},
                    {"name": "Ahrefs", "why": "من أفضل القنوات لتعلم SEO وتسويق المحتوى", "content": "SEO، تسويق محتوى", "for": "متخصصي SEO", "url": "https://www.youtube.com/@AhrefsCom"}
                ]
            },
            {
                "level": "🔴 المستوى الثالث: المتقدم",
                "channels": [
                    {"name": "Y Combinator", "why": "لتعلم بناء الشركات، التفكير الريادي، والتوسع", "content": "ريادة أعمال، شركات ناشئة", "for": "مؤسسي الشركات", "url": "https://www.youtube.com/@ycombinator"},
                    {"name": "CXL", "why": "أفضل مصدر لتحسين معدل التحويل (CRO) وتحليل سلوك العملاء", "content": "CRO، تحسين تحويل، عملاء", "for": "محترفي التسويق", "url": "https://www.youtube.com/@CXLdotcom"},
                    {"name": "Neil Patel", "why": "خبير عالمي في التسويق الرقمي، SEO، وزيادة المبيعات", "content": "تسويق رقمي، SEO، مبيعات", "for": "المسوقين", "url": "https://www.youtube.com/@NeilPatel"},
                    {"name": "GaryVee", "why": "يركز على العلامة التجارية الشخصية، المحتوى، وريادة الأعمال", "content": "علامة تجارية، محتوى، ريادة", "for": "رواد الأعمال", "url": "https://www.youtube.com/@garyvee"},
                    {"name": "My First Million", "why": "تحليل أفكار المشاريع والمتاجر الناجحة واستراتيجيات النمو", "content": "أفكار مشاريع، نمو", "for": "رواد الأعمال", "url": "https://www.youtube.com/@MyFirstMillionPod"}
                ]
            }
        ],
        "top_picks": "🥇 Shopify\n🥇 Alex Hormozi\n🥇 HubSpot\n4️⃣ Learn With Shopify\n5️⃣ Meta for Business\n6️⃣ Google\n7️⃣ Flown Marketing\n8️⃣ CXL\n9️⃣ Ahrefs\n🔟 Y Combinator",
        "extra_resources": "📌 *مسار التعلم الموصى به:*\n\n1️⃣ ابدأ مع *ياسين زروال* أو *Ismail Rouji* إذا كنت تفضل الشرح بالعربية\n2️⃣ انتقل إلى *Shopify* و *Learn With Shopify* لفهم بناء وإدارة المتاجر\n3️⃣ تعلم التسويق من *HubSpot* و *Meta for Business* و *Google*\n4️⃣ طور مهاراتك في زيادة المبيعات والعروض مع *Alex Hormozi*\n5️⃣ تعلم تحسين المتجر ورفع معدل التحويل من *CXL*، وادرس استراتيجيات النمو من *Y Combinator*"
    },
    "digital_marketing": {
        "name_ar": "📈 التسويق الرقمي",
        "name_en": "📈 Digital Marketing",
        "levels": [
            {
                "level": "⭐ قنوات مميزة",
                "channels": [
                    {"name": "Neil Patel", "why": "خبير عالمي في التسويق الرقمي وتحسين محركات البحث", "content": "SEO، تسويق، تحليلات", "for": "المسوقين", "url": "https://youtube.com/@neilpatel"},
                    {"name": "HubSpot", "why": "مصدر تعليمي رسمي لجميع مجالات التسويق", "content": "تسويق، مبيعات، خدمة عملاء", "for": "المبتدئين والمحترفين", "url": "https://youtube.com/@hubspotmarketing"},
                    {"name": "Semrush", "why": "SEO وتحسين ظهور المواقع في محركات البحث", "content": "SEO، محتوى، تحليلات", "for": "متخصصي SEO", "url": "https://youtube.com/@semrush"},
                    {"name": "Ahrefs", "why": "دروس متقدمة في SEO وبحث الكلمات المفتاحية", "content": "SEO، كلمات مفتاحية", "for": "متخصصي التسويق", "url": "https://youtube.com/@AhrefsCom"},
                    {"name": "Meta for Business", "why": "القناة الرسمية لتعلم إعلانات ميتا", "content": "فيسبوك، إنستغرام، إعلانات", "for": "المعلنين", "url": "https://youtube.com/@metaforbusiness"}
                ]
            }
        ]
    },
    "ai": {
        "name_ar": "🤖 الذكاء الاصطناعي",
        "name_en": "🤖 Artificial Intelligence",
        "levels": [
            {
                "level": "⭐ قنوات مميزة",
                "channels": [
                    {"name": "Two Minute Papers", "why": "شروحات مبسطة لأحدث أبحاث AI", "content": "أبحاث، تقنيات جديدة", "for": "عشاق التقنية", "url": "https://youtube.com/@twominutepapers"},
                    {"name": "Andrej Karpathy", "why": "دروس متعمقة في تعلم الآلة من خبير OpenAI", "content": "تعلم آلة، شبكات عصبية", "for": "المبرمجين", "url": "https://youtube.com/@andrejkarpathy"},
                    {"name": "3Blue1Brown", "why": "شروحات رياضية مبصرة للتعلم العميق", "content": "رياضيات، تعلم عميق", "for": "من يريد فهم الرياضيات", "url": "https://youtube.com/@3blue1brown"},
                    {"name": "AI Explained", "why": "تحليل وشرح آخر تطورات AI", "content": "AI، ChatGPT، أخبار", "for": "المتابعين لأخبار AI", "url": "https://youtube.com/@AIexplained-official"},
                    {"name": "sentdex", "why": "برامج عملية في تعلم الآلة والبايثون", "content": "بايثون، تعلم آلة", "for": "المبرمجين", "url": "https://youtube.com/@sentdex"}
                ]
            }
        ]
    },
    "programming": {
        "name_ar": "💻 البرمجة",
        "name_en": "💻 Programming",
        "levels": [
            {
                "level": "⭐ قنوات مميزة",
                "channels": [
                    {"name": "freeCodeCamp", "why": "دورات كاملة ومجانية في جميع لغات البرمجة", "content": "جميع اللغات، مشاريع", "for": "جميع المستويات", "url": "https://youtube.com/@freecodecamp"},
                    {"name": "CodeWithHarry", "why": "شروحات برمجة بلغة بسيطة ومشاريع عملية", "content": "ويب، بايثون، JavaScript", "for": "المبتدئين", "url": "https://youtube.com/@codewithharry"},
                    {"name": "Net Ninja", "why": "شروحات منظمة لأطر العمل الحديثة", "content": "React, Node.js, Flutter", "for": "مطوري الويب", "url": "https://youtube.com/@NetNinja"},
                    {"name": "Traversy Media", "why": "دروس سريعة ومشاريع كاملة", "content": "HTML, CSS, JS, Python", "for": "مطوري الويب", "url": "https://youtube.com/@traversymedia"},
                    {"name": "Programming with Mosh", "why": "دورات احترافية لتعلم البرمجة", "content": "Python, JavaScript, C#", "for": "جميع المستويات", "url": "https://youtube.com/@programmingwithmosh"}
                ]
            }
        ]
    },
    "graphic_design": {
        "name_ar": "🎨 التصميم الجرافيكي",
        "name_en": "🎨 Graphic Design",
        "levels": [
            {
                "level": "⭐ قنوات مميزة",
                "channels": [
                    {"name": "Satori Graphics", "why": "دروس تصميم احترافية ومبادئ التصميم", "content": "مبادئ التصميم، أدوات", "for": "المصممين", "url": "https://youtube.com/@satorigraphics"},
                    {"name": "Will Paterson", "why": "تصميم الشعارات والهويات البصرية", "content": "شعارات، براندينغ", "for": "مصممي الشعارات", "url": "https://youtube.com/@willpaterson"},
                    {"name": "Tutvid", "why": "دروس في Photoshop و Illustrator و After Effects", "content": "Adobe Suite", "for": "مستخدمي Adobe", "url": "https://youtube.com/@tutvid"},
                    {"name": "Piximperfect", "why": "أفضل قناة لتعليم Photoshop بطريقة احترافية", "content": "Photoshop، مونتاج", "for": "مستخدمي Photoshop", "url": "https://youtube.com/@piximperfect"},
                    {"name": "Figma", "why": "القناة الرسمية لتعلم التصميم بـ Figma", "content": "Figma، UI/UX", "for": "مصممي UI/UX", "url": "https://youtube.com/@figma"}
                ]
            }
        ]
    },
    "video_editing": {
        "name_ar": "🎬 المونتاج",
        "name_en": "🎬 Video Editing",
        "levels": [
            {
                "level": "⭐ قنوات مميزة",
                "channels": [
                    {"name": "Film Riot", "why": "دروس مونتاج متقدمة ومؤثرات بصرية", "content": "مونتاج، مؤثرات", "for": "المحررين", "url": "https://youtube.com/@filmriot"},
                    {"name": "Peter McKinnon", "why": "نصائح تصوير ومونتاج بطريقة إبداعية", "content": "تصوير، مونتاج", "for": "صانعي المحتوى", "url": "https://youtube.com/@petermckinnon"},
                    {"name": "Premiere Basics", "why": "دروس مبسطة لـ Premiere Pro", "content": "Premiere Pro", "for": "المبتدئين", "url": "https://youtube.com/@premierebasics"},
                    {"name": "SonduckFilm", "why": "دروس After Effects ومؤثرات حركية", "content": "After Effects", "for": "مصممي الحركة", "url": "https://youtube.com/@sonduckfilm"},
                    {"name": "Davinci Resolve", "why": "القناة الرسمية لتعلم Davinci Resolve", "content": "Davinci Resolve", "for": "جميع المستويات", "url": "https://youtube.com/@davinciresolve"}
                ]
            }
        ]
    },
    "content_creation": {
        "name_ar": "🎥 صناعة المحتوى",
        "name_en": "🎥 Content Creation",
        "levels": [
            {
                "level": "⭐ قنوات مميزة",
                "channels": [
                    {"name": "Think Media", "why": "نصائح شاملة لصانعي المحتوى", "content": "يوتيوب، تصوير، نمو", "for": "اليوتيوبرز", "url": "https://youtube.com/@thinkmedia"},
                    {"name": "Video Influencers", "why": "استراتيجيات نمو القنوات", "content": "نمو القنوات، خوارزميات", "for": "صانعي المحتوى", "url": "https://youtube.com/@videoinfluencers"},
                    {"name": "Ali Abdaal", "why": "إنتاجية وعمل حر وصناعة محتوى تعليمي", "content": "إنتاجية، يوتيوب", "for": "صانعي المحتوى", "url": "https://youtube.com/@aliabdaal"},
                    {"name": "Roberto Blake", "why": "نصائح في الإبداع والتسويق", "content": "إبداع، تسويق", "for": "المبدعين", "url": "https://youtube.com/@robertoblake"},
                    {"name": "Creator Insider", "why": "قناة رسمية من يوتيوب", "content": "أخبار يوتيوب", "for": "اليوتيوبرز", "url": "https://youtube.com/@creatorinsider"}
                ]
            }
        ]
    },
    "freelancing": {
        "name_ar": "💼 العمل الحر",
        "name_en": "💼 Freelancing",
        "levels": [
            {
                "level": "⭐ قنوات مميزة",
                "channels": [
                    {"name": "The Futur", "why": "أفضل قناة لتعلم فن البيع والتصميم وبناء العلامات التجارية من Chris Do", "content": "فريلانس، براندينغ، بيع", "for": "المستقلين والمصممين", "url": "https://youtube.com/@thefutur"},
                    {"name": "Biaheza", "why": "تجارب واقعية في الربح من الإنترنت", "content": "دروبشيبينغ، فريلانس", "for": "من يريد الربح", "url": "https://youtube.com/@biaheza"},
                    {"name": "Charlie Morgan", "why": "نصائح في العمل الحر", "content": "فريلانس، تسويق", "for": "المستقلين", "url": "https://youtube.com/@charliemofficial"},
                    {"name": "Josh Burns", "why": "استراتيجيات الفوز بالمشاريع", "content": "عروض، مشاريع", "for": "مستقلين Upwork", "url": "https://youtube.com/@joshburns"},
                    {"name": "HBA Services", "why": "قناة ضخمة تقدم محتوى عملي في العمل الحر والتسويق الرقمي وبناء الدخل من الإنترنت", "content": "فريلانس، تسويق رقمي، دخل", "for": "المبتدئين والمحترفين", "url": "https://youtube.com/@hbaservices"}
                ]
            }
        ]
    },
    "sales": {
        "name_ar": "🤝 المبيعات والتفاوض",
        "name_en": "🤝 Sales & Negotiation",
        "levels": [
            {
                "level": "⭐ قنوات مميزة",
                "channels": [
                    {"name": "Grant Cardone", "why": "خبير مبيعات عالمي", "content": "مبيعات، تسويق", "for": "رجال المبيعات", "url": "https://youtube.com/@grantcardone"},
                    {"name": "Jordan Belfort", "why": "نظام المبيعات الخطي", "content": "مبيعات، إقناع", "for": "محترفي المبيعات", "url": "https://youtube.com/@jordanbelfortofficial"},
                    {"name": "Dan Lok", "why": "خبير في الإقناع", "content": "مبيعات، قيادة", "for": "رواد الأعمال", "url": "https://youtube.com/@danlok"},
                    {"name": "Victor Antonio", "why": "استراتيجيات مبيعات B2B", "content": "B2B، تفاوض", "for": "محترفي B2B", "url": "https://youtube.com/@victorantonio"},
                    {"name": "Chris Voss", "why": "تقنيات تفاوض من FBI — أفضل مصدر لتعلم فن التفاوض والإقناع", "content": "تفاوض، اتصال، إقناع", "for": "الجميع", "url": "https://youtube.com/@Blackswanltd1"}
                ]
            }
        ]
    },
    "personal_finance": {
        "name_ar": "💰 التمويل الشخصي",
        "name_en": "💰 Personal Finance",
        "levels": [
            {
                "level": "⭐ قنوات مميزة",
                "channels": [
                    {"name": "Graham Stephan", "why": "نصائح في الاستثمار والتمويل", "content": "استثمار، عقارات", "for": "المبتدئين", "url": "https://youtube.com/@grahamstephan"},
                    {"name": "Andrei Jikh", "why": "الاستثمار في الأسهم والعملات", "content": "أسهم، كريبتو", "for": "المستثمرين", "url": "https://youtube.com/@andreijikh"},
                    {"name": "The Financial Diet", "why": "نصائح مالية بسيطة", "content": "ميزانية، توفير", "for": "الشباب", "url": "https://youtube.com/@thefinancialdiet"},
                    {"name": "Minority Mindset", "why": "ثقافة مالية وبناء ثروة", "content": "ثقافة مالية", "for": "بناة الثروة", "url": "https://youtube.com/@minoritymindset"},
                    {"name": "Meet Kevin", "why": "تحليل الأسواق والعقارات", "content": "عقارات، أسهم", "for": "المستثمرين", "url": "https://youtube.com/@meetkevin"}
                ]
            }
        ]
    },
    "english": {
        "name_ar": "🇬🇧 الإنجليزية",
        "name_en": "🇬🇧 English",
        "levels": [
            {
                "level": "🟢 المستوى الأول: المبتدئ (A1 - A2)",
                "channels": [
                    {"name": "ZAmericanEnglish", "why": "أشهر قناة عربية لتعلم الإنجليزية من الصفر حتى الاحتراف، بمنهج منظم ومتكامل", "content": "تأسيس، قواعد، منهج متكامل", "for": "المبتدئين من الصفر", "url": "https://www.youtube.com/@ZAmericanEnglish"},
                    {"name": "English with Ehab", "why": "يشرح الإنجليزية بالعربية بطريقة عملية وسهلة مع التركيز على المحادثة", "content": "قواعد، محادثة، شرح عربي", "for": "المبتدئين", "url": "https://www.youtube.com/channel/UCa3TXR0vxlj4uKgQNTvXAHw"},
                    {"name": "BBC Learning English", "why": "واحدة من أفضل القنوات الرسمية لتعلم الإنجليزية البريطانية، تغطي القواعد، المفردات، والنطق", "content": "قواعد، مفردات، نطق، أخبار", "for": "جميع المستويات", "url": "https://www.youtube.com/@bbclearningenglish"},
                    {"name": "VOA Learning English", "why": "تعلم الإنجليزية من خلال أخبار مبسطة، ممتازة لتطوير الاستماع", "content": "استماع، أخبار مبسطة، مفردات", "for": "تطوير الاستماع", "url": "https://www.youtube.com/@VOALearningEnglish"},
                    {"name": "Speak English With Vanessa", "why": "تركز على المحادثة اليومية والنطق الطبيعي", "content": "محادثة، نطق، تعبيرات", "for": "تطوير المحادثة", "url": "https://www.youtube.com/@SpeakEnglishWithVanessa"},
                    {"name": "English with Lucy", "why": "شرح احترافي للقواعد والنطق والمفردات", "content": "نطق بريطاني، قواعد، مفردات", "for": "محبي اللهجة البريطانية", "url": "https://www.youtube.com/@EnglishwithLucy"}
                ]
            },
            {
                "level": "🟡 المستوى الثاني: المتوسط (B1 - B2)",
                "channels": [
                    {"name": "English With Khaled", "why": "قناة عربية بجودة عالية لتعلم الإنجليزية بأسلوب محترف وسهل لجميع المستويات", "content": "قواعد، محادثة، شرح عربي", "for": "جميع المستويات", "url": "https://www.youtube.com/@englishwithkhaled"},
                    {"name": "Oxford Online English", "why": "دروس احترافية في الإنجليزية العامة والمهنية", "content": "قواعد، محادثة، إنجليزية مهنية", "for": "المتوسطين والمحترفين", "url": "https://www.youtube.com/@Oxfordonlineenglish1"},
                    {"name": "Learn English with TV Series", "why": "تعلم الإنجليزية من الأفلام والمسلسلات بطريقة ممتعة", "content": "مفردات، نطق، تعبيرات عامية", "for": "محبي الأفلام والمسلسلات", "url": "https://www.youtube.com/@LearnEnglishWithTVSeries"},
                    {"name": "EnglishClass101", "why": "دروس منظمة للمحادثة والاستماع والمفردات", "content": "محادثة، استماع، مفردات", "for": "المبتدئين والمتوسطين", "url": "https://www.youtube.com/@EnglishClass101"},
                    {"name": "Rachel's English", "why": "أفضل قناة لتحسين النطق الأمريكي", "content": "نطق أمريكي، لكنة، محادثة", "for": "تحسين النطق", "url": "https://www.youtube.com/@rachelsenglish"},
                    {"name": "mmmEnglish", "why": "تشرح المحادثة والقواعد والأخطاء الشائعة بطريقة عملية", "content": "محادثة، قواعد، أخطاء شائعة", "for": "المتوسطين", "url": "https://www.youtube.com/@mmmEnglish"},
                    {"name": "English with Jennifer", "why": "دروس هادئة ومنظمة لتطوير القواعد والمحادثة", "content": "قواعد، محادثة، دروس منظمة", "for": "جميع المستويات", "url": "https://www.youtube.com/@Englishwithjennifer"}
                ]
            },
            {
                "level": "🔴 المستوى الثالث: المتقدم (C1 - C2)",
                "channels": [
                    {"name": "Business English Pod", "why": "أفضل قناة عالميًا لتعلم الإنجليزية الخاصة بالأعمال، الاجتماعات، البريد الإلكتروني، والعروض التقديمية", "content": "اجتماعات، بريد إلكتروني، عروض", "for": "رجال الأعمال والموظفين", "url": "https://www.youtube.com/@BusinessEnglishPod"},
                    {"name": "Business English with Christina", "why": "ممتازة للمستقلين ورواد الأعمال، مع تركيز على التواصل المهني", "content": "تواصل مهني، أعمال", "for": "المستقلين ورواد الأعمال", "url": "https://www.youtube.com/@ChristinaRebuffet"},
                    {"name": "Learn English with Rebecca", "why": "تحتوي على دروس متقدمة وسلسلة قوية في الإنجليزية للأعمال", "content": "Business English، دروس متقدمة", "for": "محترفي الأعمال", "url": "https://www.youtube.com/@engvidRebecca"},
                    {"name": "Harvard Business Review", "why": "لتعلم لغة الإدارة والقيادة وريادة الأعمال", "content": "إدارة، قيادة، ريادة أعمال", "for": "القادة والمديرين", "url": "https://www.youtube.com/@HarvardBusinessReview"},
                    {"name": "TED", "why": "أفضل مصدر لتطوير الاستماع والمفردات الأكاديمية والمهنية", "content": "استماع، مفردات أكاديمية", "for": "تطوير الاستماع المتقدم", "url": "https://www.youtube.com/@TED"},
                    {"name": "Stanford Graduate School of Business", "why": "محاضرات في الإدارة والقيادة وريادة الأعمال بلغة احترافية", "content": "إدارة، قيادة، اقتصاد", "for": "رواد الأعمال", "url": "https://www.youtube.com/@stanfordgsb"},
                    {"name": "LinkedIn", "why": "محتوى عن الوظائف، التواصل المهني، والمهارات المطلوبة في سوق العمل", "content": "وظائف، تواصل مهني، مهارات", "for": "الباحثين عن عمل والمحترفين", "url": "https://www.youtube.com/@LinkedIn"}
                ]
            }
        ],
        "top_picks": "🥇 ZAmericanEnglish\n🥇 BBC Learning English\n🥇 VOA Learning English\n4️⃣ English with Lucy\n5️⃣ Speak English With Vanessa\n6️⃣ Oxford Online English\n7️⃣ Learn English with TV Series\n8️⃣ Business English Pod\n9️⃣ Rachel's English\n🔟 TED",
        "extra_resources": "📌 *مسار التعلم الموصى به:*\n\n1️⃣ ابدأ مع *ZAmericanEnglish* لبناء أساس قوي باللغة العربية\n2️⃣ بالتوازي، تابع *BBC Learning English* و *VOA Learning English* لتطوير الاستماع والمفردات\n3️⃣ عند الوصول إلى المستوى المتوسط، انتقل إلى *English with Lucy* و *Oxford Online English* و *Learn English with TV Series*\n4️⃣ إذا كان هدفك العمل، ركز على *Business English Pod* و *Business English with Christina*\n5️⃣ للمستوى المتقدم، تابع *TED* و *Harvard Business Review* و *Stanford GSB*"
    }
}

CAT1_ORDER = ["entrepreneurship", "ecommerce", "digital_marketing", "ai", "programming", "graphic_design", "video_editing", "content_creation", "freelancing", "sales", "personal_finance", "english", "german"]

# ============================================================
#  BOT 2 DATA  (library)
# ============================================================

CAT2 = {
    "english": {
        "name_ar": "📚 اللغة الإنجليزية",
        "name_en": "📚 English Books",
        "books": [
            {"title": "Dictionary", "description": "قاموس إنجليزي-عربي شامل — يحتوي على آلاف الكلمات مع النطق والترجمة.", "url": "https://example.com/dictionary.pdf"},
            {"title": "Grammar", "description": "قواعد اللغة الإنجليزية كاملة — شرح مبسط لجميع القواعد مع تمارين تطبيقية.", "url": "https://example.com/grammar.pdf"},
            {"title": "IELTS", "description": "دليل اختبار IELTS — نصائح واستراتيجيات للتحضير للامتحان.", "url": "https://example.com/ielts.pdf"},
            {"title": "1000 فعل إنجليزي مستخدم في حياتنا اليومية", "description": "أكثر 1000 فعل استخداماً في اللغة الإنجليزية مع الترجمة والنطق.", "url": "https://example.com/1000-verbs.pdf"},
            {"title": "موسوعة الشامل في تعليم اللغة الإنجليزية", "description": "دليل شامل من الصفر إلى الاحتراف — قواعد، مفردات، محادثة.", "url": "https://example.com/mawsoa.pdf"}
        ]
    },
    "entrepreneurship": {
        "name_ar": "🚀 ريادة الأعمال",
        "name_en": "🚀 Entrepreneurship",
        "books": [
            {"title": "كيف تصبح قائداً استراتيجياً", "description": "دليل شامل لتطوير مهارات القيادة الاستراتيجية واتخاذ القرارات الحاسمة في عالم الأعمال.", "url": "https://drive.google.com/uc?export=download&id=1rKdXUFd_iWaohghOHGg3gA_-XdA-ymk1"},
            {"title": "كيف تصبح مديراً عاماً", "description": "خطوات عملية للانتقال من مدير تنفيذي إلى مدير عام ناجح يدير الفرق والمشاريع بكفاءة.", "url": "https://example.com/general-manager.pdf"},
            {"title": "المهارات الإدارية ومهارة التعامل مع الآخرين", "description": "أساسيات الإدارة الحديثة ومهارات التواصل الفعال مع الزملاء والمرؤوسين والعملاء.", "url": "https://example.com/management-skills.pdf"},
            {"title": "فن اختيار أفضل الموظفين", "description": "استراتيجيات توظيف ذكية — كيف تختار الشخص المناسب للوظيفة المناسبة.", "url": "https://example.com/hiring.pdf"},
            {"title": "التفكير المستقبلي", "description": "منهجيات التخطيط الاستراتيجي والتفكير طويل المدى لبناء مستقبل مؤسستك.", "url": "https://example.com/future-thinking.pdf"}
        ]
    },
    "german": {
        "name_ar": "🇩🇪 اللغة الألمانية",
        "name_en": "🇩🇪 German",
        "books": [
            {"title": "تعلم اللغة الألمانية", "description": "كتاب شامل لتعلم اللغة الألمانية من الصفر — يغطي الأساسيات والمفردات اليومية.", "url": "https://example.com/german-1.pdf"},
            {"title": "اللغة الألمانية", "description": "مرجع متكامل لتعلم اللغة الألمانية — قواعد، محادثة، ونطق.", "url": "https://example.com/german-2.pdf"},
            {"title": "قواعد اللغة الألمانية للمبتدئين والمتقدم", "description": "شرح كامل لقواعد اللغة الألمانية يناسب جميع المستويات — من المبتدئ إلى المتقدم.", "url": "https://example.com/german-grammar.pdf"},
            {"title": "أدوات الاستفهام في اللغة الألمانية", "description": "دروس وأمثلة حول أدوات الاستفهام واستخداماتها في اللغة الألمانية.", "url": "https://example.com/german-question.pdf"},
            {"title": "كورس تعلم اللغة الألمانية", "description": "دورة متكاملة لتعلم اللغة الألمانية — دروس مرتبة ومتسلسلة من البداية إلى الاحتراف.", "url": "https://example.com/german-course.pdf"}
        ]
    },
    "digital_marketing": {
        "name_ar": "📈 التسويق الرقمي",
        "name_en": "📈 Digital Marketing",
        "books": [
            {"title": "الدليل الاحترافي لاستراتيجية التسويق الرقمي", "description": "دليل متكامل لوضع وتنفيذ استراتيجيات التسويق الرقمي الناجحة.", "url": "https://example.com/digital-strategy.pdf"},
            {"title": "التسويق عبر الإنترنت", "description": "أساسيات التسويق الإلكتروني وأفضل الممارسات للوصول إلى الجمهور المستهدف.", "url": "https://example.com/online-marketing.pdf"},
            {"title": "احترف التسويق الإلكتروني", "description": "دورات متقدمة في التسويق الإلكتروني — من المبتدئ إلى الاحتراف.", "url": "https://example.com/master-e-marketing.pdf"},
            {"title": "استراتيجية التسويق الإلكتروني", "description": "خطط واستراتيجيات فعالة لتنمية الأعمال عبر القنوات الرقمية.", "url": "https://example.com/e-marketing-strategy.pdf"},
            {"title": "فن التسويق في المشاريع الصغيرة", "description": "أساليب تسويقية مبتكرة ومناسبة للمشاريع الصغيرة بميزانية محدودة.", "url": "https://example.com/small-business-marketing.pdf"}
        ]
    },
    "personal_finance": {
        "name_ar": "💰 التمويل الشخصي والاستثمار",
        "name_en": "💰 Personal Finance & Investment",
        "books": [
            {"title": "أغنى رجل في بابل", "description": "كتاب كلاسيكي عن أساسيات إدارة المال والتوفير والاستثمار — دروس من حضارة بابل القديمة.", "url": "https://example.com/richest-man-in-babylon.pdf"},
            {"title": "تحويل الابتكار إلى أموال", "description": "كيف تحول أفكارك الإبداعية إلى مصادر دخل حقيقية — استراتيجيات monetizing الابتكار.", "url": "https://example.com/innovation-to-money.pdf"},
            {"title": "اصنع المزيد من المال", "description": "طرق عملية لزيادة دخلك وبناء ثروة — من التوفير إلى الاستثمار الذكي.", "url": "https://example.com/make-more-money.pdf"},
            {"title": "ابنِ عضلاتك المالية", "description": "تمرينات مالية لتعزيز صحتك المالية — بناء عادات مالية قوية ومتينة.", "url": "https://example.com/financial-muscles.pdf"},
            {"title": "البيع على طريقة الأذكياء", "description": "استراتيجيات بيع ذكية ومبتكرة — كيف تبيع بفعالية وتحقق أرباحاً أعلى.", "url": "https://example.com/smart-selling.pdf"}
        ]
    },
    "ai": {
        "name_ar": "🤖 الذكاء الاصطناعي",
        "name_en": "🤖 Artificial Intelligence",
        "books": [
            {"title": "تعلم الذكاء الاصطناعي", "description": "دليل شامل لتعلم أساسيات الذكاء الاصطناعي — من المفاهيم إلى التطبيقات العملية.", "url": "https://example.com/learn-ai.pdf"},
            {"title": "نموذج الذكاء الاصطناعي ChatGPT", "description": "شرح كامل لنموذج ChatGPT — كيفية استخدامه وتوظيفه في العمل والحياة اليومية.", "url": "https://example.com/chatgpt-model.pdf"}
        ]
    },
    "freelancing": {
        "name_ar": "💼 العمل الحر",
        "name_en": "💼 Freelancing",
        "books": [
            {"title": "الأب الغني والأب الفقير", "description": "كتاب تحويلي عن الفروقات في tư duy المال بين الأغنياء والفقراء — دروس أساسي عن الحرية المالية.", "url": "https://example.com/rich-dad-poor-dad.pdf"},
            {"title": "دليل الاستثمار للأب الغني", "description": "استراتيجيات استثمار متقدمة من سلسلة الأب الغني — كيف تبني ثروة عبر الاستثمار الذكي.", "url": "https://example.com/rich-dad-guide-investing.pdf"},
            {"title": "فكر وازدد ثراء", "description": "كتاب كلاسيكي عن قوة التفكير الإيجابي ودوره في بناء الثروة — من نابليون هيل.", "url": "https://example.com/think-and-grow-rich.pdf"},
            {"title": "سيكولوجية المال", "description": "فهم كيف يؤثر تفكيرنا وسلوكنا على قراراتنا المالية — دروس من مورغان هاوسل.", "url": "https://example.com/psychology-of-money.pdf"}
        ]
    },
    "sales": {
        "name_ar": "🛒 المبيعات",
        "name_en": "🛒 Sales",
        "books": [
            {"title": "أسرار المبيعات", "description": "أسرار وتقنيات مخفية يستخدمها أفضل مندوبي المبيعات للفوز بالصفقات وزيادة الأرباح.", "url": "https://example.com/sales-secrets.pdf"},
            {"title": "المبيعات العملاقة", "description": "استراتيجيات متقدمة لتنمية المبيعات وتحقيق أرقام قياسية في الإيرادات.", "url": "https://example.com/big-sales.pdf"},
            {"title": "151 فكرة سريعة لزيادة المبيعات", "description": "مجموعة من أفكار عملية وسريعة التطبيق لرفع المبيعات وتحسين الأداء التجاري.", "url": "https://example.com/151-sales-ideas.pdf"},
            {"title": "دراسة السوق", "description": "كيف تحلل السوق وتفهم احتياجات العملاء لتطوير استراتيجيات بيع فعالة.", "url": "https://example.com/market-study.pdf"}
        ]
    },
    "mindset": {
        "name_ar": "🧠 عقليتك",
        "name_en": "🧠 Your Mindset",
        "books": [
            {"title": "قوة عقلك الباطن", "description": "اكتشف القوة الهائلة المخفية في عقلك الباطن — كيف تستخدمها لتحقيق أهدافك وطموحاتك.", "url": "https://example.com/power-subconscious-mind.pdf"},
            {"title": "العادات الذرية", "description": "كيف تبني عادات إيجابية صغيرة تحقق نتائج كبيرة — دليل جيمس كلير للتغيير الفعال.", "url": "https://example.com/atomic-habits.pdf"},
            {"title": "إعادة ضبط شغفك", "description": "كيف تستعيد حماسك وشغفك بالحياة والعمل — خطوات عملية لإعادة التصميم الداخلي.", "url": "https://example.com/reset-passion.pdf"},
            {"title": "العقل المدبر", "description": "فهم كيف يعمل عقلك وكيف تتحكم في أفكارك — أساليب ذكية لإدارة العقل والمشاعر.", "url": "https://example.com/intelligent-mind.pdf"},
            {"title": "النجاح هو لك", "description": "دليل عملي لبناء الثقة بالنفس وتحقيق النجاح في جميع جوانب الحياة.", "url": "https://example.com/success-is-yours.pdf"}
        ]
    },
    "investment": {
        "name_ar": "📈 الاستثمار",
        "name_en": "📈 Investment",
        "books": [
            {"title": "المستثمر الذكي", "description": "الكتاب المرجعي الأول عالمياً في الاستثمار من تأليف بنجامين غراهام — أساسيات الاستثمار القائم على القيمة والتحليل المالي.", "url": "https://example.com/intelligent-investor.pdf"},
            {"title": "الميليونير الفوري", "description": "قصة ملهمة عن رجل يتحول إلى مليونير بين عشية وضحاها — أسرار العقلية المالية والنجاح من تأليف مارك فيكتور هانسن وروبرت ألن.", "url": "https://example.com/instant-millionaire.pdf"},
            {"title": "دراسة السوق", "description": "كيف تحلل السوق وتحدد الفرص الاستثمارية — فهم المنافسين والعرض والطلب قبل اتخاذ أي قرار استثماري.", "url": "https://example.com/market-analysis.pdf"},
            {"title": "اجتذاب العملاء", "description": "استراتيجيات عملية لجذب العملاء الجدد والاحتفاظ بهم — بناء قاعدة عملاء قوية لتنمية استثمارك وأعمالك.", "url": "https://example.com/customer-acquisition.pdf"}
        ]
    },
    "islamic": {
        "name_ar": "🕌 الكتب الإسلامية",
        "name_en": "🕌 Islamic Books",
        "books": [
            {"title": "كتب الحديث الستة", "description": "مجموعة الكتب الستة المعتمدة في الحديث النبوي — صحيح البخاري، صحيح مسلم، سنن أبي داود، سنن الترمذي، سنن النسائي، وسنن ابن ماجه.", "url": "https://example.com/six-books-of-hadith.pdf"},
            {"title": "مؤلفات ابن تيمية", "description": "مختارات من أهم كتب شيخ الإسلام ابن تيمية في العقيدة والفقه والتفسير — مثل العقيدة الواسطية ومنهاج السنة النبوية.", "url": "https://example.com/ibn-taymiyyah.pdf"},
            {"title": "مؤلفات ابن قيم الجوزية", "description": "روائع الإمام ابن قيم الجوزية — مثل زاد المعاد والفوائد وكتاب الروح.", "url": "https://example.com/ibn-al-qayyim.pdf"},
            {"title": "مؤلفات ابن الجوزي", "description": "من أهم كتب الإمام ابن الجوزي — مثل صيد الخاطر وتلبيس إبليس وبستان الواعظين.", "url": "https://example.com/ibn-al-jawzi.pdf"},
            {"title": "مؤلفات ابن عثيمين", "description": "شروحات وكتب الشيخ محمد بن صالح العثيمين — مثل شرح الأصول الثلاثة وشرح العقيدة الواسطية.", "url": "https://example.com/ibn-uthaymeen.pdf"}
        ]
    },
    "personality": {
        "name_ar": "🌱 ابني شخصيتك",
        "name_en": "🌱 Build Your Personality",
        "books": [
            {"title": "القوة الهادئة", "description": "كتاب عن قوة الشخصيات الهادئة وكيف تحوّل هدوءك إلى ميزة في الحياة والعمل.", "url": "https://example.com/quiet-power.pdf"},
            {"title": "انت قوة مذهلة", "description": "دليل عملي لاكتشاف قوتك الداخلية وبناء ثقة مطلقة بنفسك وتحقيق أهدافك.", "url": "https://example.com/you-are-a-badass.pdf"},
            {"title": "بسط حياتك", "description": "كيف تتخلص من الفوضى والتعقيد وتعيش حياة أبسط وأكثر تركيزاً.", "url": "https://example.com/simplify-your-life.pdf"},
            {"title": "كيف تقطع علاقتك بهاتفك", "description": "خطوات عملية لتقليل استخدام الهاتف والعودة إلى الحياة الحقيقية.", "url": "https://example.com/break-up-with-phone.pdf"},
            {"title": "7 شخصيات تسمم حياتكم", "description": "تعرّف على الشخصيات السامة التي تستنزف طاقتك وكيف تحمي نفسك منها.", "url": "https://example.com/7-toxic-personalities.pdf"}
        ]
    },
    "energy": {
        "name_ar": "⚡ اشحن طاقتك",
        "name_en": "⚡ Charge Your Energy",
        "books": [
            {"title": "حافلة الطاقة", "description": "قصة ملهمة عن قيادة الطاقة الإيجابية في العمل والحياة من تأليف جون غوردون.", "url": "https://example.com/energy-bus.pdf"},
            {"title": "تغلب على الاكتئاب بسرعة", "description": "استراتيجيات عملية للتخلص من الاكتئاب واستعادة التوازن النفسي.", "url": "https://example.com/overcome-depression.pdf"},
            {"title": "ذاكرة مثالية", "description": "تقنيات عملية لتقوية الذاكرة والحفظ السريع.", "url": "https://example.com/perfect-memory.pdf"},
            {"title": "مشاعرك قد تكون قاتلة", "description": "فهم خطورة المشاعر السلبية على صحتك وكيف تتحكم بها قبل أن تتحكم بك.", "url": "https://example.com/your-emotions.pdf"},
            {"title": "من الصفر", "description": "دليل عملي لبدء حياة جديدة من الصفر وبناء مستقبل أفضل.", "url": "https://example.com/from-scratch.pdf"}
        ]
    }
}

CAT2_ORDER = ["english", "entrepreneurship", "german", "digital_marketing", "personal_finance", "investment", "ai", "freelancing", "sales", "mindset", "islamic", "personality", "energy"]

# ============================================================
#  BOT 1 HANDLERS  (channels)
# ============================================================

router1 = Router()

def reply_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📋 القائمة الرئيسية")]],
        resize_keyboard=True
    )
    return kb

def main_keyboard1():
    kb = InlineKeyboardBuilder()
    for key in CAT1_ORDER:
        cat = CAT1[key]
        kb.button(text=cat["name_ar"], callback_data=f"cat_{key}")
    kb.adjust(2)
    return kb.as_markup()

@router1.message(Command("start"), F.chat.type == "private")
async def cmd_start1(msg: Message):
    await msg.answer("📱 *اختر مجالك:*\n", reply_markup=main_keyboard1())

@router1.message(Command("help"), F.chat.type == "private")
async def cmd_help1(msg: Message):
    await msg.answer("🎓 *Mindset Learning Channels*\n\nالأمر /start — عرض القائمة الرئيسية\nالأمر /help — هذه المساعدة\n\nاختر مجالاً وستظهر لك القنوات مرتبة حسب المستوى.", reply_markup=reply_menu())

@router1.message(F.text == "📋 القائمة الرئيسية", F.chat.type == "private")
async def menu_button1(msg: Message):
    await msg.answer("📱 *اختر مجالك:*\n", reply_markup=main_keyboard1())

@router1.message(F.chat.type == "private")
async def any_message1(msg: Message):
    await msg.answer("📱 *اختر مجالك:*\n", reply_markup=main_keyboard1())

@router1.callback_query(F.data == "main_menu")
async def cb_main_menu1(cq: CallbackQuery):
    await cq.message.edit_text("📱 *اختر مجالك:*", reply_markup=main_keyboard1())

@router1.callback_query(F.data.startswith("cat_"))
async def cb_show_channels(cq: CallbackQuery):
    cat_key = cq.data[4:]
    if cat_key not in CAT1:
        await cq.answer("القسم غير موجود", show_alert=True)
        return
    cat = CAT1[cat_key]
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

@router1.callback_query(F.data.startswith("top_"))
async def cb_top_picks1(cq: CallbackQuery):
    cat_key = cq.data[4:]
    cat = CAT1[cat_key]
    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 الرجوع للقنوات", callback_data=f"cat_{cat_key}")
    kb.button(text="🏠 القائمة الرئيسية", callback_data="main_menu")
    kb.adjust(1)
    await cq.message.edit_text(
        f"🏆 *أفضل الاختيارات*\n{cat['top_picks']}",
        parse_mode="Markdown",
        reply_markup=kb.as_markup()
    )

@router1.callback_query(F.data.startswith("ext_"))
async def cb_extra1(cq: CallbackQuery):
    cat_key = cq.data[4:]
    cat = CAT1[cat_key]
    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 الرجوع للقنوات", callback_data=f"cat_{cat_key}")
    kb.button(text="🏠 القائمة الرئيسية", callback_data="main_menu")
    kb.adjust(1)
    await cq.message.edit_text(
        f"📚 *مصادر إضافية*\n{cat['extra_resources']}",
        parse_mode="Markdown",
        reply_markup=kb.as_markup()
    )

@router1.callback_query(F.data.startswith("ch_"))
async def cb_show_channel1(cq: CallbackQuery):
    rest = cq.data[3:]
    idx_str, cat_key = rest.split("_", 1)
    idx = int(idx_str)
    if cat_key not in CAT1:
        await cq.answer("القسم غير موجود", show_alert=True)
        return
    cat = CAT1[cat_key]
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

# ============================================================
#  BOT 2 HANDLERS  (library)
# ============================================================

router2 = Router()

REGISTERED_FILES = {}

def main_keyboard2():
    kb = InlineKeyboardBuilder()
    for key in CAT2_ORDER:
        cat = CAT2[key]
        kb.button(text=cat["name_ar"], callback_data=f"cat_{key}")
    kb.adjust(2)
    return kb.as_markup()

def library_welcome_text():
    return (
        "📚 *Mindset Library*\n\n"
        "أفضل الكتب لتنمية مهاراتك وتطوير نفسك\n\n"
        "اختر مجالًا وستظهر لك أفضل الكتب فيه 👇"
    )

@router2.message(Command("start"), F.chat.type == "private")
async def cmd_start2(msg: Message):
    await msg.answer(library_welcome_text(), reply_markup=main_keyboard2())

@router2.message(Command("help"), F.chat.type == "private")
async def cmd_help2(msg: Message):
    await msg.answer("📚 *Mindset Library*\n\n/start — عرض القائمة الرئيسية\n/help — هذه المساعدة\n\nاختر مجالاً، ثم كتاباً لقراءة الوصف وتحميل PDF.", reply_markup=reply_menu())

@router2.message(F.text == "📋 القائمة الرئيسية", F.chat.type == "private")
async def menu_button2(msg: Message):
    await msg.answer(library_welcome_text(), reply_markup=main_keyboard2())

@router2.message(Command("files"), F.chat.type == "private")
async def cmd_files(msg: Message):
    if not REGISTERED_FILES:
        await msg.answer("لا توجد ملفات مسجلة بعد. أرسل الكتب كملفات PDF وسيتم حفظها تلقائياً.")
        return
    lines = [f"{i+1}. `{name}`\n   `{fid}`" for i, (name, fid) in enumerate(REGISTERED_FILES.items())]
    await msg.answer("📚 *الملفات المسجلة:*\n\n" + "\n".join(lines))

@router2.message(F.document, F.chat.type == "private")
async def collect_document(msg: Message):
    doc = msg.document
    fid = doc.file_id
    fname = doc.file_name or "ملف"
    REGISTERED_FILES[fname] = fid
    await msg.answer(
        f"📁 *تم استلام الملف:* `{fname}`\n"
        f"`file_id: {fid}`\n\n"
        f"اكتب /files لعرض جميع الملفات المسجلة."
    )

@router2.message(F.chat.type == "private")
async def any_message2(msg: Message):
    await msg.answer(library_welcome_text(), reply_markup=main_keyboard2())

@router2.callback_query(F.data == "main_menu")
async def cb_main_menu2(cq: CallbackQuery):
    await cq.message.edit_text("📱 *اختر مجالك:*", reply_markup=main_keyboard2())

@router2.callback_query(F.data.startswith("cat_"))
async def cb_show_books(cq: CallbackQuery):
    cat_key = cq.data[4:]
    if cat_key not in CAT2:
        await cq.answer("القسم غير موجود", show_alert=True)
        return
    cat = CAT2[cat_key]
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

@router2.callback_query(F.data.startswith("bk_"))
async def cb_show_book(cq: CallbackQuery):
    rest = cq.data[3:]
    cat_key, idx_str = rest.rsplit("_", 1)
    idx = int(idx_str)
    if cat_key not in CAT2:
        await cq.answer("القسم غير موجود", show_alert=True)
        return
    books = CAT2[cat_key]["books"]
    if idx >= len(books):
        await cq.answer("الكتاب غير موجود", show_alert=True)
        return
    book = books[idx]
    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 رجوع للكتب", callback_data=f"cat_{cat_key}")
    kb.button(text="🏠 القائمة الرئيسية", callback_data="main_menu")
    kb.adjust(1)
    if book.get("file_id"):
        text = (
            f"📖 *{book['title']}*\n\n"
            f"{book['description']}"
        )
        await cq.message.edit_text(text, parse_mode="Markdown", reply_markup=kb.as_markup())
        await cq.message.answer_document(book["file_id"], caption=f"📖 {book['title']}")
    else:
        text = (
            f"📖 *{book['title']}*\n\n"
            f"{book['description']}\n\n"
            f"🔗 [اضغط هنا لتحميل PDF]({book['url']})"
        )
        await cq.message.edit_text(text, parse_mode="Markdown", reply_markup=kb.as_markup(), disable_web_page_preview=False)

# ============================================================
#  HEALTH SERVER + MAIN
# ============================================================

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        pass

def start_health_server():
    port = int(os.getenv("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logging.info(f"Health server listening on port {port}")

async def run_polling(name, bot, dp):
    while True:
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)
        except Exception as e:
            logging.error(f"[{name}] connection error: {e}, retrying in 15s")
        await asyncio.sleep(15)

async def main():
    token1 = os.getenv("BOT_TOKEN")
    token2 = os.getenv("BOT_TOKEN_2")
    if not token1:
        raise RuntimeError("BOT_TOKEN environment variable is not set")
    if not token2:
        raise RuntimeError("BOT_TOKEN_2 environment variable is not set")

    bot1 = Bot(token=token1, default=DefaultBotProperties(parse_mode="Markdown"))
    dp1 = Dispatcher()
    dp1.include_router(router1)

    bot2 = Bot(token=token2, default=DefaultBotProperties(parse_mode="Markdown"))
    dp2 = Dispatcher()
    dp2.include_router(router2)

    logging.info("Starting both bots")
    await asyncio.gather(
        run_polling("bot1_channels", bot1, dp1),
        run_polling("bot2_library", bot2, dp2),
    )

if __name__ == "__main__":
    try:
        start_health_server()
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Cloud supervisor stopped")
