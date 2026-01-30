import streamlit as st

def get_frame_settings():
    st.subheader("🖼️ 純粋装飾フレーム設定")
    res = []
    
    # 強力な指示：外側の「箱」を消し、装飾だけで形を作る
    res.append("no outer rectangular box, frame made purely of ornaments, decorative borders only, transparent-ready composition, isolated on white background")

    col1, col2 = st.columns(2)
    
    with col1:
        # ① 形状の定義
        st.write("**1. 装飾の構成形状**")
        frame_shape = st.selectbox("全体の形状", ["長方形 (Rectangular)", "円形 (Circular)", "オーバル (Oval)", "不規則な装飾塊 (Irregular Ornate)"])
        shape_en = {
            "長方形 (Rectangular)": "rectangular arrangement",
            "円形 (Circular)": "circular wreath shape",
            "オーバル (Oval)": "oval elegant border",
            "不規則な装飾塊 (Irregular Ornate)": "asymmetrical ornate clusters, organic decorative shape"
        }
        res.append(f"a {shape_en[frame_shape]} made of decorations")

        # ② 装飾の密度
        st.write("**2. 装飾の密度・ボリューム**")
        density = st.select_slider("装飾の密度", options=["シンプル", "適度", "豪華", "圧倒的"], value="豪華")
        dens_en = {
            "シンプル": "minimalist decorative accents",
            "適度": "moderate detailing",
            "豪華": "highly ornate, intricate filigree",
            "圧倒的": "maximalist, overflowing decorative elements, hyper-detailed"
        }
        res.append(dens_en[density])

    with col2:
        # ③ デザインスタイル（遊技機スタイルを強化）
        st.write("**3. デザインスタイル**")
        style = st.selectbox("デザインスタイル", [
            "指定なし", "パチンコ・パチスロ（遊技機演出）", "中世ヨーロッパ（彫刻）", 
            "アール・ヌーヴォー（曲線美）", "メカニカル・サイバー", "自然（蔦・花）"
        ])
        
        s_dict = {
            "指定なし": "decorative border",
            "パチンコ・パチスロ（遊技機演出）": "pachinko visual effect frame, explosive light energy, spinning chrome parts, floating 3D metallic ornaments, flashing LED borders",
            "中世ヨーロッパ（彫刻）": "rococo gold carvings, acanthus leaf ornaments, vintage scrollwork",
            "アール・ヌーヴォー（曲線美）": "art nouveau flowing lines, elegant organic curves, symmetrical filigree",
            "メカニカル・サイバー": "sci-fi hard surface details, mechanical joints, glowing circuitry, tech-frame",
            "自然（蔦・花）": "intertwined thorny vines, botanical decorations, floral wreath"
        }
        res.append(s_dict[style])

        # ④ 質感
        st.write("**4. 質感（マテリアル）**")
        texture = st.selectbox("マテリアル", ["磨き上げられた金", "鏡面クローム", "クリスタル", "エネルギー体", "氷", "液体"])
        t_dict = {
            "磨き上げられた金": "shining 24k gold, metallic luster",
            "鏡面クローム": "polished chrome, high reflection, silver metal",
            "クリスタル": "transparent crystal, diamond-like refraction",
            "エネルギー体": "pure glowing energy, plasma, electric aura",
            "氷": "frozen ice, translucent frost, cold blue crystal",
            "液体": "liquid splashing, water droplets, flowing form"
        }
        res.append(t_dict[texture])

    # 最終仕上げ：中身に何も描かせない指示を最優先に
    res.insert(0, "white empty center, absolute blank space in middle, floating decorative elements")
    res.append("white background, isolated, high contrast, concept art for border assets")
    
    return res, frame_shape, style, texture