import streamlit as st
import pandas as pd
import os
import getpass
from deep_translator import GoogleTranslator
import human_module
import animal_module
import landscape_module
import logo_module
import frame_module  # 追加

def custom_to_en(text_ja):
    # ここに実際の翻訳処理が入っているか確認
    # もし単に 'return text_ja' となっていると、日本語のまま返ってしまいます
    from deep_translator import GoogleTranslator
    translated = GoogleTranslator(source='ja', target='en').translate(text_ja)
    return translated


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
    "タイトルロゴ": ["ファンタジーロゴ", "SFロゴ", "ホラーロゴ", "企業ロゴ", "ヴィンテージロゴ"],
    "フレームデザイン": ["額縁", "カード枠", "ウィンドウ"] 
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

# 体型の定義
body_types = {
   "指定なし": "",
   "スリム": "slender, slim build",
   "痩せ型": "thin, skinny",
   "アスリート": "athletic, toned body",
   "筋肉質": "muscular, ripped physique",
   "ふくよか": "plump, curvy figure",
   "がっしり": "sturdy, thick build",
   "モデル体型": "tall, lean model proportions"
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
        selected_body = st.selectbox("体型", list(body_types.keys())) # 追加

# --- 4. 詳細設定 ---
st.title("🎨 AIプロンプト作成メーカー")
st.header(f"2. {category}の詳細設定")

# タブの作成
tab1, tab2 = st.tabs(["⚙️ 詳細カスタマイズ", "🏷️ クイックタグ・パレット"])

prompt_details = []
history_title = subject 

with tab1:
    if category == "人間":
        # 戻り値の数に合わせて受け取りを修正（res, age, f_style, cloth）
        res, age, f_style, cloth = human_module.get_human_settings(subject_to_en[subject])
        prompt_details.extend(res)
        
        # 国籍・肌の色・体型を追加（サイドバーの設定を反映）
        if selected_skin != "指定なし": prompt_details.append(skin_tones[selected_skin])
        if selected_nat != "指定なし": prompt_details.append(nationalities[selected_nat])
        if selected_body != "指定なし": prompt_details.append(body_types[selected_body])  
      
        # 履歴タイトルに反映
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

    elif category == "フレームデザイン":
    # texture を追加して4つの戻り値を受け取るように修正
        res, ratio, style, texture = frame_module.get_frame_settings()
        prompt_details.extend(res)
        history_title = f"Frame: {ratio} / {style} / {texture}"

with tab2:
# --- タグの一括削除ボタンを追加 ---
    if st.session_state.custom_keywords:
        if st.button("🗑️ 全てのクイックタグをクリア", use_container_width=True):
            st.session_state.custom_keywords = []
            st.toast("タグをすべて削除しました")
            st.rerun()
        st.divider()
    
    st.info("使いたい雰囲気（タグ）をクリックすると、自動で英語に変換してカスタムキーワードに追加されます。")
    
    # クイックタグの定義（表示名: 英語プロンプト）
    tag_categories = {
	    "🇯🇵 日本の伝統画風": {
	            "浮世絵": "Ukiyo-e style, woodblock print, traditional japanese art",
	            "水墨画": "Suibokuga, ink wash painting, sumi-e, Zen aesthetic",
	            "金箔画": "Kinpaku-ga, gold leaf background, japanese gold foil art, opulent",
	            "墨画": "Sumi-e, traditional japanese ink drawing, expressive brushwork",
	            "大和絵": "Yamato-e style, classical japanese painting, soft colors",
	            "日本画": "Nihonga style, traditional japanese pigments, mineral pigments",
	            "屏風絵": "Byobu-e, japanese folding screen painting style",
	            "襖絵": "Fusuma-e, japanese sliding door painting style",
	            "絵巻物": "Emakimono, japanese horizontal handscroll painting style"
        },
        "💡 演出・光の魔法": {
            "映画のような照明": "Cinematic Lighting",
            "天使の梯子": "God rays",
            "ネオンの輝き": "Neon glow",
            "夕暮れの黄金色": "Golden hour",
            "逆光": "Backlighting",
            "柔らかい光": "Soft lighting",
            "ドラマチックな影": "Dramatic shadows",
            "幻想的な光の粒": "Magical sparkling bokeh"
        },
        "💎 圧倒的な画質": {
            "最高傑作": "Masterpiece",
            "超詳細な描き込み": "Highly detailed, Intricate details",
            "実写のような": "Photorealistic",
            "UE5レンダリング": "Unreal Engine 5 render",
            "8k解像度": "8k resolution",
            "3Dフィギュア風": "Octane render",
            "繊細な質感": "Sharp focus, hyper-realistic texture"
        },
        "🎭 世界観・ムード": {
            "神秘的・優美": "Ethereal, Mystical",
            "ダークファンタジー": "Dark fantasy, Gothic atmosphere",
            "サイバーパンク": "Cyberpunk, Futuristic neon",
            "レトロ写真風": "Vintage photography style",
            "夢幻的・淡い": "Dreamy, Pastel colors",
            "終末世界": "Post-apocalyptic, Desolate",
            "スチームパンク": "Steampunk, Brass and Steam",
            "鮮やかな色彩": "Vibrant colors, High saturation"
        },
        "📸 構図・カメラ": {
            "躍動感のある構図": "Dynamic angle",
            "アップ（顔寄り）": "Close-up shot",
            "全身ショット": "Full body shot",
            "ローアングル": "Low angle, Heroic perspective",
            "俯瞰（上から）": "Bird's eye view",
            "左右対称": "Symmetrical composition",
            "広角レンズ": "Wide angle shot"
        },
        "✨ 特殊エフェクト": {
            "キラキラ・粒子": "Shimmering particles",
            "水しぶき": "Water splashes",
            "燃え盛る炎": "Swirling flames",
            "花吹雪": "Falling flower petals",
            "デジタルノイズ": "Glitch effect",
            "浮遊感": "Floating object, Zero gravity"
        },
    	"💇 髪型（男性向け）": {
    	    "短髪": "short hair",
    	    "ツーブロック": "undercut",
    	    "マッシュ": "mushroom cut",
    	    "オールバック": "slicked back",
    	    "坊主": "buzz cut",
    	    "モヒカン": "mohawk"
   	 },
   	 "💇 髪型（女性向け）": {
   	     "ロングヘア": "long hair",
   	     "ポニーテール": "ponytail",
   	     "ツインテール": "twintails",
   	     "ボブ": "bob cut",
   	     "姫カット": "hime cut",
   	     "ハーフアップ": "half-up"
  	  },
    "✨ 髪質・質感": {
   	     "サラサラ": "silky smooth hair",
   	     "つやつや": "glossy hair",
   	     "濡れ髪": "wet hair",
   	     "透明感のある髪": "translucent hair",
   	     "ウェーブ": "wavy hair"
    }
    }

    # カテゴリごとにボタンを配置
    for cat_name, tags_dict in tag_categories.items():
        st.write(f"**{cat_name}**")
        # 5列に増やして、より多くのタグを並べやすくします
        cols = st.columns(5) 
        for i, (label_ja, tag_en) in enumerate(tags_dict.items()):
            if cols[i % 5].button(label_ja, key=f"quick_{tag_en}"):
                # セッション状態のカスタムキーワードリストに追加（英語の方を入れる）
                if tag_en not in st.session_state.custom_keywords:
                    st.session_state.custom_keywords.append(tag_en)
                    st.toast(f"追加: {label_ja} ({tag_en})")
                    st.rerun()
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

# --- 6.5 追加オプション ---
st.subheader("💡 出力オプション")
col_opt1, col_opt2 = st.columns(2)

with col_opt1:
    idea_mode = st.checkbox("4分割アイデアモード（番号付き4案）")

with col_opt2:
    use_negative = st.checkbox("ネガティブプロンプトを適用")

# セッション状態の初期化
if "neg_custom_keywords" not in st.session_state:
    st.session_state.neg_custom_keywords = []

negative_content = ""
if use_negative:
    # 1. プリセット
    neg_options = {
        "低品質": "low quality, worst quality, lowres",
        "解剖学的異常（手足の崩れ）": "bad anatomy, missing fingers, extra digit, fewer digits",
        "文字・ロゴの混入": "text, letter, signature, watermark, username",
        "ぼやけ・ノイズ": "blurry, error, cropped, jpeg artifacts",
        "不自然な顔": "deformed face, disfigured, mutated"
    }
    selected_neg_labels = st.multiselect(
        "除外したい要素を選択（日本語）",
        options=list(neg_options.keys()),
        default=["低品質", "文字・ロゴの混入"]
    )
    
    # 2. 自由入力欄
    st.write("追加の除外ワード（個別入力 例：メガネ、帽子、背景の建物）")
    neg_col_in, neg_col_btn = st.columns([0.7, 0.3])
    
    with neg_col_in:
        neg_input_ja = st.text_input("日本語で入力してください", key="neg_input_field", label_visibility="collapsed")
    
    with neg_col_btn:
        if st.button("翻訳して追加", key="neg_add_btn", use_container_width=True):
            if neg_input_ja:
                # --- 翻訳ロジックを直接実行 ---
                try:
                    # ポジティブ側で使っている翻訳関数を呼び出す
                    # もし関数名が違う場合はここを修正してください
                    neg_en = custom_to_en(neg_input_ja)
                    
                    # 確実に英語（翻訳後）を保存する
                    if neg_en and neg_en not in st.session_state.neg_custom_keywords:
                        st.session_state.neg_custom_keywords.append(neg_en)
                        st.rerun()
                except Exception as e:
                    st.error(f"翻訳エラー: {e}")

    # 3. 英語（翻訳後）でキーワードを表示
    if st.session_state.neg_custom_keywords:
        st.write("現在ストックされている除外キーワード（英語）:")
        cols_neg = st.columns(4)
        for idx, kw in enumerate(st.session_state.neg_custom_keywords):
            # kw が英語になっていることを確認して表示
            if cols_neg[idx % 4].button(f"❌ {kw}", key=f"remove_neg_{idx}"):
                st.session_state.neg_custom_keywords.remove(kw)
                st.rerun()

    # --- ネガティブプロンプト全体の組み立て ---
    final_neg_list = [neg_options[label] for label in selected_neg_labels]
    final_neg_list.extend(st.session_state.neg_custom_keywords)
    
    if final_neg_list:
        negative_content = f" [Negative Prompt: {', '.join(final_neg_list)}]"


# --- 7. 生成ボタン ---
st.divider()
if st.button("✨ プロンプト生成", type="primary", use_container_width=True):
    final_prompt_list = prompt_details.copy()
    
    # 4分割モード
    if idea_mode:
        final_prompt_list.append("split into 4 separate views, quadrant layout, numbered 1 2 3 4 on each frame, 4 different design concepts")
    
    # 通常のカスタムキーワード（日本語→英語）
    if "custom_keywords" in st.session_state and st.session_state.custom_keywords:
        final_prompt_list.extend(st.session_state.custom_keywords)
        
    final_prompt_list.append(f"color theme {picked_color}")
    final_prompt_list.append("masterpiece, best quality, highly detailed")
    
    # メインとネガティブを合体
    full_prompt = ", ".join(final_prompt_list) + negative_content
    
    # 履歴保存
    new_entry = pd.DataFrame([{
        "日付": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
        "タイトル": history_title,
        "プロンプト": full_prompt
    }])
    st.session_state.history = pd.concat([new_entry, st.session_state.history], ignore_index=True)
    
    st.balloons()
    st.success("プロンプトを生成しました！")
    st.code(full_prompt)

# --- 8. 履歴表示・お気に入り・CSV書き出し ---
st.divider()
st.header("📜 生成履歴と管理")

if isinstance(st.session_state.history, pd.DataFrame) and not st.session_state.history.empty:
    
    # --- CSVダウンロードボタン ---
    csv = st.session_state.history.to_csv(index=False).encode('utf_8_sig')
    st.download_button(
        label="📥 履歴をCSVとしてダウンロード",
        data=csv,
        file_name=f"prompt_history_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

    # --- 履歴の表示と「お気に入り」登録機能 ---
    st.subheader("履歴一覧")
    # 履歴を1行ずつループして、横に「お気に入り」ボタンを配置
    for i, row in st.session_state.history.iterrows():
        cols = st.columns([0.1, 0.2, 0.5, 0.2])
        with cols[0]:
            st.write(f"{len(st.session_state.history)-i}") # 番号
        with cols[1]:
            st.write(row["タイトル"])
        with cols[2]:
            st.text_small = st.code(row["プロンプト"])
        with cols[3]:
            if st.button("⭐ お気に入り", key=f"fav_{i}"):
                if row["プロンプト"] not in [f["プロンプト"] for f in st.session_state.favorites]:
                    st.session_state.favorites.append(row.to_dict())
                    st.toast(f"「{row['タイトル']}」をお気に入りに保存しました！")
                else:
                    st.toast("既にお気に入りに登録されています。")

    # --- お気に入りセクション ---
    if st.session_state.favorites:
        st.divider()
        st.subheader("⭐ お気に入り済みプロンプト")
        fav_df = pd.DataFrame(st.session_state.favorites)
        st.dataframe(fav_df, use_container_width=True)
        if st.button("お気に入りをクリア"):
            st.session_state.favorites = []
            st.rerun()

    # --- 履歴クリア ---
    st.divider()
    if st.button("履歴をすべて削除", type="secondary"):
        st.session_state.history = pd.DataFrame(columns=["日付", "タイトル", "プロンプト"])
        st.rerun()

else:
    st.info("履歴はまだありません。")