import streamlit as st
import pandas as pd
import human_module
import animal_module
import landscape_module
import logo_module

# --- 0. 簡易パスワード機能 ---
def check_password():
    def password_entered():
        # 設定したいパスワードをここに記述
        if st.session_state["password"] == "aloft1324": 
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("パスワードを入力してください", type="password", on_change=password_entered, key="password")
        st.info("※このアプリは関係者のみ利用可能です。")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("パスワードを入力してください", type="password", on_change=password_entered, key="password")
        st.error("😕 パスワードが間違っています。")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- 1. アプリ設定 ---
st.set_page_config(page_title="プロンプトメーカーPro", layout="wide")

if "history" not in st.session_state: st.session_state.history = []
if "favorites" not in st.session_state: st.session_state.favorites = []

st.title("🎨 画像生成プロンプトメーカー Pro (完全統合版)")

# --- 2. 被写体定義 ---
categories = {
    "人間": ["女性", "男性"],
    "動物・魔物": ["猫", "犬", "虎", "龍", "ライオン", "鷲", "狼", "グリフォン"],
    "自然・風景": ["山", "海", "森", "宇宙", "砂漠", "浮遊島"],
    "タイトルロゴ": ["ファンタジーロゴ", "SFロゴ", "ホラーロゴ", "企業ロゴ"]
}

subject_to_en = {
    "女性": "woman", "男性": "man",
    "猫": "cat", "犬": "dog", "虎": "tiger", "龍": "dragon", "ライオン": "lion", "鷲": "eagle", "狼": "wolf", "グリフォン": "griffin",
    "山": "mountains", "海": "ocean", "森": "forest", "宇宙": "space", "砂漠": "desert", "浮遊島": "floating island",
    "ファンタジーロゴ": "fantasy logo", "SFロゴ": "sci-fi logo", "ホラーロゴ": "horror logo", "企業ロゴ": "tech logo"
}

# --- 3. サイドバー ---
with st.sidebar:
    st.header("1. 基本選択")
    category = st.selectbox("カテゴリー", list(categories.keys()))
    subject = st.selectbox("被写体", categories[category])
    
    selected_skin = "指定なし"
    if category == "人間":
        skin_tones = {"指定なし": "", "色白": "pale skin", "美白": "fair skin", "普通": "natural skin", "小麦色": "tan skin", "褐色": "dark skin"}
        selected_skin = st.selectbox("肌の色", list(skin_tones.keys()))

# --- 4. メイン画面：詳細設定 (モジュール呼び出し) ---
st.header(f"2. {category}の詳細設定")
prompt_details = []

if category == "人間":
    prompt_details.extend(human_module.get_human_settings(subject_to_en[subject]))
    if selected_skin != "指定なし": prompt_details.append(skin_tones[selected_skin])
elif category == "動物・魔物":
    prompt_details.extend(animal_module.get_animal_settings(subject_to_en[subject]))
elif category == "自然・風景":
    prompt_details.extend(landscape_module.get_landscape_settings(subject_to_en[subject]))
elif category == "タイトルロゴ":
    prompt_details.extend(logo_module.get_logo_settings(subject_to_en[subject]))

# --- 5. 共通設定（背景・カメラ・画風） ---
st.divider()
st.header("3. 共通設定（背景・カメラ・画風）")
c1, c2, c3 = st.columns(3)

with c1:
    if category != "タイトルロゴ":
        bg_type = st.radio("背景タイプ", ["風景（天候）", "単色背景"], horizontal=True)
        if bg_type == "単色背景":
            bg_color = st.color_picker("背景色を選択", "#ffffff")
            prompt_details.append(f"on simple flat {bg_color} background")
        else:
            weather = st.selectbox("環境・天気", ["指定なし", "晴れ", "雨", "雪", "霧", "魔法の光", "木漏れ日"])
            w_dict = {"晴れ": "sunny", "雨": "rainy", "雪": "snowy", "霧": "foggy", "魔法の光": "magical light", "木漏れ日": "sun dappled"}
            if weather != "指定なし": prompt_details.append(f"{w_dict[weather]} weather")
    else:
        st.write("ロゴ背景は個別設定に従います")

with c2:
    shot = st.selectbox("カメラ距離", ["指定なし", "全身", "上半身", "顔のアップ", "引きの絵"])
    shot_dict = {"全身": "full body shot", "上半身": "medium shot", "顔のアップ": "close-up shot", "引きの絵": "wide shot"}
    if shot != "指定なし": prompt_details.append(shot_dict[shot])
    
    angle = st.selectbox("カメラ角度", ["指定なし", "正面", "俯瞰", "アオリ", "真横"])
    angle_dict = {"正面": "eye level", "俯瞰": "high angle", "アオリ": "low angle", "真横": "side view"}
    if angle != "指定なし": prompt_details.append(angle_dict[angle])

with c3:
    style = st.selectbox("画風", ["アニメ風", "実写", "水彩画", "油絵", "3D", "ピクセルアート"])
    st_dict = {"アニメ風": "anime style", "実写": "photorealistic", "水彩画": "watercolor", "油絵": "oil painting", "3D": "3D render", "ピクセルアート": "pixel art"}
    prompt_details.append(st_dict[style])

picked_color = st.color_picker("全体のカラーテーマ", "#ffffff")

# --- 6. 生成ボタン ---
st.divider()
if st.button("✨ プロンプトを生成する", type="primary", use_container_width=True):
    p_list = prompt_details + [f"color theme {picked_color}", "masterpiece, best quality, highly detailed"]
    final_positive = ", ".join([p for p in p_list if p])
    
    if category == "タイトルロゴ":
        final_negative = "bad text, wrong font, blurry, low resolution, messy, ugly, distorted"
    else:
        final_negative = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, worst quality, low quality"

    st.session_state.history.insert(0, {"positive": final_positive, "negative": final_negative, "subject": subject})
    st.subheader("生成結果")
    st.code(final_positive)
    st.caption("Negative Prompt:")
    st.code(final_negative)

# --- 7. お気に入り ---
st.divider()
st.header("⭐ お気に入り")
if st.session_state.favorites:
    for idx, fav in enumerate(st.session_state.favorites):
        with st.expander(f"⭐ お気に入り {idx+1}: {fav['subject']}"):
            st.code(fav['positive'])
            if st.button(f"削除 (No.{idx+1})", key=f"del_fav_{idx}"):
                st.session_state.favorites.pop(idx)
                st.rerun()
    df_fav = pd.DataFrame(st.session_state.favorites)
    csv_data = df_fav.to_csv(index=False).encode('utf_8_sig')
    st.download_button(label="📥 お気に入りをCSVで保存", data=csv_data, file_name="my_prompts.csv", mime="text/csv")

# --- 8. 履歴 ---
st.divider()
col_h1, col_h2 = st.columns([0.8, 0.2])
with col_h1: st.header("📜 履歴")
with col_h2: 
    if st.button("🗑️ 履歴全削除"): 
        st.session_state.history = []
        st.rerun()

if st.session_state.history:
    for i, item in enumerate(st.session_state.history):
        with st.expander(f"履歴 {len(st.session_state.history)-i}: {item['subject']}"):
            st.code(item['positive'])
            if st.button(f"⭐ お気に入りに追加", key=f"fav_btn_{i}"):
                if item not in st.session_state.favorites:
                    st.session_state.favorites.append(item)
                    st.toast("追加しました！")
                st.rerun()