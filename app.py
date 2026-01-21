import streamlit as st
import pandas as pd
import os
import getpass
from deep_translator import GoogleTranslator  # ここに移動
import human_module
# ...（他のモジュール）
import animal_module
import landscape_module
import logo_module

# --- 0. パスワード機能 (エラー回避・ローカル完全スルー版) ---
def check_password():
    # 自分のPCのユーザー名（エラーログに表示されていた "himai"）を指定
    # これにより、あなたのPCで動かす時だけパスワード機能を完全にバイパスします
    local_user = "himai" 
    
    # 実行中のユーザー名を取得
    import getpass
    current_user = getpass.getuser()

    # ローカルPC環境ならパスワード処理を一切行わずに終了
    if current_user == local_user:
        return True

    # --- 以下、サーバー（Streamlit Cloud）用の処理 ---
    # サーバー上では st.secrets を参照するが、ローカルではここは実行されない
    try:
        target_password = st.secrets.get("password") or st.secrets.get("passwords", {}).get("password")
    except:
        # 万が一サーバーでSecretsが読み込めない場合
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

# パスワードチェック実行
if not check_password():
    st.stop()

# --- 1. アプリ設定 ---
st.set_page_config(page_title="プロンプトメーカーPro", layout="wide")
if "history" not in st.session_state: st.session_state.history = []
if "favorites" not in st.session_state: st.session_state.favorites = []

st.title("🎨 画像生成プロンプトメーカー Pro")

# --- 2. データ定義の更新 ---
categories = {
    "人間": ["女性", "男性"],
    "動物・魔物": ["猫", "犬", "馬", "虎", "ライオン", "鷲", "龍", "狼", "グリフォン"],
    "風景・環境": ["山", "海", "森", "滝", "空", "崖", "ビル群", "宇宙", "砂漠", "洞窟", "浮遊島"], # 追加
    "タイトルロゴ": ["ファンタジーロゴ", "SFロゴ", "ホラーロゴ", "企業ロゴ", "ヴィンテージロゴ"]
}

subject_to_en = {
    "女性": "woman", "男性": "man",
    "猫": "cat", "犬": "dog", "馬": "horse", "虎": "tiger", "ライオン": "lion", "鷲": "eagle", "龍": "dragon", "狼": "wolf", "グリフォン": "griffin",
    "山": "mountains", "海": "ocean", "森": "forest", "滝": "waterfall", 
    "空": "sky", "崖": "cliff", "ビル群": "cityscape, skyscrapers", # 追加
    "宇宙": "space", "砂漠": "desert", "洞窟": "cave", "浮遊島": "floating island",
    "ファンタジーロゴ": "fantasy game logo", "SFロゴ": "sci-fi movie logo", "ホラーロゴ": "horror logo", "企業ロゴ": "tech logo", "ヴィンテージロゴ": "vintage logo"
}

# --- 3. サイドバー ---
with st.sidebar:
    st.header("1. 基本選択")
    category = st.selectbox("カテゴリー", list(categories.keys()))
    
    # 表示名を「テーマ」に変更
    subject_label = "テーマ" if category == "タイトルロゴ" else "被写体"
    subject = st.selectbox(subject_label, categories[category])
    
    selected_skin = "指定なし"
    # ...（以下、肌の色などの処理は変更なし）
    if category == "人間":
        skin_tones = {"指定なし": "", "色白": "pale skin", "美白": "fair skin", "普通": "natural skin", "小麦色": "tan skin", "褐色": "dark skin"}
        selected_skin = st.selectbox("肌の色", list(skin_tones.keys()))

# --- 4. 詳細設定 (各モジュール呼び出し) ---
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

# ↓↓↓ ここが「風景・環境」に一致しているか確認してください ↓↓↓
elif category == "風景・環境":
    res, vibe = landscape_module.get_landscape_settings(subject_to_en[subject])
    prompt_details.extend(res)
    history_title = f"{subject} ({vibe})"

elif category == "タイトルロゴ":
    res, text, shape, world, material = logo_module.get_logo_settings(subject_to_en[subject])
    prompt_details.extend(res)
    history_title = f"Logo: {text} / {shape} / {world} / {material}"

# --- 4.5 自由入力・翻訳セクション ---
st.divider()
st.header("追加カスタムキーワード")

if "custom_keywords" not in st.session_state:
    st.session_state.custom_keywords = []

col_inp1, col_inp2 = st.columns([0.7, 0.3])
with col_inp1:
    # keyを指定することで、ボタン押下後に中身を操作しやすくします
    custom_input = st.text_input("追加したい要素を日本語で入力（例：チェック柄、逆光、サイバーシティ）", key="input_box")

with col_inp2:
    st.write(" ") # ラベルとの高さを合わせるための余白
    if st.button("翻訳して追加", type="secondary", use_container_width=True):
        if custom_input:
            with st.spinner('翻訳中...'):
                try:
                    translated = GoogleTranslator(source='ja', target='en').translate(custom_input)
                    st.session_state.custom_keywords.append(translated)
                    st.toast(f"追加: {translated}")
                except Exception as e:
                    st.error("翻訳に失敗しました。ネット接続を確認してください。")

# 追加されたキーワードをタグのように表示
if st.session_state.custom_keywords:
    st.write("▼ 追加済みのキーワード（クリックで削除）")
    # キーワードを横並びに表示する工夫
    tags = st.container()
    cols = tags.columns(min(len(st.session_state.custom_keywords), 5)) # 最大5列で折り返し
    for i, word in enumerate(st.session_state.custom_keywords):
        col_idx = i % 5
        if cols[col_idx].button(f"× {word}", key=f"custom_word_{i}", use_container_width=True):
            st.session_state.custom_keywords.pop(i)
            st.rerun()

# --- 5. 共通設定 ---
st.divider()
st.header("3. 共通設定（背景・カメラ・画風・サイズ）")
c1, c2, c3 = st.columns(3)

with c1:
    if category != "タイトルロゴ":
        bg_type = st.radio("背景タイプ", ["風景（天候）", "単色背景", "背景透過用（透過指定）"], horizontal=False)
        if bg_type == "単色背景":
            bg_color = st.color_picker("背景色", "#ffffff")
            prompt_details.append(f"on simple flat {bg_color} background")
        elif bg_type == "背景透過用（透過指定）":
            prompt_details.append("isolated on white background, high contrast, alpha channel ready, simple background")
            st.info("💡 切り抜きやすい白背景で生成します。")
        else:
            weather = st.selectbox("環境・天気", ["指定なし", "晴れ", "雨", "雪", "霧", "魔法の光", "木漏れ日"])
            w_dict = {"晴れ": "sunny", "雨": "rainy", "雪": "snowy", "霧": "foggy", "魔法の光": "magical light", "木漏れ日": "sun dappled"}
            if weather != "指定なし": prompt_details.append(f"{w_dict[weather]} weather")
    else:
        # タイトルロゴ用背景設定
        bg_type_logo = st.radio("背景タイプ", ["単色背景", "背景透過用（透過指定）", "風景"], horizontal=False)
        if bg_type_logo == "単色背景":
            bg_color = st.color_picker("背景色", "#ffffff")
            prompt_details.append(f"on simple flat {bg_color} background")
        elif bg_type_logo == "背景透過用（透過指定）":
            prompt_details.append("isolated on white background, high contrast, alpha channel ready, simple background")
        else:
            prompt_details.append("cinematic background")

with c2:
    shot = st.selectbox("カメラ距離", ["指定なし", "全身", "上半身", "顔のアップ", "引きの絵"])
    shot_dict = {"全身": "full body shot", "上半身": "medium shot", "顔のアップ": "close-up shot", "引きの絵": "wide shot"}
    if shot != "指定なし": prompt_details.append(shot_dict[shot])
    
    angle = st.selectbox("カメラ角度", ["指定なし", "正面", "俯瞰", "アオリ", "真横"])
    angle_dict = {"正面": "eye level", "俯瞰": "high angle", "アオリ": "low angle", "真横": "side view"}
    if angle != "指定なし": prompt_details.append(angle_dict[angle])

    # --- アスペクト比の追加 ---
    aspect_ratio = st.selectbox("アスペクト比 (縦横比)", ["指定なし", "正方形 (1:1)", "横長 (16:9)", "縦長 (9:16)", "シネマスコープ (21:9)", "旧4:3"])
    ar_dict = {
        "正方形 (1:1)": "square ratio, --ar 1:1",
        "横長 (16:9)": "wide angle, widescreen, --ar 16:9",
        "縦長 (9:16)": "vertical, portrait orientation, --ar 9:16",
        "シネマスコープ (21:9)": "ultra-wide, cinematic ratio, --ar 21:9",
        "旧4:3": "standard ratio, --ar 4:3"
    }
    if aspect_ratio != "指定なし":
        prompt_details.append(ar_dict[aspect_ratio])

with c3:
    style = st.selectbox("画風", ["アニメ風", "実写", "水彩画", "油絵", "3D", "ピクセルアート"])
    st_dict = {"アニメ風": "anime style", "実写": "photorealistic", "水彩画": "watercolor", "油絵": "oil painting", "3D": "3D render", "ピクセルアート": "pixel art"}
    prompt_details.append(st_dict[style])

    picked_color = st.color_picker("全体のカラーテーマ", "#ffffff")

# --- 6. 生成 ---
st.divider()
if st.button("✨ プロンプト生成", type="primary", use_container_width=True):
    p_list = prompt_details + [f"color theme {picked_color}", "masterpiece, best quality, highly detailed"]
    final_p = ", ".join([p for p in p_list if p])
    
    # ネガティブプロンプトの出し分け
    if category == "タイトルロゴ":
        final_n = "bad text, wrong font, blurry, low resolution, messy, ugly, distorted, watermark"
    else:
        final_n = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, worst quality, low quality"
    
    st.session_state.history.insert(0, {"positive": final_p, "negative": final_n, "subject": history_title})
    st.subheader("生成結果")
    st.code(final_p)
    st.caption("Negative Prompt:")
    st.code(final_n)

# --- 7. お気に入り ---
st.divider()
st.header("⭐ お気に入りプロンプト")
if st.session_state.favorites:
    for idx, fav in enumerate(st.session_state.favorites):
        with st.expander(f"⭐ お気に入り {idx+1}: {fav['subject']}"):
            st.code(fav['positive'])
            if st.button(f"削除", key=f"del_fav_{idx}"):
                st.session_state.favorites.pop(idx)
                st.rerun()
    
    df_fav = pd.DataFrame(st.session_state.favorites)
    csv_data = df_fav.to_csv(index=False).encode('utf_8_sig')
    st.download_button(label="📥 お気に入りをCSVで保存", data=csv_data, file_name="my_prompts.csv", mime="text/csv")
else:
    st.write("お気に入りはまだありません。")

# --- 8. 履歴 ---
st.divider()
col_h1, col_h2 = st.columns([0.8, 0.2])
with col_h1:
    st.header("📜 プロンプト履歴")
with col_h2: 
    if st.button("🗑️ 履歴全削除", use_container_width=True): 
        st.session_state.history = []
        st.rerun()

if st.session_state.history:
    for i, item in enumerate(st.session_state.history):
        with st.expander(f"履歴 {len(st.session_state.history)-i}: {item['subject']}"):
            st.code(item['positive'])
            if st.button(f"⭐ お気に入りに追加", key=f"fav_btn_{i}"):
                if item not in st.session_state.favorites:
                    st.session_state.favorites.append(item)
                    st.toast("お気に入りに追加しました！")
                st.rerun()
else:
    st.write("履歴はまだありません。")