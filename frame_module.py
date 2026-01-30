import streamlit as st

def get_frame_settings():
    st.subheader("🖼️ フレームデザイン設定")
    res = []
    
    # フレームのみに集中させるための指示
    res.append("empty frame center, blank middle, white background in the center, frame only design, no contents inside")

    col1, col2 = st.columns(2)
    
    with col1:
        # ① アスペクト比
        st.write("**1. アスペクト比の設定**")
        ratio_type = st.radio("比率の選択", ["標準 (1:1)", "横長 (16:9)", "縦長 (9:16)", "カスタム"], index=0)
        
        if ratio_type == "カスタム":
            w = st.number_input("幅", value=1920)
            h = st.number_input("高さ", value=1080)
            res.append(f"aspect ratio {w}:{h}")
        else:
            r_dict = {"標準 (1:1)": "1:1 ratio", "横長 (16:9)": "16:9 ratio", "縦長 (9:16)": "9:16 ratio"}
            res.append(r_dict[ratio_type])

        # ② 物理形状
        st.write("**2. フレームの物理形状**")
        frame_width = st.select_slider("フレームの幅", options=["極細", "細め", "標準", "太め", "極太"], value="標準")
        w_en = {"極細": "very thin", "細め": "thin", "標準": "medium", "太め": "thick", "極太": "heavy wide"}
        
        frame_depth = st.selectbox("立体感（厚み）", ["平面的な枠", "少し立体的な枠", "重厚な彫刻の厚み"])
        d_en = {"平面的な枠": "flat frame", "少し立体的な枠": "3D beveled frame", "重厚な彫刻の厚み": "deeply embossed heavy frame"}
        
        res.append(f"{w_en[frame_width]} border, {d_en[frame_depth]}")

    with col2:
        # ③ デザインスタイル
        st.write("**3. デザインスタイル**")
        style = st.selectbox("デザインスタイル", [
            "指定なし", "パチンコ・パチスロ（遊技機スタイル）", "豪華な金縁（バロック）", "シンプルモダン", 
            "和風（木製・漆）", "近未来（LED/メカニカル）", "アンティーク・ヴィンテージ", 
            "ファンタジー（石像・ツタ）", "トランプ/カード風"
        ])
        
        s_dict = {
            "指定なし": "simple border frame",
            "パチンコ・パチスロ（遊技機スタイル）": "pachinko machine frame design, flashy japanese gambling machine aesthetic, neon glowing chrome, luxury parlor style",
            "豪華な金縁（バロック）": "ornate gold luxury frame, baroque style, intricate carvings",
            "シンプルモダン": "minimalist sleek modern frame, solid color, matte finish",
            "和風（木製・漆）": "traditional japanese wood frame, lacquered finish",
            "近未来（LED/メカニカル）": "sci-fi mechanical frame, glowing LED strips, techwear aesthetic",
            "アンティーク・ヴィンテージ": "distressed vintage wooden frame, aged texture",
            "ファンタジー（石像・ツタ）": "ancient stone frame, overgrown vines and moss",
            "トランプ/カード風": "trading card game frame design, decorative border without illustration"
        }
        res.append(s_dict[style])

        # ④ 質感（マテリアル） - 新規追加！
        st.write("**4. 質感（マテリアル）**")
        texture = st.selectbox("フレームの質感", [
            "指定なし", "磨き上げられた金属", "純金", "クリスタル・宝石", "半透明ガラス", 
            "燃え盛る炎", "流れる水", "液体金属", "ネオン・エネルギー", "漆黒の黒曜石"
        ])
        
        t_dict = {
            "指定なし": "",
            "磨き上げられた金属": "polished metallic texture, chrome finish",
            "純金": "solid gold texture, 24k gold, shiny metallic",
            "クリスタル・宝石": "shimmering crystal, refractive gemstone material",
            "半透明ガラス": "translucent glass, frosted texture, refraction",
            "燃え盛る炎": "made of raging fire and flames, glowing embers",
            "流れる水": "made of flowing liquid water, splashing droplets",
            "液体金属": "liquid mercury, molten silver, flowing metallic",
            "ネオン・エネルギー": "energy beam, glowing neon, plasma",
            "漆黒の黒曜石": "dark obsidian, polished volcanic glass, black reflective"
        }
        if t_dict[texture]:
            res.append(t_dict[texture])

        is_inner_shadow = st.checkbox("内側に影を入れる (Inner shadow)")
        if is_inner_shadow:
            res.append("inner shadow, depth effect")

    res.insert(0, "a standalone decorative frame")
    res.append("clear center, no portrait, no landscape, empty canvas inside")
    
    return res, ratio_type, style, texture