import io
import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS


# =========================================================
# CẤU HÌNH
# =========================================================

st.set_page_config(
    page_title="Dịch Nhanh",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# GIAO DIỆN
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
    background: #0b0f14;
    color: white;
}

.block-container {
    max-width: 720px;
    padding-top: 25px;
    padding-bottom: 40px;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 17px;
    margin-bottom: 30px;
}

.card {
    background: #151a22;
    border: 1px solid #262d38;
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 18px;
}

.language {
    text-align: center;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
}

.arrow {
    text-align: center;
    font-size: 30px;
    color: #60a5fa;
    margin: 8px;
}

.result-box {
    background: #11161e;
    border: 1px solid #2c3440;
    border-radius: 18px;
    padding: 20px;
    font-size: 22px;
    line-height: 1.5;
    min-height: 80px;
}

.info {
    text-align: center;
    color: #9ca3af;
    font-size: 14px;
    margin-top: 10px;
}

div.stButton > button {
    width: 100%;
    border-radius: 16px;
    min-height: 52px;
    font-size: 17px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 4 CHẾ ĐỘ DỊCH
# =========================================================

MODES = {
    "🇻🇳 Việt → 🇬🇧 Anh": {
        "source": "vi",
        "target": "en",
        "source_name": "Tiếng Việt",
        "target_name": "English",
        "speech": "vi-VN",
    },

    "🇻🇳 Việt → 🇨🇳 Trung": {
        "source": "vi",
        "target": "zh-CN",
        "source_name": "Tiếng Việt",
        "target_name": "中文",
        "speech": "vi-VN",
    },

    "🇨🇳 Trung → 🇻🇳 Việt": {
        "source": "zh-CN",
        "target": "vi",
        "source_name": "中文",
        "target_name": "Tiếng Việt",
        "speech": "zh-CN",
    },

    "🇬🇧 Anh → 🇻🇳 Việt": {
        "source": "en",
        "target": "vi",
        "source_name": "English",
        "target_name": "Tiếng Việt",
        "speech": "en-US",
    }
}


# =========================================================
# HÀM NHẬN DIỆN GIỌNG NÓI
# =========================================================

def speech_to_text(audio_file, language):
    recognizer = sr.Recognizer()

    try:
        audio_bytes = audio_file.getvalue()

        audio_stream = io.BytesIO(audio_bytes)

        with sr.AudioFile(audio_stream) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(
            audio_data,
            language=language
        )

        return text

    except sr.UnknownValueError:
        return None

    except sr.RequestError:
        st.error(
            "Không kết nối được dịch vụ nhận diện giọng nói. "
            "Hãy kiểm tra Internet rồi thử lại."
        )
        return None

    except Exception as e:
        st.error(f"Lỗi microphone: {e}")
        return None


# =========================================================
# DỊCH
# =========================================================

def translate_text(text, source, target):

    try:
        translator = GoogleTranslator(
            source=source,
            target=target
        )

        return translator.translate(text)

    except Exception as e:
        st.error(f"Lỗi dịch: {e}")
        return None


# =========================================================
# TẠO GIỌNG NÓI
# =========================================================

def text_to_speech(text, language):

    try:

        audio_buffer = io.BytesIO()

        tts = gTTS(
            text=text,
            lang=language,
            slow=False
        )

        tts.write_to_fp(audio_buffer)

        audio_buffer.seek(0)

        return audio_buffer

    except Exception as e:

        st.error(f"Lỗi tạo giọng nói: {e}")

        return None


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="title">🌐 Dịch Nhanh</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Dịch giọng nói Việt • Anh • Trung</div>',
    unsafe_allow_html=True
)


# =========================================================
# CHỌN CHẾ ĐỘ
# =========================================================

mode = st.selectbox(
    "Chọn chế độ dịch",
    list(MODES.keys())
)

config = MODES[mode]


# =========================================================
# HIỂN THỊ NGÔN NGỮ
# =========================================================

st.markdown(
    f"""
    <div class="card">

        <div class="language">
            🎤 {config["source_name"]}
        </div>

        <div class="arrow">
            ↓
        </div>

        <div class="language">
            🔊 {config["target_name"]}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MICROPHONE
# =========================================================

st.markdown(
    "### 🎙️ Nói vào microphone"
)

audio_input = st.audio_input(
    "Nhấn để ghi âm",
    sample_rate=16000,
    key=f"mic_{mode}",
    label_visibility="collapsed"
)


# =========================================================
# XỬ LÝ GIỌNG NÓI
# =========================================================

if audio_input:

    with st.spinner("🎧 Đang nhận diện giọng nói..."):

        spoken_text = speech_to_text(
            audio_input,
            config["speech"]
        )

    if spoken_text:

        st.markdown("### 📝 Bạn nói")

        st.markdown(
            f"""
            <div class="result-box">
            {spoken_text}
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.spinner("🌐 Đang dịch..."):

            translated_text = translate_text(
                spoken_text,
                config["source"],
                config["target"]
            )

        if translated_text:

            st.markdown("### 🔊 Bản dịch")

            st.markdown(
                f"""
                <div class="result-box">
                {translated_text}
                </div>
                """,
                unsafe_allow_html=True
            )

            # =============================================
            # TẠO ÂM THANH
            # =============================================

            tts_language = config["target"]

            # gTTS dùng zh-CN cho tiếng Trung
            if tts_language == "zh-CN":
                tts_language = "zh-CN"

            audio_output = text_to_speech(
                translated_text,
                tts_language
            )

            if audio_output:

                st.markdown("### 🔊 Nghe bản dịch")

                st.audio(
                    audio_output,
                    format="audio/mp3"
                )

                st.download_button(
                    "⬇️ Lưu giọng nói",
                    data=audio_output.getvalue(),
                    file_name="ban_dich.mp3",
                    mime="audio/mpeg"
                )

    else:

        st.warning(
            "Không nghe rõ giọng nói. "
            "Hãy nói gần microphone và thử lại."
        )


# =========================================================
# NHẬP VĂN BẢN THỦ CÔNG
# =========================================================

st.divider()

st.markdown("### ⌨️ Hoặc nhập văn bản")

manual_text = st.text_area(
    "Nội dung",
    placeholder="Nhập câu bạn muốn dịch...",
    height=120,
    label_visibility="collapsed"
)


if st.button("🌐 Dịch văn bản"):

    if manual_text.strip():

        with st.spinner("Đang dịch..."):

            result = translate_text(
                manual_text,
                config["source"],
                config["target"]
            )

        if result:

            st.markdown("### 🔊 Kết quả")

            st.markdown(
                f"""
                <div class="result-box">
                {result}
                </div>
                """,
                unsafe_allow_html=True
            )

            audio_output = text_to_speech(
                result,
                config["target"]
            )

            if audio_output:

                st.audio(
                    audio_output,
                    format="audio/mp3"
                )

    else:

        st.warning("Bạn chưa nhập nội dung.")


# =========================================================
# THÔNG TIN
# =========================================================

st.markdown(
    """
    <div class="info">
    🎙️ Nhận diện giọng nói → 🌐 Dịch → 🔊 Phát âm thanh
    </div>
    """,
    unsafe_allow_html=True
)