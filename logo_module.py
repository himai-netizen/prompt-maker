import streamlit as st

def get_logo_settings(subject_en):
    st.subheader("🔡 ロゴデザイン詳細")
    text = st.text_input("ロゴに入れたいテキスト", "ADVENTURE")
    col1, col2 = st.columns(2)
    res = [f'"{text}" text logo', subject_en]
    with col1:
        ext = st.selectbox("厚み", ["指定なし", "極厚", "厚め", "巨大なブロック", "中程度"])
        e_dict = {"極厚": "Deep extrusion", "厚め": "Thick extruded text", "巨大なブロック": "Massive block letters", "中程度": "Medium extrusion"}
        if ext != "指定なし": res.append(e_dict[ext])
        bev = st.selectbox("角(ベベル)", ["指定なし", "彫刻風", "プリズム", "センターリッジ", "ダイヤカット"])
        b_dict = {"彫刻風": "Chiseled", "プリズム": "Prismatic", "センターリッジ": "Center ridge", "ダイヤカット": "Diamond cut"}
        if bev != "指定なし": res.append(f"{b_dict[bev]} edges")
    with col2:
        font = st.selectbox("フォント", ["指定なし", "極太サンセリフ", "筆文字", "マンガ風", "テクノ風", "軍用ステンシル"])
        f_dict = {"極太サンセリフ": "Ultra-bold sans-serif", "筆文字": "Aggressive brush calligraphy", "マンガ風": "Manga sound effect", "テクノ風": "Futuristic techno", "軍用ステンシル": "Military stencil"}
        if font != "指定なし": res.append(f"font style is {f_dict[font]}")
        mat = st.selectbox("質感", ["指定なし", "黄金", "クローム", "マグマ", "ネオン", "ダイヤモンド", "氷"])
        m_dict = {"黄金": "polished gold material", "クローム": "chrome shiny metal", "マグマ": "burning magma", "ネオン": "glowing neon tubes", "ダイヤモンド": "diamond refractive crystal", "氷": "transparent clear ice"}
        if mat != "指定なし": res.append(m_dict[mat])
    return res, text