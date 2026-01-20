import streamlit as st

def get_logo_settings(subject_en):
    st.subheader("🔡 遊技機風ロゴデザイン詳細")
    text = st.text_input("ロゴに入れたいテキスト", "ADVENTURE")
    
    col1, col2 = st.columns(2)
    res = [f'"{text}" text logo', subject_en, "centered composition"]
    
    # 変数の初期化（エラー防止）
    shape_label = "指定なし"
    material_label = "指定なし"
    world_label = "指定なし"

    with col1:
        # 1. 形状・構成
        shape_label = st.selectbox("形状・立体感", [
            "指定なし", "3D飛び出し効果", "太い面取り", "多層構造", "動的なパース", "放射線状の広がり"
        ])
        s_dict = {
            "3D飛び出し効果": "3D extrusion, pop-out effect, depth",
            "太い面取り": "thick bevel, bold edges",
            "多層構造": "multi-layered design, bezel design",
            "動的なパース": "dynamic perspective, isometric view",
            "放射線状の広がり": "radical lines, explosive composition"
        }
        if shape_label != "指定なし":
            res.append(s_dict[shape_label])

        # 2. 質感・マテリアル
        material_label = st.selectbox("質感・マテリアル", [
            "指定なし", "磨き上げられた金", "鏡面クローム", "金属の質感", "光沢仕上げ"
        ])
        m_dict = {
            "磨き上げられた金": "polished gold texture, luxury metallic",
            "鏡面クローム": "chrome shiny metal, high reflection",
            "金属の質感": "heavy metallic texture, industrial steel",
            "光沢仕上げ": "glossy finish, ray tracing, reflective"
        }
        if material_label != "指定なし":
            res.append(m_dict[material_label])

        # 3. エフェクト
        effect = st.selectbox("エフェクト", ["指定なし", "ネオンの輝き", "LEDバックライト", "電撃・火花", "ガラスの破片"])
        e_dict = {
            "ネオンの輝き": "neon glowing edges", 
            "LEDバックライト": "LED lighting",
            "電撃・火花": "electric sparks", 
            "ガラスの破片": "shattered glass"
        }
        if effect != "指定なし":
            res.append(e_dict[effect])

    with col2:
        # 4. 世界観・ジャンル
        world_label = st.selectbox("世界観・ジャンル", [
            "王道・豪華（Pachinko Style）", "近未来・SF", "和風・墨絵", "萌え系・ポップ", "ホラー・ダーク"
        ])
        w_dict = {
            "王道・豪華（Pachinko Style）": "Luxury, Royal, Golden, Baroque style",
            "近未来・SF": "Cyberpunk, Sci-fi, Holographic",
            "和風・墨絵": "Japanese style, Sumi-e",
            "萌え系・ポップ": "Vibrant anime colors, Pop and Cute",
            "ホラー・ダーク": "Dark fantasy, Gothic, Blood splash"
        }
        res.append(w_dict[world_label])

        # 5. 品質
        quality = st.selectbox("レンダリング品質", ["最高級（UE5/Octane）", "グラフィックデザイン重視", "高コントラスト"])
        q_dict = {
            "最高級（UE5/Octane）": "Unreal Engine 5, Octane Render, 8k",
            "グラフィックデザイン重視": "Vector style, Sharp edges",
            "高コントラスト": "high contrast, vivid colors"
        }
        res.append(q_dict[quality])

    # 共通のベース呪文
    res.append("Pachinko style logo style, masterpiece, best quality")
    
    # 重要：app.pyが期待する5つの戻り値を確実に返す
    return res, text, shape_label, world_label, material_label