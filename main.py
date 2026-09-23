import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
import html


# =========================================================
# CẤU HÌNH APP
# =========================================================

st.set_page_config(
    page_title="Dịch Nhanh",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {
    background: #f6f7f9;
}

/* Nội dung chính */
.block-container {
    max-width: 700px;
    padding-top: 25px;
    padding-bottom: 40px;
}

/* Tiêu đề */
.app-title {
    text-align: center;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 4px;
}

.app-subtitle {
    text-align: center;
    color: #777;
    font-size: 15px;
    margin-bottom: 25px;
}

/* Card */
.card {
    background: white;
    border-radius: 22px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
}

/* Ngôn ngữ */
.language-title {
    text-align: center;
    font-size: 19px;
    font-weight: 700;
}

/* Mũi tên */
.arrow {
    padding: 0 10px;
    color: #777;
}

/* Khu vực kết quả */
.text-box {
    background: #f1f3f5;
    border-radius: 16px;
    padding: 18px;
    font-size: 20px;
    line-height: 1.5;
    min-height: 70px;
    word-wrap: break-word;
}

/* Nhãn */
.label {
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 9px;
}

/* Nút */
div.stButton > button {
    width: 100%;
    border-radius: 15px;
    height: 48px;
    font-size: 16px;
    font-weight: 650;
}

/* Audio */
audio {
    width: 100%;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    border-radius: 15px;
}

/* Mobile */
@media (max-width: 600px) {

    .block-container {
        padding-left: 15px;
        padding-right: 15px;
    }

    .app-title {
        font-size: 28px;
    }

    .text-box {
        font-size: 18px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DỮ LIỆU 4 CHẾ ĐỘ
# =========================================================

MODES = {

    "🇻🇳 Việt → 🇬🇧 Anh": {
        "source": "vi",
        "target": "en",
        "source_name": "Tiếng Việt",
        "target_name": "English",
        "speech_language": "vi-VN",
        "tts_language": "en"
    },

    "🇻🇳 Việt → 🇨🇳 Trung": {
        "source": "vi",
        "target": "zh-CN",
        "source_name": "Tiếng Việt",
        "target_name": "中文",
        "speech_language": "vi-VN",
        "tts_language": "zh-CN"
    },

    "🇨🇳 Trung → 🇻🇳 Việt": {
        "source": "zh-CN",
        "target": "vi",
        "source_name": "中文",
        "target_name": "Tiếng Việt",
        "speech_language": "zh-CN",
        "tts_language": "vi"
    },

    "🇬🇧 Anh → 🇻🇳 Việt": {
        "source": "en",
        "target": "vi",
        "source_name": "English",
        "target_name": "Tiếng Việt",
        "speech_language": "en-US",
        "tts_language": "vi"
    }
}


# =========================================================
# HÀM NHẬN DIỆN GIỌNG NÓI
# =========================================================

def recognize_speech(audio_file, language):

    recognizer = sr.Recognizer()

    try:

        # Đưa file audio về đầu file
        audio_file.seek(0)

        # Streamlit audio_input tạo file WAV
        with sr.AudioFile(audio_file) as source:

            audio_data = recognizer.record(source)

        # Google Speech Recognition
        result = recognizer.recognize_google(
            audio_data,
            language=language
        )

        return result.strip()

    except sr.UnknownValueError:

        return None

    except sr.RequestError:

        raise Exception(
            "Không thể kết nối dịch vụ nhận diện giọng nói."
        )

    except Exception as error:

        raise Exception(
            f"Lỗi xử lý âm thanh: {error}"
        )


# =========================================================
# HÀM DỊCH
# =========================================================

def translate_text(text, source, target):

    try:

        translator = GoogleTranslator(
            source=source,
            target=target
        )

        result = translator.translate(text)

        return result

    except Exception as error:

        raise Exception(
            f"Không thể dịch câu này: {error}"
        )


# =========================================================
# HÀM TẠO GIỌNG NÓI
# =========================================================

def create_voice(text, language):

    try:

        audio_buffer = BytesIO()

        tts = gTTS(
            text=text,
            lang=language,
            slow=False
        )

        tts.write_to_fp(audio_buffer)

        audio_buffer.seek(0)

        return audio_buffer

    except Exception as error:

        raise Exception(
            f"Không thể tạo giọng nói: {error}"
        )


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="app-title">🌐 Dịch Nhanh</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'Nói • Dịch • Nghe'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# CHỌN CHẾ ĐỘ
# =========================================================

mode_name = st.selectbox(
    "Chọn chế độ dịch",
    list(MODES.keys())
)

mode = MODES[mode_name]


# =========================================================
# HIỂN THỊ NGÔN NGỮ
# =========================================================

st.markdown(
    f"""
    <div class="card">
        <div class="language-title">
            {mode["source_name"]}
            <span class="arrow">→</span>
            {mode["target_name"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MICRO
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        font-size:15px;
        color:#666;
        margin-bottom:8px;
    ">
        🎙️ Nhấn nút bên dưới và nói
    </div>
    """,
    unsafe_allow_html=True
)


audio = st.audio_input(
    "🎙️ Nhấn để nói",
    sample_rate=16000
)


# =========================================================
# KHI NGƯỜI DÙNG NÓI
# =========================================================

if audio is not None:

    # -----------------------------------------------------
    # NHẬN DIỆN
    # -----------------------------------------------------

    with st.spinner("🎧 Đang nghe và nhận diện..."):

        try:

            original_text = recognize_speech(
                audio,
                mode["speech_language"]
            )

        except Exception as error:

            st.error(str(error))
            st.stop()


    # -----------------------------------------------------
    # KHÔNG NGHE ĐƯỢC
    # -----------------------------------------------------

    if not original_text:

        st.warning(
            "😕 Mình chưa nghe rõ. "
            "Bạn thử nói gần mic hơn và chậm hơn một chút nhé."
        )

        st.stop()


    # -----------------------------------------------------
    # HIỂN THỊ CÂU GỐC
    # -----------------------------------------------------

    safe_original = html.escape(original_text)

    st.markdown(
        f"""
        <div class="card">

            <div class="label">
                🗣️ Bạn nói
            </div>

            <div class="text-box">
                {safe_original}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # DỊCH
    # -----------------------------------------------------

    with st.spinner("🌐 Đang dịch..."):

        try:

            translated_text = translate_text(
                original_text,
                mode["source"],
                mode["target"]
            )

        except Exception as error:

            st.error(str(error))
            st.stop()


    # -----------------------------------------------------
    # HIỂN THỊ BẢN DỊCH
    # -----------------------------------------------------

    safe_translation = html.escape(
        translated_text
    )

    st.markdown(
        f"""
        <div class="card">

            <div class="label">
                🌐 Bản dịch
            </div>

            <div class="text-box">
                {safe_translation}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # TẠO GIỌNG NÓI
    # -----------------------------------------------------

    with st.spinner("🔊 Đang tạo giọng đọc..."):

        try:

            voice = create_voice(
                translated_text,
                mode["tts_language"]
            )

        except Exception as error:

            st.error(str(error))
            st.stop()


    # -----------------------------------------------------
    # PHÁT ÂM THANH
    # -----------------------------------------------------

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 🔊 Nghe bản dịch"
    )

    st.audio(
        voice,
        format="audio/mp3"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# HƯỚNG DẪN
# =========================================================

with st.expander("ℹ️ Cách sử dụng"):

    st.write(
        """
        **Bước 1:** Chọn ngôn ngữ cần dịch.

        **Bước 2:** Nhấn nút 🎙️ và nói.

        **Bước 3:** Ứng dụng nhận diện câu nói.

        **Bước 4:** Ứng dụng dịch sang ngôn ngữ còn lại.

        **Bước 5:** Nhấn ▶️ để nghe bản dịch.
        """
    )


# =========================================================
# CHÂN TRANG
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#999;
        font-size:13px;
        margin-top:30px;
    ">
        🌐 Dịch Nhanh • Việt • Anh • Trung
    </div>
    """,
    unsafe_allow_html=True
)