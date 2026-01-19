import streamlit as st
# --- 簡易パスワード機能 ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "aloft1234":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # セッションから消して安全にする
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("パスワードを入力してください", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("パスワードが違います。再入力してください", type="password", on_change=password_entered, key="password")
        st.error("😕 パスワードが間違っています")
        return False
    else:
        return True

if not check_password():
    st.stop()  # パスワードが正しくない場合、これ以降のコードを実行しない
# -------------------------
import pandas as pd

# --- 1. アプリの設定とセッションの初期化 ---
st.set_page_config(page_title="画像生成プロンプトメーカーPro", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []

st.title("🎨 画像生成プロンプトメーカー Pro")
st.write("全てのカテゴリー、詳細設定、履歴管理、お気に入り機能を統合した完全版です。")

# --- 2. データ定義 ---
categories = {
    "人間・職業": ["女性", "男性", "女の子", "男の子", "勇者", "戦士", "騎士", "聖騎士(パラディン)", "僧侶", "魔術師", "賢者", "武闘家", "侍", "忍者", "暗殺者", "狩人/アーチャー", "盗賊", "吟遊詩人"],
    "動物・魔物": ["猫", "犬", "馬", "虎", "ライオン", "鷲", "龍", "狼", "グリフォン"],
    "自然・風景": ["山", "海", "森", "滝", "宇宙", "砂漠", "洞窟", "浮遊島"],
    "タイトルロゴ": ["ファンタジーゲームロゴ", "SF映画ロゴ", "ホラーゲームロゴ", "テクノロジー企業ロゴ", "ヴィンテージカフェロゴ"]
}

subject_to_en = {
    "女性": "1girl", "男性": "1boy", "女の子": "1girl, cute", "男の子": "1boy, cute",
    "勇者": "hero holding a holy sword", "戦士": "warrior with a big sword", "騎士": "knight in armor", 
    "聖騎士(パラディン)": "paladin with a shield and holy light", "僧侶": "priest holding a staff", 
    "魔術師": "wizard casting a spell", "賢者": "sage holding an ancient book", 
    "武闘家": "martial artist in fighting pose", "侍": "samurai with a katana", "忍者": "ninja in stealth suit", 
    "暗殺者": "assassin with daggers", "狩人/アーチャー": "archer with a bow", 
    "盗賊": "thief with a hood", "吟遊詩人": "bard playing a lute",
    "猫": "cat", "犬": "dog", "馬": "horse", "虎": "tiger", "ライオン": "lion", "鷲": "eagle", "龍": "dragon", "狼": "wolf", "グリフォン": "griffin",
    "山": "mountains", "海": "ocean", "森": "forest", "滝": "waterfall", "宇宙": "outer space", "砂漠": "desert", "洞窟": "cave", "浮遊島": "floating island",
    "ファンタジーゲームロゴ": "fantasy game logo, cinematic, epic, golden", 
    "SF映画ロゴ": "sci-fi movie logo, futuristic, neon, metallic", 
    "ホラーゲームロゴ": "horror game logo, dark, gothic, bloody", 
    "テクノロジー企業ロゴ": "tech company logo, sleek, minimalist, blue light", 
    "ヴィンテージカフェロゴ": "vintage cafe logo, retro, handwritten, warm colors"
}

# --- 3. サイドバー設定 ---
with st.sidebar:
    st.header("1. 基本選択")
    category = st.selectbox("カテゴリー", list(categories.keys()))
    subject = st.selectbox("具体的な被写体", categories[category])
    
    selected_skin = "指定なし"
    if category == "人間・職業":
        skin_tones = {"指定なし": "", "色白": "pale skin", "美白": "fair skin", "普通": "natural skin", "小麦色": "tan skin", "褐色": "dark skin", "日焼け": "sun-kissed skin"}
        selected_skin = st.selectbox("肌の色", list(skin_tones.keys()))

# --- 4. メイン画面：詳細設定 ---
st.header(f"2. {category}の詳細設定")
col1, col2 = st.columns(2)
prompt_details = []

if category == "人間・職業":
    with col1:
        age = st.slider("年齢層", 5, 80, 20)
        prompt_details.append(f"{age}yo {subject_to_en[subject]}")
        if selected_skin != "指定なし": prompt_details.append(skin_tones[selected_skin])
        body = st.selectbox("体型", ["指定なし", "スリム", "筋肉質", "小柄", "背が高い", "がっしりした"])
        body_dict = {"スリム": "slender", "筋肉質": "muscular", "小柄": "petite", "背が高い": "tall", "がっしりした": "athletic build"}
        if body != "指定なし": prompt_details.append(body_dict[body])
    with col2:
        hair = st.selectbox("髪型", ["指定なし", "ロング", "ショート", "ポニーテール", "ボブ", "ツインテール", "白髪", "銀髪", "金髪", "黒髪"])
        hair_dict = {"ロング": "long hair", "ショート": "short hair", "ポニーテール": "ponytail", "ボブ": "bob hair", "ツインテール": "twintails", "白髪": "white hair", "銀髪": "silver hair", "金髪": "blonde hair", "黒髪": "black hair"}
        if hair != "指定なし": prompt_details.append(hair_dict[hair])
        cloth = st.selectbox("服装の雰囲気", ["指定なし", "豪華な装飾", "ボロボロの服", "重厚な鎧", "軽装", "和服", "ローブ"])
        cloth_dict = {"豪華な装飾": "luxurious ornate clothes", "ボロボロの服": "ragged clothes", "重厚な鎧": "heavy metal armor", "軽装": "light equipment", "和服": "traditional japanese clothes", "ローブ": "magical robe"}
        if cloth != "指定なし": prompt_details.append(cloth_dict[cloth])
    face = st.selectbox("表情", ["微笑む", "キリッとした表情", "叫ぶ", "不敵な笑み", "祈る"])
    face_dict = {"微笑む": "smiling", "キリッとした表情": "determined face", "叫ぶ": "shouting", "不敵な笑み": "smirk", "祈る": "praying"}
    prompt_details.append(face_dict[face])

elif category == "動物・魔物":
    with col1:
        animal_state = st.selectbox("状態・動作", ["立っている", "歩いている", "全力疾走", "座っている", "寝ている", "咆哮している", "威嚇", "ジャンプ", "空を飛んでいる", "水の中"])
        state_dict = {"立っている": "standing", "歩いている": "walking", "全力疾走": "galloping at full speed", "座っている": "sitting", "寝ている": "sleeping", "咆哮している": "roaring", "威嚇": "intimidating stance", "ジャンプ": "jumping mid-air", "空を飛んでいる": "flying", "水の中": "swimming"}
        prompt_details.append(f"{state_dict[animal_state]} {subject_to_en[subject]}")
    with col2:
        animal_size = st.selectbox("サイズ感", ["普通の", "巨大な", "伝説級の", "手のひらサイズの"])
        size_dict = {"普通の": "", "巨大な": "huge", "伝説級の": "mythical giant", "手のひらサイズの": "tiny palm-sized"}
        if size_dict[animal_size]: prompt_details.append(size_dict[animal_size])

elif category == "自然・風景":
    with col1:
        time_of_day = st.selectbox("時間帯", ["朝", "昼", "夕暮れ", "夜", "真夜中"])
        time_dict = {"朝": "morning", "昼": "midday", "夕暮れ": "sunset", "夜": "night", "真夜中": "midnight"}
        prompt_details.append(f"{time_dict[time_of_day]} {subject_to_en[subject]}")
    with col2:
        vibe = st.selectbox("雰囲気", ["幻想的", "暗い", "平和", "荒廃した", "神秘的"])
        vibe_dict = {"幻想的": "ethereal fantasy", "暗い": "dark and gloomy", "平和": "peaceful", "荒廃した": "ruined", "神秘的": "mysterious"}
        prompt_details.append(vibe_dict[vibe])

elif category == "タイトルロゴ":
    title_text = st.text_input("ロゴに入れたいテキスト", "ADVENTURE")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        ext_map = {"指定なし": "", "極厚": "Deep extrusion", "厚め": "Thick extruded text", "巨大なブロック": "Massive block letters", "中程度": "Medium extrusion"}
        sel_ext = st.selectbox("厚み", list(ext_map.keys()))
        if ext_map[sel_ext]: prompt_details.append(ext_map[sel_ext])
        bev_map = {"指定なし": "", "彫刻風": "Chiseled", "プリズム": "Prismatic", "センターリッジ": "Center ridge", "ダイヤカット": "Diamond cut"}
        sel_bev = st.selectbox("角(ベベル)", list(bev_map.keys()))
        if bev_map[sel_bev]: prompt_details.append(f"{bev_map[sel_bev]} edges")
    with col_l2:
        font_map = {"指定なし": "", "極太サンセリフ": "Ultra-bold sans-serif", "筆文字": "Aggressive brush calligraphy", "マンガ風": "Manga sound effect", "テクノ風": "Futuristic techno"}
        sel_font = st.selectbox("フォント", list(font_map.keys()))
        if font_map[sel_font]: prompt_details.append(f"font style is {font_map[sel_font]}")
        mat_map = {"指定なし": "", "黄金": "polished gold material, mirror finish", "クローム": "chrome metal", "マグマ": "burning magma", "ネオン": "glowing neon tubes"}
        sel_mat = st.selectbox("質感", list(mat_map.keys()))
        if mat_map[sel_mat]: prompt_details.append(mat_map[sel_mat])
    prompt_details.append(f'"{title_text}" text logo')
    prompt_details.append(subject_to_en[subject])

# --- 5. 共通設定 ---
st.divider()
st.header("3. 共通設定（環境・画風・アングル）")
if category != "タイトルロゴ":
    c1, c2, c3 = st.columns(3)
    with c1:
        weather = st.selectbox("環境効果", ["指定なし", "晴れ", "雨", "雪", "霧", "魔法の光"])
        w_dict = {"指定なし": "", "晴れ": "sunny", "雨": "rainy", "雪": "snowing", "霧": "foggy", "魔法の光": "magical glowing particles"}
        if weather != "指定なし": prompt_details.append(w_dict[weather])
    with c2:
        shot = st.selectbox("距離", ["指定なし", "全身", "上半身", "アップ", "引き"])
        s_dict = {"全身": "full body shot", "上半身": "medium shot", "アップ": "close-up shot", "引き": "wide shot"}
        if shot != "指定なし": prompt_details.append(s_dict[shot])
        angle = st.selectbox("角度", ["指定なし", "正面", "俯瞰", "アオリ", "真横"])
        a_dict = {"正面": "eye level", "俯瞰": "high angle", "アオリ": "low angle", "真横": "side view"}
        if angle != "指定なし": prompt_details.append(a_dict[angle])
    with c3:
        style = st.selectbox("画風", ["アニメ風", "実写", "水彩画", "油絵", "3D"])
        st_dict = {"アニメ風": "anime style", "実写": "photorealistic", "水彩画": "watercolor", "油絵": "oil painting", "3D": "3D render"}
        prompt_details.append(st_dict[style])

picked_color = st.color_picker("メインカラー/背景色", "#ffffff")

# --- 6. 生成・お気に入り・履歴 ---
st.divider()

if st.button("✨ プロンプトを生成する", type="primary", use_container_width=True):
    p_list = prompt_details + [f"color theme {picked_color}", "masterpiece, best quality, highly detailed"]
    final_positive = ", ".join([p for p in p_list if p])
    
    if category == "タイトルロゴ":
        final_negative = "bad text, wrong font, blurry, low resolution, messy, ugly, distorted"
    else:
        final_negative = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, worst quality, low quality"

    # 履歴に保存
    st.session_state.history.insert(0, {"positive": final_positive, "negative": final_negative, "subject": subject})

    st.subheader("生成結果")
    st.code(final_positive, language="text")
    st.caption("Negative Prompt:")
    st.code(final_negative, language="text")

# --- 7. お気に入り表示 ---
st.divider()
st.header("⭐ お気に入りプロンプト")
if st.session_state.favorites:
    for idx, fav in enumerate(st.session_state.favorites):
        with st.expander(f"⭐ お気に入り {idx+1}: {fav['subject']}"):
            st.code(fav['positive'], language="text")
            if st.button(f"お気に入りから削除 (No.{idx+1})", key=f"del_fav_{idx}"):
                st.session_state.favorites.pop(idx)
                st.rerun()
    
    df = pd.DataFrame(st.session_state.favorites)
    csv = df.to_csv(index=False).encode('utf_8_sig')
    st.download_button(label="📥 お気に入りをCSVで保存", data=csv, file_name="my_prompts.csv", mime="text/csv")
else:
    st.write("お気に入りはまだありません。")

# --- 8. 履歴表示 ---
st.divider()
col_h1, col_h2 = st.columns([0.8, 0.2])
with col_h1:
    st.header("📜 プロンプト履歴")
with col_h2:
    if st.button("🗑️ 履歴を全削除", use_container_width=True):
        st.session_state.history = []
        st.rerun()

if st.session_state.history:
    for i, item in enumerate(st.session_state.history):
        with st.expander(f"履歴 {len(st.session_state.history)-i}: {item['subject']}"):
            st.code(item['positive'], language="text")
            if st.button(f"⭐ お気に入りに追加", key=f"fav_btn_{i}"):
                if item not in st.session_state.favorites:
                    st.session_state.favorites.append(item)
                    st.toast("お気に入りに追加しました！")
                else:
                    st.toast("既に登録済みです")
                st.rerun()
else:
    st.write("履歴はまだありません。")