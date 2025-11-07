import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew
import os
from utils import get_openai_api_key 

# OpenAI API kalitini olish
openai_api_key = get_openai_api_key()

# Muhit o'zgaruvchisini o'rnatish
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini" 

# Hozircha test uchun chiqish
# print("CrewAI muhit sozlandi! Model:", os.environ["OPENAI_MODEL_NAME"])

planner = Agent(
    role="Kontent rejalovchi",
    goal="Berilgan {topic} mavzusida qiziqarli va faktlarga asoslangan kontent rejasini tuzish.",
    backstory=(
        "Siz blog maqolasi uchun reja tayyorlayotgan tajribali kontent rejalovchisiz. "
        "Mavzu: {topic}. "
        "Siz auditoriyaga foydali va to‘g‘ri ma’lumot berishga yordam beradigan faktlarni yig‘asiz. "
        "Sizning ishingiz o‘quvchilarga mavzuni yaxshiroq tushunishga, "
        "va to‘g‘ri qaror qabul qilishlariga yordam beradi. "
        "Siz tayyorlagan reja keyinchalik kontent yozuvchi tomonidan maqola yozishda asos sifatida ishlatiladi."
    ),
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role="Kontent Yozuvchisi",
    goal="Mavzu: {topic} bo‘yicha chuqur va faktlarga asoslangan fikriy maqola yozish",
    backstory=(
        "Siz yangi fikriy maqola yozayotgan Kontent Yozuvchisi sifatida ishlayapsiz. "
        "Sizning yozuvingiz Content Planner (Kontent Rejalashtiruvchisi) tomonidan taqdim etilgan reja va mavzu bo‘yicha tegishli ma’lumotlarga asoslanadi. "
        "Siz reja bo‘yicha asosiy maqsadlar va yo‘nalishlarni bajarishingiz kerak. "
        "Shuningdek, siz ob’ektiv va tarafkash bo‘lmagan fikrlarni taqdim etasiz va ularni Content Planner tomonidan berilgan ma’lumotlar bilan qo‘llab-quvvatlaysiz. "
        "Maqolangizda qachon fikringiz shaxsiy bo‘lsa va qachon ob’ektiv ma’lumotlarga asoslangan bo‘lsa, bu farqni aniq ko‘rsatishingiz kerak."
        ),
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    role="Tahrirchi",
    goal="Berilgan blog postni tahrir qilish va uni tashkilotning yozish uslubiga moslashtirish",
    backstory=(
        "Siz Content Writer (Kontent Yozuvchisi) tomonidan yuborilgan blog postni oladigan Tahrirchisiz. "
        "Sizning maqsadingiz blog postni ko‘rib chiqish va quyidagilarni ta’minlashdir: "
        "u jurnalistik eng yaxshi amaliyotlarga rioya qiladi, "
        "fikr yoki bayonotlarni taqdim etishda muvozanatli nuqtai nazarni saqlaydi, "
        "va imkon qadar katta bahsli mavzular yoki shaxsiy fikrlarni oldini oladi."
    ),
    allow_delegation=False,
    verbose=True
)

plan = Task(
    description=(
        "1. {topic} bo‘yicha so‘nggi trendlar, asosiy ishtirokchilar va e’tiborga molik yangiliklarni ustuvor qilish.\n"
        "2. Maqsadli auditoriyani aniqlash, ularning qiziqishlari va muammolarini hisobga olish.\n"
        "3. Kirish qismi, asosiy nuqtalar va harakatga chaqiriq (call to action)ni o‘z ichiga olgan batafsil kontent rejasi tuzish.\n"
        "4. SEO kalit so‘zlar va tegishli ma’lumotlar yoki manbalarni qo‘shish."
    ),
    expected_output=(
        "Maqsadli auditoriya tahlili, kontent rejasi, "
        "SEO kalit so‘zlar va manbalarni o‘z ichiga olgan "
        "to‘liq kontent reja hujjati"
    ),
    agent=planner,
)

write = Task(
    description=(
        "1. Kontent rejasidan foydalanib {topic} bo‘yicha qiziqarli blog post yozish.\n"
        "2. SEO kalit so‘zlarni tabiiy tarzda qo‘shish.\n"
        "3. Bo‘limlar va kichik sarlavhalar qiziqarli va mazmunli nomlanishi.\n"
        "4. Postni jozibali kirish qismi, tushunarli asosiy qismi va xulosaviy yakun bilan tuzilganligiga ishonch hosil qilish.\n"
        "5. Imlo va grammatik xatolarni tekshirish hamda brend ovozi bilan mosligini ta’minlash."
    ),
    expected_output=(
        "Markdown formatida tayyorlangan, nashrga tayyor, har bir bo‘limida 2–3 paragraf bo‘lgan yaxshi yozilgan blog post"
    ),
    agent=writer
)

edit = Task(
    description=(
        "Berilgan blog postni imlo va grammatik xatolar uchun tekshirish, "
        "shuningdek, uning brend ovozi bilan mosligini ta’minlash."
    ),
    expected_output=(
        "Markdown formatida tayyorlangan, nashrga tayyor, har bir bo‘limida 2–3 paragraf bo‘lgan yaxshi yozilgan blog post"
    ),
    agent=editor
)

crew = Crew(
    agents=[planner,writer,editor],
    tasks=[plan,write,edit],
    verbose=True
)

result = crew.kickoff(inputs={"topic":"Suniy intellekt"})