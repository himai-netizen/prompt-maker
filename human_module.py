import streamlit as st

def get_human_settings(subject_en):
    res = []
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("年齢層", 5, 80, 20)
        res.append(f"{age}yo {subject_en}")
        
        # 「職種（現代・専門）」を追加
        f_style = st.selectbox("ファッションスタイル", 
            ["現代カジュアル", "ビジネス/フォーマル", "職種（現代・専門）", "ファンタジー/RPG職種", "和装", "サイバーパンク"]
        )
        
        if f_style == "現代カジュアル":
            cloth = st.selectbox("衣装", ["指定なし", "Tシャツとジーンズ", "パーカー", "夏服ワンピース", "レザージャケット", "カーディガン"])
            c_en_dict = {"指定なし": "", "Tシャツとジーンズ": "t-shirt and blue jeans", "パーカー": "hoodie", "夏服ワンピース": "summer dress", "レザージャケット": "leather jacket", "カーディガン": "cardigan"}
            c_en = c_en_dict[cloth]
        
        elif f_style == "ビジネス/フォーマル":
            cloth = st.selectbox("衣装", ["指定なし", "ビジネススーツ", "タキシード", "イブニングドレス", "白シャツとスラックス"])
            c_en_dict = {"指定なし": "", "ビジネススーツ": "business suit", "タキシード": "tuxedo", "イブニングドレス": "evening gown", "白シャツとスラックス": "white shirt and slacks"}
            c_en = c_en_dict[cloth]
        
        elif f_style == "職種（現代・専門）": # ← 新規追加セクション
            cloth = st.selectbox("役職/制服", ["指定なし", "警官", "医者", "ナース", "消防士", "弁護士", "パイロット", "ビジネスマン/ウーマン"])
            c_en_dict = {
                "指定なし": "",
                 "警官": "police officer uniform, badge, tactical vest",
                 "医者": "doctor, white lab coat, stethoscope",
                 "ナース": "nurse uniform, medical scrubs",
                 "消防士": "firefighter gear, fireproof suit, helmet",
                 "弁護士": "lawyer, professional business suit, formal attire",
                 "パイロット": "airline pilot uniform, captain's hat",
                 "ビジネスマン/ウーマン": "modern office wear, professional suit"
            }
            c_en = c_en_dict[cloth]

        elif f_style == "ファンタジー/RPG職種":
            cloth = st.selectbox("役職/装備", ["指定なし", "騎士の鎧", "魔術師のローブ", "聖職者の服", "忍び装束", "侍の甲冑", "盗賊の軽装", "修道女/シスター", "冒険者"])
            c_en_dict = {
                "指定なし": "",
                 "騎士の鎧": "knight armor, plate mail, engraved steel", 
                 "魔術師のローブ": "wizard robes, mystical cloak", 
                 "聖職者の服": "cleric vestments", 
                 "忍び装束": "ninja outfit", 
                 "侍の甲冑": "samurai armor", 
                 "盗賊の軽装": "thief gear",
                 "修道女/シスター": "nun habit, rosary",
                 "冒険者": "fantasy adventurer gear, leather armor"
            }
            c_en = c_en_dict[cloth]
            
        elif f_style == "和装":
            cloth = st.selectbox("衣装", ["指定なし", "着物", "浴衣", "袴", "巫女装束"])
            c_en_dict = {"指定なし": "", "着物": "kimono", "浴衣": "yukata", "袴": "hakama", "巫女装束": "miko outfit"}
            c_en = c_en_dict[cloth]
            
        else: # サイバーパンク
            cloth = st.selectbox("衣装", ["指定なし", "ネオンジャケット", "タクティカルベスト", "サイバネティックウェア"])
            c_en_dict = {"指定なし": "", "ネオンジャケット": "neon glowing jacket", "タクティカルベスト": "tactical vest", "サイバネティックウェア": "cybernetic techwear"}
            c_en = c_en_dict[cloth]
        
        if c_en:
            res.append(c_en)

    with col2:
        status = st.selectbox("衣装の状態", ["新品同様", "着古した", "汚れた", "ボロボロ", "血に染まった"])
        res.append({"新品同様": "brand new, clean", "着古した": "worn-in", "汚れた": "dirty", "ボロボロ": "tattered, weathered", "血に染まった": "blood-stained"}[status])
        
        # 髪質 - 新規追加
        hair_texture = st.selectbox("髪質", ["指定なし", "ストレート", "ウェーブ", "巻き髪", "サラサラ", "つやつや", "濡れ髪", "ボサボサ", "剛毛", "猫っ毛"])
        ht_en_dict = {
            "指定なし": "",
            "ストレート": "straight hair",
            "ウェーブ": "wavy hair",
            "巻き髪": "curly hair",
            "サラサラ": "silky smooth hair",
            "つやつや": "glossy hair",
            "濡れ髪": "wet hair",
            "ボサボサ": "messy hair",
            "剛毛": "thick coarse hair",
            "猫っ毛": "fine soft hair"
        }
        if ht_en_dict[hair_texture]:
            res.append(ht_en_dict[hair_texture])

        # 髪型 - 種類を増強
        hair = st.selectbox("髪型", [
            "指定なし", "ベリーショート", "ショートヘア", "ボブカット", "ミディアムヘア", "ロングヘア", "スーパーロング",
            "ポニーテール", "サイドテール", "ツインテール", "ハーフアップ", "お団子ヘア", "三つ編み", "姫カット",
            "ピクシーカット", "坊主", "モヒカン", "オールバック", "ツーブロック", "マッシュヘア", "アフロ", "ドレッドヘア", "パーマ"
        ])
        hair_en_dict = {
            "指定なし": "",
            "ベリーショート": "very short hair",
            "ショートヘア": "short hair",
            "ボブカット": "bob cut",
            "ミディアムヘア": "medium hair",
            "ロングヘア": "long hair",
            "スーパーロング": "very long hair",
            "ポニーテール": "ponytail",
            "サイドテール": "side ponytail",
            "ツインテール": "twintails",
            "ハーフアップ": "half-up hair",
            "お団子ヘア": "bun hair",
            "三つ編み": "braided hair",
            "姫カット": "hime cut",
            "ピクシーカット": "pixie cut",
            "坊主": "buzz cut",
            "モヒカン": "mohawk",
            "オールバック": "slicked back hair",
            "ツーブロック": "undercut hair",
            "マッシュヘア": "mushroom hair cut",
            "アフロ": "afro hair",
            "ドレッドヘア": "dreadlocks",
            "パーマ": "permed hair"
        }
        if hair_en_dict[hair]:
            res.append(hair_en_dict[hair])

        face = st.selectbox("表情", ["指定なし", "微笑み", "満面の笑み", "キリッとした顔", "不敵な笑み", "叫び", "泣き顔", "驚き", "恥じらい", "無表情"])
        face_en_dict = {"指定なし": "", "微笑み": "gentle smile", "満面の笑み": "big happy smile", "キリッとした顔": "determined face", "不敵な笑み": "smirk", "叫び": "shouting", "泣き顔": "crying", "驚き": "surprised", "恥じらい": "blushing", "無表情": "expressionless"}
        if face_en_dict[face]:
            res.append(face_en_dict[face])
        
        pose = st.selectbox("ポーズ", ["指定なし", "立ち姿", "座る", "歩く", "戦う構え", "祈る", "自撮り", "振り返る", "しゃがむ", "腕を組む"])
        pose_en_dict = {"指定なし": "", "立ち姿": "standing straight", "座る": "sitting", "歩く": "walking", "戦う構え": "fighting stance", "祈る": "praying", "自撮り": "selfie pose", "振り返る": "looking back", "しゃがむ": "squatting", "腕を組む": "arms crossed"}
        if pose_en_dict[pose]:
            res.append(pose_en_dict[pose])

    return res, age, f_style, cloth