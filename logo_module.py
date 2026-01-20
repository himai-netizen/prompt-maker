import streamlit as st

def get_logo_settings(subject_en):
    st.subheader("🔡 ロゴデザイン詳細")
    text = st.text_input("ロゴに入れたいテキスト", "ADVENTURE")
    col1, col2 = st.columns(2)
    
    # 透過を意識して「浮き出た」感じを出すプロンプトを基礎に
    res = [f'"{text}" text logo', subject_en, "centered composition"]
    
    with col1:
        ext = st.selectbox("厚み", ["指定なし", "極厚", "厚め", "中程度"])
        e_dict = {"極厚": "Deep 3D extrusion", "厚め": "Thick extruded", "中程度": "Medium extrusion"}
        if ext != "指定なし": res.append(e_dict[ext])
        
        bev = st.selectbox("角(ベベル)", ["指定なし", "彫刻風", "センターリッジ", "ダイヤカット"])
        b_dict = {"彫刻風": "Chiseled", "センターリッジ": "Center ridge", "ダイヤカット": "Diamond cut"}
        if bev != "指定なし": res.append(f"{b_dict[bev]} edges")

    with col2:
        font = st.selectbox("フォント", ["指定なし", "極太サンセリフ", "筆文字", "テクノ風"])
        f_dict = {"極太サンセリフ": "Ultra-bold sans-serif font", "筆文字": "Aggressive brush calligraphy", "テクノ風": "Futuristic techno font"}
        if font != "指定なし": res.append(f_dict[font])
        
        mat = st.selectbox("質感", ["指定なし", "黄金", "クローム", "マグマ", "ネオン", "氷"])
        m_dict = {"黄金": "polished gold material", "クローム": "chrome shiny metal", "マグマ": "molten magma", "ネオン": "glowing neon", "氷": "clear ice"}
        if mat != "指定なし": res.append(m_dict[mat])
        
    return res, text