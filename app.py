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

# 国籍の定義
nationalities = {
    "指定なし": "",
    "日本": "Japanese ethnicity",
    "韓国": "Korean ethnicity",
    "中国": "Chinese ethnicity",
    "アメリカ": "American, western features",
    "イギリス": "British, classic english features",
    "フランス": "French, chic parisian style",
    "イタリア": "Italian features",
    "ドイツ": "German features",
    "ロシア": "Russian, slavic features",
    "インド": "Indian ethnicity",
    "ブラジル": "Brazilian features",
    "エジプト": "Egyptian features",
    "アフリカ系": "African ethnicity",
    "北欧": "Scandinavian, nordic features",
    "中東": "Middle Eastern ethnicity"
}

# 役職・職業衣装の定義
jobs = {
    "指定なし": "",
    "警官": "police officer uniform, badge, tactical vest",
    "医者": "doctor, white lab coat, stethoscope",
    "ナース": "nurse uniform, medical scrubs",
    "消防士": "firefighter gear, fireproof suit, helmet",
    "弁護士": "lawyer, professional business suit, formal attire",
    "パイロット": "airline pilot uniform, captain's hat, epaulettes",
    "シェフ": "chef's whites, toque hat, apron",
    "ビジネスマン/ウーマン": "modern office wear, professional suit, necktie",
    "建設作業員": "construction worker, high-visibility vest, hard hat",
    "研究員": "scientist, lab coat, safety goggles",
    "教師": "teacher, professional casual attire, holding a book"
}

# --- 3. サイドバー ---
with st.sidebar:
    st.header("1. 基本選択")
    category = st.selectbox("カテゴリー", list(categories.keys()))
    subject_label = "テーマ" if category == "タイトルロゴ" else "被写体"
    subject = st.selectbox(subject_label, categories[category])
    
    selected_skin = "指定なし"
    selected_nat = "指定なし" # 追加
    if category == "人間":
        selected_skin = st.selectbox("肌の色", list(skin_tones.keys()))
        selected_nat = st.selectbox("国籍", list(nationalities.keys())) # 追加


# --- 4. 詳細設定 ---
st.title("🎨 AIプロンプト作成メーカー")
st.header(f"2. {category}の詳細設定")
prompt_details = []
history_title = subject 

if category == "人間":
    # 修正した human_module.get_human_settings を呼び出し、3つの戻り値を受け取る
    res, f_style, cloth = human_module.get_human_settings(subject_to_en[subject])
    prompt_details.extend(res)
    
    # 国籍や肌の色を追加（これらはサイドバーの設定を反映）
    if selected_skin != "指定なし": prompt_details.append(skin_tones[selected_skin])
    if selected_nat != "指定なし": prompt_details.append(nationalities[selected_nat])
    
    # 履歴タイトルに反映（被写体 / スタイル / 具体的な衣装や職種）
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

# 年代設定スライダーの追加
st.subheader("🕰 時代設定")
target_year = st.slider(
    "西暦を選択してください（ファッションや画質に影響します）",
    min_value=1700,
    max_value=2026,
    value=2000, # 基準を2000年に設定
    step=1
)

# 年代に応じたプロンプトの自動生成
if target_year < 1850:
    era_prompt = f"historical scene from {target_year}, oil painting style, traditional aesthetic"
elif target_year < 1900:
    era_prompt = f"year {target_year}, victorian era style, early photography"
elif target_year < 1950:
    era_prompt = f"year {target_year}, vintage style, old film grain"
elif target_year < 2000:
    era_prompt = f"year {target_year}, retro aesthetic, late 20th century style"
else:
    era_prompt = f"year {target_year}, modern contemporary style, high-tech"

prompt_details.append(era_prompt)

# --- フィルタ・特殊効果セクション ---
st.subheader("🎬 フィルタ・特殊効果")

# フィルタ名とプロンプトの対応辞書
effect_dict = {
    "モノクロ": "monochrome, black and white",
    "モノクロマティック": "monochromatic color scheme",
    "モーションブラー": "motion blur, speed lines",
    "シャープネス": "sharp focus, hyper detailed edges",
    "グリッチエフェクト": "glitch effect, digital distortion",
    "グリッチノイズ": "glitch noise, VHS static, chromatic aberration",
    "フレアレンズ": "lens flare, cinematic lighting",
    "バーニング": "burning effect, fire embers, scorched edges",
    "ダストエフェクト": "dust particles, floating dust, film grain",
    "重ね撮り": "double exposure, layered imagery",
    "VFX": "VFX, cinematic post-processing",
    "SFX": "SFX, special effects, practical effects aesthetic"
}

# 複数選択可能なセレクトボックス
selected_effects = st.multiselect(
    "適用したいフィルタを選択してください（複数選択可）",
    options=list(effect_dict.keys()),
    default=[] # 基本は何もかかっていない状態
)

# 選択されたエフェクトをプロンプトに追加
for effect in selected_effects:
    prompt_details.append(effect_dict[effect])

# --- ライティング設定セクション ---
st.subheader("💡 ライティング（照明）")

# ライティング名とプロンプトの対応辞書
lighting_dict = {
    "輝く光": "glowing light, radiant lighting",
    "ぼかし光": "soft bokeh lighting, blurred light",
    "バックライト": "backlighting, silhouette lighting",
    "下からの光": "bottom lighting, mysterious under-lighting",
    "横からの光": "side lighting, dramatic shadows",
    "発光": "bioluminescence, internal glow",
    "スポットライト": "spotlight, focused beam",
    "ステージライト": "stage lighting, concert lights",
    "スタジオの照明": "studio lighting, professional photography lighting",
    "一方向の光": "directional lighting, hard shadows",
    "ドラマチックな光": "dramatic lighting, high contrast lighting",
    "映画的な光": "cinematic lighting, movie set aesthetic",
    "ボリュームのある光": "volumetric lighting, god rays, sunbeams",
    "カラフルな光": "colorful lighting, RGB lights, neon glow",
    "リムライト": "rim lighting, edge lighting",
    "実用的な照明": "practical lighting, realistic indoor lights",
    "暖かい光": "warm lighting, golden hour, 3000k",
    "冷たい光": "cool lighting, blue hour, 8000k",
    "柔らかい光": "soft lighting, diffused light",
    "強い光": "harsh lighting, intense light source",
    "周囲の光": "ambient lighting, global illumination",
    "最適な光": "optimal lighting, perfectly balanced light",
    "ダイナミックな光": "dynamic lighting, shifting light and shadow"
}

# 複数選択可能なセレクトボックス
selected_lighting = st.multiselect(
    "適用したいライティングを選択してください（複数選択可）",
    options=list(lighting_dict.keys()),
    default=[] # 基本は何もかかっていない状態
)

# 選択されたライティングをプロンプトに追加
for light in selected_lighting:
    prompt_details.append(lighting_dict[light])


# --- レンズ設定セクション ---
st.subheader("📷 レンズの種類")

# レンズ名とプロンプトの対応辞書
lens_dict = {
    "魚眼レンズ": "fisheye lens, ultra-wide circular distortion, spherical perspective",
    "広角レンズ": "wide angle lens, expansive view, 14mm, deep depth of field",
    "マクロレンズ": "macro lens, extreme close-up, microscopic detail, shallow depth of field",
    "望遠レンズ": "telephoto lens, compressed perspective, 200mm, beautiful background blur",
    "チルトシフトレンズ": "tilt-shift lens, miniature effect, selective focus, toy-like appearance"
}

# 1つだけ選択するセレクトボックス
selected_lens = st.selectbox(
    "使用するレンズを選択してください",
    options=["指定なし"] + list(lens_dict.keys()),
    index=0
)

# 選択されたレンズをプロンプトに追加
if selected_lens != "指定なし":
    prompt_details.append(lens_dict[selected_lens])



c1, c2, c3 = st.columns(3)
# ... (以前のコード)
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
    # 選択肢に「油絵」を追加
    style_label = [
        "日本風アニメ", "ちびキャラ", "漫画", "カートゥーン", "実写", 
        "3Dモデル(フィギュア風)", "3Dジオラマ", "粘土アニメ", "Zbrush", 
        "ホログラフィック", "Blender Render", "トゥーンレンダリング",
        "ピクセルアート", "水彩画", "油絵"  # 追加
    ]
    style = st.selectbox("画風", style_label)
    
    # 辞書に油絵のプロンプトを定義
    st_dict = {
        "日本風アニメ": "japanese cel anime style, high quality cel shading",
        "ちびキャラ": "chibi style, super deformed, cute small character",
        "漫画": "manga style, monochrome, screen tone, high contrast",
        "カートゥーン": "western cartoon style, vibrant colors, bold outlines",
        "実写": "photorealistic, 8k uhd, highly detailed, raw photo",
        "3Dモデル(フィギュア風)": "3D model, character figure, high quality resin, smooth surface, soft lighting",
        "3Dジオラマ": "miniature diorama style, tilt-shift photography, tiny detailed world, isometric view",
        "粘土アニメ": "claymation style, clay textures, stop-motion aesthetic, handmade look, Aardman style",
        "Zbrush": "Zbrush sculpt, highly detailed organic modeling, clay render, digital sculpting masterpiece",
        "ホログラフィック": "holographic display, glowing translucent blue, digital glitch, futuristic HUD, laser projection",
        "Blender Render": "rendered in Blender, Cycles render, high quality PBR materials, global illumination",
        "トゥーンレンダリング": "3D toon shaded, cel-shaded 3D, anime style 3D, Arcane style, thick strokes",
        "ピクセルアート": "pixel art, 8-bit style, retro gaming aesthetic",
        "水彩画": "watercolor painting, soft brush strokes, artistic texture",
        "油絵": "oil painting style, heavy impasto, canvas texture, visible brushstrokes, classical masterpiece aesthetic" # 追加
    }
    
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