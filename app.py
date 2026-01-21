import streamlit as st
import pandas as pd
import os
import getpass
from deep_translator import GoogleTranslator
import human_module
import animal_module
import landscape_module
import logo_module

# ページ設定
st.set_page_config(page_title="プロンプト作成メーカー", layout="wide")

# --- 0. パスワード機能 ---
def check_password():
    local_user = "himai" 
    current_user = getpass.getuser()
    if current_user == local_user:
        return True
    try:
        target_password = st.secrets.get("password") or st.secrets.get("passwords", {}).get("password")
    except:
        st.error("🔒 セキュリティ設定が見つかりません。")
        st.stop()
    if target_password is None:
        st.error("🔒 パスワードが設定されていません。")
        st.stop()

    def password_entered():
        if st.session_state["password"] == target_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("パスワードを入力してください", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("パスワードを入力してください", type="password", on_change=password_entered, key="password")
        st.error("😕 パスワードが間違っています。")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- 1. Session State の初期化 ---
if "history" not in st.session_state or isinstance(st.session_state.history, list):
    st.session_state.history = pd.DataFrame(columns=["日付", "タイトル", "プロンプト"])
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "custom_keywords" not in st.session_state:
    st.session_state.custom_keywords = []

# --- 2. データ定義 ---
categories = {
    "人間": ["女性", "男性"],
    "動物・魔物": ["猫", "犬", "馬", "虎", "ライオン", "鷲", "龍", "狼", "グリフォン"],
    "風景・環境": ["山", "海", "森", "滝", "空", "崖", "ビル群", "宇宙", "砂漠", "洞窟", "浮遊島"],
    "タイトルロゴ": ["ファンタジーロゴ", "SFロゴ", "ホラーロゴ", "企業ロゴ", "ヴィンテージロゴ"]
}

subject_to_en = {
    "女性": "woman", "男性": "man",
    "猫": "cat", "犬": "dog", "馬": "horse", "虎": "tiger", "ライオン": "lion", "鷲": "eagle", "龍": "dragon", "狼": "wolf", "グリフォン": "griffin",
    "山": "mountains", "海": "ocean", "森": "forest", "滝": "waterfall", 
    "空": "sky", "崖": "cliff", "ビル群": "cityscape, skyscrapers",
    "宇宙": "space", "砂漠": "desert", "洞窟": "cave", "浮遊島": "floating island",
    "ファンタジーロゴ": "fantasy game logo", "SFロゴ": "sci-fi movie logo", "ホラーロゴ": "horror logo", "企業ロゴ": "tech logo", "ヴィンテージロゴ": "vintage logo"
}

# 「美白」を追加
skin_tones = {
    "指定なし": "", 
    "美白": "fair porcelain skin, radiant skin", 
    "色白": "pale skin", 
    "普通": "natural skin tone", 
    "日焼け": "tanned skin", 
    "褐色": "brown skin"
}

# --- 3. サイドバー ---
with st.sidebar:
    st.header("1. 基本選択")
    category = st.selectbox("カテゴリー", list(categories.keys()))
    subject_label = "テーマ" if category == "タイトルロゴ" else "被写体"
    subject = st.selectbox(subject_label, categories[category])
    
    selected_skin = "指定なし"
    if category == "人間":
        # ドロップダウン（selectbox）に変更
        selected_skin = st.selectbox("肌の色", list(skin_tones.keys()))

# --- 4. 詳細設定 ---
st.title("🎨 AIプロンプト作成メーカー")
st.header(f"2. {category}の詳細設定")
prompt_details = []
history_title = subject 

if category == "人間":
    res, f_style, cloth = human_module.get_human_settings(subject_to_en[subject])
    prompt_details.extend(res)
    if selected_skin != "指定なし": prompt_details.append(skin_tones[selected_skin])
    history_title = f"{subject} / {f_style} / {cloth}"
elif category == "動物・魔物":
    res, state = animal_module.get_animal_settings(subject_to_en[subject])
    prompt_details.extend(res)
    history_title = f"{subject} ({state})"
elif category == "風景・環境":
    res, vibe = landscape_module.get_landscape_settings(subject_to_en[subject])
    prompt_details.extend(res)
    history_title = f"{subject} ({vibe})"
elif category == "タイトルロゴ":
    res, text, shape, world, material = logo_module.get_logo_settings(subject_to_en[subject])
    prompt_details.extend(res)
    history_title = f"Logo: {text} / {shape} / {world} / {material}"

# --- 5. 自由入力・翻訳セクション ---
st.divider()
st.header("追加カスタムキーワード")
col_inp1, col_inp2 = st.columns([0.7, 0.3])
with col_inp1:
    custom_input = st.text_input("日本語で入力（例：チェック柄、逆光、サイバー）", key="input_box")
with col_inp2:
    st.write(" ")
    if st.button("翻訳して追加", use_container_width=True):
        if custom_input:
            with st.spinner('翻訳中...'):
                translated = GoogleTranslator(source='ja', target='en').translate(custom_input)
                st.session_state.custom_keywords.append(translated)
                st.rerun()

if st.session_state.custom_keywords:
    st.write("▼ 追加済みのキーワード（クリックで削除）")
    cols = st.columns(5)
    for i, word in enumerate(st.session_state.custom_keywords):
        if cols[i % 5].button(f"× {word}", key=f"custom_word_{i}", use_container_width=True):
            st.session_state.custom_keywords.pop(i)
            st.rerun()

# --- 6. 共通設定 ---
st.divider()
st.header("3. 共通設定")
c1, c2, c3 = st.columns(3)
with c1:
    bg_choice = st.radio("背景タイプ", ["風景（天候）", "単色背景", "背景透過用"])
    if bg_choice == "単色背景":
        bg_color = st.color_picker("背景色", "#ffffff")
        prompt_details.append(f"on simple flat {bg_color} background")
    elif bg_choice == "背景透過用":
        prompt_details.append("isolated on white background, high contrast, alpha channel ready")
    else:
        weather = st.selectbox("環境・天気", ["指定なし", "晴れ", "雨", "雪", "霧", "魔法の光", "木漏れ日"])
        w_dict = {"晴れ": "sunny weather", "雨": "rainy weather", "雪": "snowy weather", "霧": "foggy", "魔法の光": "magical light", "木漏れ日": "sun dappled"}
        if weather != "指定なし": prompt_details.append(w_dict[weather])

with c2:
    shot = st.selectbox("カメラ距離", ["指定なし", "全身", "上半身", "顔のアップ", "引きの絵"])
    shot_dict = {"全身": "full body shot", "上半身": "medium shot", "顔のアップ": "close-up shot", "引きの絵": "wide shot"}
    if shot != "指定なし": prompt_details.append(shot_dict[shot])
    
    angle = st.selectbox("カメラ角度", ["指定なし", "正面", "俯瞰", "アオリ", "真横"])
    angle_dict = {"正面": "eye level", "俯瞰": "high angle", "アオリ": "low angle", "真横": "side view"}
    if angle != "指定なし": prompt_details.append(angle_dict[angle])

    aspect_ratio = st.selectbox("アスペクト比", ["指定なし", "正方形 (1:1)", "横長 (16:9)", "縦長 (9:16)", "シネマ (21:9)"])
    ar_dict = {"正方形 (1:1)": "--ar 1:1", "横長 (16:9)": "--ar 16:9", "縦長 (9:16)": "--ar 9:16", "シネマ (21:9)": "--ar 21:9"}
    if aspect_ratio != "指定なし": prompt_details.append(ar_dict[aspect_ratio])

with c3:
    style = st.selectbox("画風", ["アニメ風", "実写", "3D", "ピクセルアート", "水彩画"])
    st_dict = {"アニメ風": "anime style", "実写": "photorealistic", "3D": "3D render", "ピクセルアート": "pixel art", "水彩画": "watercolor style"}
    prompt_details.append(st_dict[style])
    picked_color = st.color_picker("全体のカラーテーマ", "#ffffff")

# --- 7. 生成ボタン ---
st.divider()
if st.button("✨ プロンプト生成", type="primary", use_container_width=True):
    final_prompt_list = prompt_details.copy()
    if st.session_state.custom_keywords:
        final_prompt_list.extend(st.session_state.custom_keywords)
    final_prompt_list.append(f"color theme {picked_color}")
    final_prompt_list.append("masterpiece, best quality, highly detailed")
    
    full_prompt = ", ".join(final_prompt_list)
    
    new_entry = pd.DataFrame([{
        "日付": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
        "タイトル": history_title,
        "プロンプト": full_prompt
    }])
    st.session_state.history = pd.concat([new_entry, st.session_state.history], ignore_index=True)
    st.balloons()
    st.code(full_prompt)

# --- 8. 履歴表示 ---
st.divider()
st.header("📜 生成履歴")
if isinstance(st.session_state.history, pd.DataFrame) and not st.session_state.history.empty:
    st.dataframe(st.session_state.history, use_container_width=True)
    if st.button("履歴をクリア"):
        st.session_state.history = pd.DataFrame(columns=["日付", "タイトル", "プロンプト"])
        st.rerun()
else:
    st.info("履歴はまだありません。")