import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import textwrap
import io

# Meme captions dataset organized by category
CAPTION_CATEGORIES = {
    "Exams/College": [
        "Exams tomorrow, but I only know HTML 😂",
        "When teacher says exam is tomorrow 😱📚",
        "Me trying to remember what I studied at 2 AM before exam 🤯📚",
        "When you realize the assignment was due yesterday 😬",
        "When you see marks after exam results 😳",
        "When you finish all assignments at 3AM 😴📚",
        "When you get extra marks for no reason 😎",
        "When you see your exam timetable 😱📅",
        "When you pretend to understand in class but you're lost 🤔",
        "When you wake up and realize you overslept for class 😱",
        "When you open the book and sleep attacks you immediately 😴📖",
        "When you study all night and exam paper is from another planet 👽📚",
        "When you write 'see next page' and there is no next page 😅",
        "When you realize you prepared for the wrong subject 😭",
        "When you see your friend confidently writing in the exam and you panic 😨",
        "When you ask for extra sheet just to look smart 😎📝",
        "When you and your friend both fail but celebrate together 😂",
    ],
    "Food": [
        "Me opening fridge every 5 minutes 🍔🥤",
        "When you try to eat healthy but pizza calls your name 🍕😂",
        "When you realize biryani is over 😭🍚",
        "When your friend eats your food without asking 😤",
        "When you open the fridge and forget why you came 😅🥶",
        "When you try to diet but see ice cream 🍦😅",
        "When you hear 'free food' in college 🍕",
        "When you order salad but eat your friend's fries 🍟😜",
        "When mom says 'food is ready' and you run like Usain Bolt 🏃‍♂️🍲",
        "When you see samosas in the canteen 😍🥟",
        "When you eat Maggi at 2AM and feel like a chef 👨‍🍳🍜",
        "When you say 'last piece' but eat three more 😂",
    ],
    "Tech/Struggles": [
        "When WiFi goes down during submission 😭📶",
        "When you finally get WiFi after hours of struggle 🙌📶",
        "When your code works on the first try 😎",
        "When you get caught using your phone in class 📱😳",
        "When you realize you sent the message to the wrong group 😱",
        "When you finally understand a meme after 5 minutes 🤔😂",
        "When you get a call from an unknown number 📞😬",
        "When you try to act busy but have nothing to do 😅",
        "When you fix one bug and three more appear 🐞🐞🐞",
        "When you Google the error and find your own question from last year 😅",
        "When you forget to save and your laptop crashes 😭💻",
        "When you say 'it works on my machine' 😏",
        "When you join a Zoom call and forget the camera is on 😳",
    ],
    "Relationships/Friends": [
        "When you see your crush online but can't say hi 😅",
        "When you send a risky text and see 'typing...' 👀",
        "When you see your crush with someone else 💔😢",
        "When you get a like from your crush on Instagram 😍",
        "When you laugh at your own joke because no one else did 🤣",
        "When you try to act cool but trip in front of everyone 😅",
        "When you finally find your lost pen 🖊️🥳",
        "When you see your old school photos 😂",
        "When your friend says 'I'll be there in 5 minutes' and comes after 1 hour ⏰😂",
        "When you and your bestie laugh at something nobody else gets 🤪",
        "When your friend eats your lunch and says 'just a bite' 😒",
        "When you both get scolded and blame each other 😆",
        "When you and your friend make eye contact in class and start laughing for no reason 🤭",
    ],
    "Telugu Movie": [
        "Em jarigindante... chala jarigindi! 😅",
        "Nenu local! 😎",
        "Evadu kodithe dimma tirigi mind block avuthundo aade pandu gaadu! 💥",
        "Naku konchem tikkundi, kani daniki okka lekkundi! 🤪",
        "Okkasari commit aithe na mata nene vinanu! 🔥",
        "Cheppanu brother! 😏",
        "Life ante oka chota nilabadadam kaadu, munduku velladam! 🚶‍♂️",
        "Nenu single, ante powerful! 💪",
        "Aithey ok! 😁",
        "Nuvvu leka nenu leka, ee world lo evaru leka! 🌎",
        "Nenu eppudu chesina correct gaane chestha! 😁",
        "Andaru chesaru, nenu kuda chesanu! 😜",
        "Nenu ready, meeru ready ah? 🤔",
        "Nuvvu chesina paniki nenu answer ivvalenu! 🙅‍♂️",
        "Nenu chesina tappu correct cheyyalenu! 😅",
        "Ee roju manaki festival! 🥳",
        "Naku ardham kaledu, kani chala bagundi! 😂",
        "Nuvvu chesina joke ki navvadaniki nenu ready! 😆",
        "Nenu chala busy, please disturb cheyyakandi! 🚫",
        "Ee photo chusi naku memory flashback! 🧠",
        "Nenu meme king! 👑",
        "Nuvvu meme queen! 👸",
        "Nenu eppudu padukuntanu, lekapote padukuntanu! 😴",
        "Nenu chesina meme, meeru enjoy cheyyandi! 😁",
        "Ee meme chusi andaru navvali! 😂",
        "Nuvvu chesina paniki naku navvu vastundi! 😆",
        "Nenu chesina joke ki andaru navvali! 😁",
        "Nenu chesina plan ki andaru shock! 😲",
        "Nenu chesina work ki andaru appreciate chestaru! 👏",
        "Nenu chesina dance ki andaru wow antaru! 💃",
        "Nenu chesina photo ki andaru like vestaru! 👍",
        "Nenu chesina prank ki andaru confuse! 😜",
        "Nenu vadalanu, vadalanu, vadalanu! 😤",
        "Nenu eppudu fail avvanu! 💪",
        "Nenu chesina mistake ki sorry cheppanu! 😅",
        "Nenu chesina paniki explanation ivvanu! 😏",
        "Nenu chesina meme ki copyright undadu! 😂",
        "Nenu chesina joke ki punch undali! 🥊",
        "Nenu chesina photo ki filter undali! 😎",
        "Nenu chesina plan ki backup undali! 📝",
        "Nenu chesina meme ki viral avvali! 🌐",
        "Nenu chesina dance ki steps undali! 💃",
        "Nenu chesina prank ki twist undali! 😜",
        "Nenu chesina selfie ki angle undali! 🤳",
        "Nenu chesina story ki suspense undali! 😲",
        "Nenu chesina reply ki timing undali! ⏰",
        "Nenu chesina comment ki like ravali! 👍",
        "Nenu chesina status ki views ravali! 👀",
        "Nenu chesina call ki answer ravali! 📞",
        "Nenu chesina message ki reply ravali! 💬",
        "Nenu chesina meme ki share ravali! 🔄",
        # More Telugu viral/funny lines
        "Aithey ok! 😁",
        "Nenu eppudu padukuntanu, lekapote padukuntanu! 😴",
        "Nenu chesina meme, meeru enjoy cheyyandi! 😁",
        "Ee meme chusi andaru navvali! 😂",
        "Nuvvu chesina paniki naku navvu vastundi! 😆",
        "Nenu chesina joke ki andaru navvali! 😁",
        "Nenu chesina plan ki andaru shock! 😲",
        "Nenu chesina work ki andaru appreciate chestaru! 👏",
        "Nenu chesina dance ki andaru wow antaru! 💃",
        "Nenu chesina photo ki andaru like vestaru! 👍",
        "Nenu chesina prank ki andaru confuse! 😜",
        "Nenu vadalanu, vadalanu, vadalanu! 😤",
        "Nenu eppudu fail avvanu! 💪",
        "Nenu chesina mistake ki sorry cheppanu! 😅",
        "Nenu chesina paniki explanation ivvanu! 😏",
        "Nenu chesina meme ki copyright undadu! 😂",
        "Nenu chesina joke ki punch undali! 🥊",
        "Nenu chesina photo ki filter undali! 😎",
        "Nenu chesina plan ki backup undali! 📝",
        "Nenu chesina meme ki viral avvali! 🌐",
        "Nenu chesina dance ki steps undali! 💃",
        "Nenu chesina prank ki twist undali! 😜",
        "Nenu chesina selfie ki angle undali! 🤳",
        "Nenu chesina story ki suspense undali! 😲",
        "Nenu chesina reply ki timing undali! ⏰",
        "Nenu chesina comment ki like ravali! 👍",
        "Nenu chesina status ki views ravali! 👀",
        "Nenu chesina call ki answer ravali! 📞",
        "Nenu chesina message ki reply ravali! 💬",
        "Nenu chesina meme ki share ravali! 🔄",
        "Nenu chesina meme ki Oscar ravali! 🏆",
        "Nenu chesina meme ki punch undali! 😁",
        "Nenu chesina meme ki andaru navvali! 😂",
        "Nenu chesina meme ki like ravali! 👍",
        "Nenu chesina meme ki viral avvali! 🌐",
        "Nenu chesina meme ki share ravali! 🔄",
        "Nenu chesina meme ki status ravali! 👀",
        "Nenu chesina meme ki comment ravali! 💬",
        "Nenu chesina meme ki reply ravali! ⏰",
        "Nenu chesina meme ki answer ravali! 📞",
        "Nenu chesina meme ki explanation ravali! 😏",
        "Nenu chesina meme ki copyright undadu! 😂",
        "Nenu chesina meme ki punch undali! 🥊",
        "Nenu chesina meme ki filter undali! 😎",
        "Nenu chesina meme ki backup undali! 📝",
        "Nenu chesina meme ki steps undali! 💃",
        "Nenu chesina meme ki twist undali! 😜",
        "Nenu chesina meme ki angle undali! 🤳",
        "Nenu chesina meme ki suspense undali! 😲",
    ],
    "Engineers": [
        "Engineering: Where sleep is a myth and deadlines are real 😴📚",
        "When you pass the exam by writing only formulas 😂",
        "When you fix a bug by commenting out the code 😅",
        "When you realize your project is due tomorrow 😱",
        "When you say 'chalega' for every jugaad solution 😎",
        "When you attend class just for attendance sheet 📝",
        "When you see 'placement drive' and panic mode ON 😨",
        "When you survive 4 years of engineering, you can survive anything 💪",
        "When you ask 'placement ki preparation start chesava?' and get silence 😶",
        "When you see your name in the attendance list but you never attended 😂",
        "When you submit the assignment 5 minutes before deadline ⏰",
        "When you realize you have backlogs but still chill 😎",
        "When you and your friend both fail and say 'next sem lo chuddam' 😁",
        "When you attend lab just to sign the register 🧑‍🔬",
        "When you see '100% placement' banner and laugh internally 🤣",
        "When you say 'engineering ante easy' and regret later 😅",
        "When you do group study and end up watching movies 🍿",
        "When you ask 'placement package enti?' and get shocked 😳",
        "When you see your friend placed and you still preparing 😭",
        "When you say 'last bench best bench' and enjoy life 😎",
        "When you attend online class and sleep with camera off 😴",
        "When you say 'project work' but actually chilling with friends 😂",
        "When you see 'internship' and think it's a vacation 🏖️",
        "When you say 'CGPA ante em ledu bro' and cry during placements 😭",
        "When you attend campus interview and forget your name 😅",
        "When you say 'placement ki ready' but still searching for resume template 🤦‍♂️",
        "When you see 'core job' and run away to IT 😂",
        "When you say 'coding ante headache bro' and still apply for IT jobs 🤣",
        "When you see 'aptitude test' and open calculator app immediately 🧮",
        "When you say 'placement lo HR round easy' and get rejected 😬",
    ],
    "Placements": [
        "When you see 'placement drive' and your heart skips a beat 😱",
        "When you clear aptitude but fail in technical round 😭",
        "When HR asks 'tell me about yourself' and you forget everything 😅",
        "When you say 'I am flexible' but mean 'I need job urgently' 😂",
        "When you see your friend placed and you still preparing 😭",
        "When you get placed and update LinkedIn immediately 😎",
        "When you say 'package enti?' and get shocked 😳",
        "When you attend interview in formals for the first time 👔",
        "When you say 'I am a team player' but hate group projects 😆",
        "When you say 'I am passionate about coding' but Google everything 🤣",
        "When you attend campus interview and forget your name 😅",
        "When you say 'placement ki ready' but still searching for resume template 🤦‍♂️",
        "When you see 'core job' and run away to IT 😂",
        "When you say 'coding ante headache bro' and still apply for IT jobs 🤣",
        "When you see 'aptitude test' and open calculator app immediately 🧮",
        "When you say 'placement lo HR round easy' and get rejected 😬",
        "When you get offer letter and celebrate like you won a lottery 🥳",
        "When you say 'salary ante em ledu bro, experience important' and cry at month end 😅",
        "When you attend interview and HR says 'we'll get back to you' 😐",
        "When you say 'I am open to relocation' but want to stay at home 🏠",
    ],
    "Lecturer/Teacher Struggles": [
        "When you ask 'any doubts?' and get silence 😶",
        "When you say 'attendance is important' and students disappear 😂",
        "When you explain the same topic thrice and still get doubts 😅",
        "When you say 'last 5 minutes' and teach for 30 more minutes ⏰",
        "When you say 'surprise test' and students panic 😱",
        "When you say 'projector not working' and students celebrate 🎉",
        "When you say 'submit assignment tomorrow' and get 100 excuses 😆",
        "When you say 'no mobile phones' and students still texting 📱",
        "When you say 'group discussion' and only one group talks 😂",
        "When you say 'open book test' and students still copy 😅",
        "When you say 'extra class' and students vanish 🏃‍♂️",
        "When you say 'I will check homework' and students pray 🙏",
        "When you say 'I will take attendance' and class is full 😁",
        "When you say 'I will give marks for discipline' and students start behaving 😇",
        "When you say 'I will finish syllabus today' and never finish 😅",
        "When you say 'I will give grace marks' and students celebrate 🥳",
        "When you say 'I will take viva' and students disappear 😱",
        "When you say 'I will give surprise quiz' and students panic 😨",
        "When you say 'I will give bonus marks' and students become toppers 😂",
        "When you say 'I will give attendance for project work' and students become engineers overnight 🤣",
        # Telugu
        "Sir: 'Evaraina doubt unda?' Class: 'Silence' 😅",
        "Lecturer: 'Attendance is must' Students: 'Zoom lo join chestam sir' 😂",
        "Sir: 'Assignment submit cheyyandi' Students: 'Net ledu sir' 😆",
        "Sir: 'Extra class undi' Students: 'Home ki vellali sir' 🏃‍♂️",
        "Sir: 'Projector panicheyyadu' Students: 'Super sir' 🎉",
        "Sir: 'Viva undi' Students: 'Leave pettandi sir' 😱",
        "Sir: 'Syllabus complete chestha' Students: 'Next year sir' 😅",
        "Sir: 'Discipline ki marks istanu' Students: 'Andaru silent' 😇",
        "Sir: 'Surprise test' Students: 'Ammayi poyindi sir' 😨",
        "Sir: 'Bonus marks istanu' Students: 'Jai ho sir' 😂",
    ],
    "Other": [
        "When you finish a series and don't know what to do with life 📺😭",
        "When you realize it's Monday tomorrow 😩",
        "When you get a call from home during class 😅",
        "When you realize tomorrow is a holiday 🎉",
        "When you check your bank account after a weekend out 💸",
        "When you try to act serious but fail miserably 😂",
        "When you laugh at your own joke because no one else did 🤣",
        "When you finally get WiFi after hours of struggle 🙌📶",
        "When you try to act cool but trip in front of everyone 😅",
        "When you see your neighbor and pretend you didn't 😅",
        "When you try to take a selfie and camera opens front cam 😳",
        "When you realize you wore mismatched socks all day 🧦😂",
        "When you try to act like an adult but want to nap like a kid 😴",
        "When you see your childhood photo and cringe 😂",
        "When you try to be productive but end up watching reels all day 📱😂",
    ]
}

def memeify_image(image, caption):
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    draw = ImageDraw.Draw(image)
    # Try to use a font that supports emojis
    font = None
    font_size = int(image.height/12)
    try:
        font = ImageFont.truetype("seguiemj.ttf", size=font_size)  # Segoe UI Emoji (Windows)
    except:
        try:
            font = ImageFont.truetype("Segoe UI Emoji.ttf", size=font_size)
        except:
            try:
                font = ImageFont.truetype("NotoColorEmoji.ttf", size=font_size)  # Noto Color Emoji (Linux/Google)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", size=font_size)
                except:
                    font = ImageFont.load_default()
    # Wrap text
    margin = 40
    max_width = image.width - 2*margin
    lines = []
    for line in caption.split('\n'):
        lines.extend(textwrap.wrap(line, width=22))
    y = margin
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (image.width - w) / 2
        # Draw black outline
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                draw.text((x+dx, y+dy), line, font=font, fill='black')
        # Draw white text
        draw.text((x, y), line, font=font, fill='white')
        y += h + 5
    return image

def main():
    st.set_page_config(page_title="Memeify My Photo", page_icon="😂", layout="centered")
    # Custom CSS for background and joyful style
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #f9d423 0%, #ff4e50 100%) !important;
        }
        .stApp {
            background: linear-gradient(135deg, #f9d423 0%, #ff4e50 100%) !important;
        }
        .meme-header {
            font-size: 3em;
            font-weight: bold;
            color: #fff700;
            text-shadow: 2px 2px 8px #ff4e50, 0 0 10px #fff;
            text-align: center;
            margin-bottom: 0.2em;
        }
        .meme-sub {
            font-size: 1.3em;
            color: #fff;
            text-align: center;
            margin-bottom: 1em;
        }
        .meme-box {
            background: #fffbe7;
            border-radius: 18px;
            padding: 1.5em 2em;
            box-shadow: 0 4px 24px #ff4e5055;
            margin-bottom: 1.5em;
        }
        .meme-btn button {
            background: linear-gradient(90deg, #f9d423 0%, #ff4e50 100%) !important;
            color: #fff !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            font-size: 1.2em !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="meme-header">Memeify My Photo <span>🖼️😂</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="meme-sub">Upload or capture a photo and get a random, funny meme caption!<br>Spread joy, share laughter! 🎉</div>', unsafe_allow_html=True)
    st.markdown('<div class="meme-box">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    with col2:
        camera_image = st.camera_input("Or take a photo with your camera")
    st.markdown('</div>', unsafe_allow_html=True)
    # Category selection
    st.markdown('<div class="meme-box">', unsafe_allow_html=True)
    category = st.selectbox("Choose a meme category", list(CAPTION_CATEGORIES.keys()))
    st.markdown('</div>', unsafe_allow_html=True)
    image = None
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Photo", use_container_width=True)
    elif camera_image:
        image = Image.open(camera_image)
        st.image(image, caption="Captured Photo", use_container_width=True)
    if image:
        st.markdown('<div class="meme-box">', unsafe_allow_html=True)
        if st.button("Memeify!", key="meme_btn"):
            caption = random.choice(CAPTION_CATEGORIES[category])
            meme_img = memeify_image(image.copy(), caption)
            st.image(meme_img, caption=caption, use_container_width=True)
            buf = io.BytesIO()
            meme_img.save(buf, format="PNG")
            st.download_button("Download Meme", buf.getvalue(), file_name="meme.png", mime="image/png")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
