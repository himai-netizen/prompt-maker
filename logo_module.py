import streamlit as st

def get_logo_settings(subject_en):
    st.subheader("🔡 遊技機風ロゴデザイン詳細")
    
    # 1. テキスト入力
    # 説明文を変更：スペースではなくスラッシュでの区切りを案内
    text_input = st.text_input("ロゴに入れたいテキスト（改行したい場所に / を入力）", "ADVENTURE/world")
    
    # --- 複数行レイアウトの切り替え ---
    # ラベルを変更
    is_stacked = st.checkbox("記号「/」で区切って改行・積み重ね配置にする (Stacked Layout)")
    
    # 2. 詳細設定（並び方向・文字のまとまり）
    col_txt1, col_txt2 = st.columns(2)
    
    with col_txt1:
        direction = st.radio(
            "文字の並び方向", 
            ["横並び (Horizontal)", "縦並び (Vertical)"],
            index=0,
            help="通常は横並び推奨。縦書き看板などの場合に縦並びを選択。"
        )
    
    with col_txt2:
        composition = st.radio(
            "文字のまとまり", 
            ["一列・塊で配置 (Grouped)", "一文字ずつ分離・散らす (Split/Scattered)"],
            index=0
        )

    # --- プロンプト構築ロジック ---
    res = []
    
    # A. テキストの処理（スラッシュ区切りで2行積み重ね vs 1行）
    if is_stacked and "/" in text_input:
        # スラッシュで分割
        parts = text_input.split("/")
        # 空白文字の前後の余分なスペースは除去しつつ、中身のスペースは保持
        parts = [p.strip() for p in parts if p.strip()] 
        
        if len(parts) >= 2:
            # 例: text logo containing "THE WORLD" and "OF MAGIC"
            text_content = " and ".join([f'"{p}"' for p in parts])
            res.append(f'text logo containing {text_content}')
            
            # 積み重ねの指示
            res.append(f"{len(parts)} lines stacked text layout")
            res.append("text written above text")
            res.append("balanced typography composition")
        else:
            # スラッシュがあっても実質1行だった場合
            res.append(f'"{text_input.replace("/", "")}" text logo')
    else:
        # 積み重ねない場合（1行）またはスラッシュがない場合
        # スラッシュがもし残っていたら削除して表示
        clean_text = text_input.replace("/", "")
        
        # 文字の分離設定を確認
        final_text_str = clean_text
        if "分離" in composition:
            # 分離の場合はスペースを空けて個別の文字として認識させる
            # "THE WORLD" -> "T H E   W O R L D" のようにする処理
            # 文字列を一文字ずつリスト化し、結合
            final_text_str = " ".join(list(clean_text))
            res.append("separated individual letters, deconstructed typography, floating characters")
        else:
            res.append("contiguous text, single word logo, tight kerning")
            
        res.append(f'"{final_text_str}" text logo')

    res.append(subject_en)

    # B. 並び方向の指定
    if "縦並び" in direction:
        res.append("vertical text layout, vertically stacked letters, top-to-bottom flow")
    else:
        res.append("horizontal reading direction")
        if not is_stacked:
            res.append("centered composition")

    # -------------------------------------------------
    # 以下、既存の装飾設定
    # -------------------------------------------------
    
    col1, col2 = st.columns(2)
    
    # 変数の初期化
    shape_label = "指定なし"
    material_label = "指定なし"
    world_label = "指定なし"

    with col1:
        # 1. 形状・立体感
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

        # --- 中央を尖らせるオプション ---
        st.write("---")
        is_sharp = st.checkbox("中央を鋭利にとがらせる (Sharp Center)")
        if is_sharp:
            sharp_keywords = "Sharp, Pointy, Spike, Apex, Geometric, Minimalist logo of a sharp, A diamond-shaped, 3D futuristic logo with a sharp peak in the center"
            res.append(sharp_keywords)

    # 共通のベース呪文
    res.append("Pachinko style logo style, masterpiece, best quality")
    
    return res, text_input, shape_label, world_label, material_label