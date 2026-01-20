import streamlit as st

def get_human_settings(subject_en):
    res = []
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("年齢層", 5, 80, 20)
        res.append(f"{age}yo {subject_en}")
        f_style = st.selectbox("ファッションスタイル", ["現代カジュアル", "ビジネス/フォーマル", "ファンタジー/RPG職種", "和装", "サイバーパンク"])
        
        if f_style == "現代カジュアル":
            cloth = st.selectbox("衣装", ["Tシャツとジーンズ", "パーカー", "夏服ワンピース", "レザージャケット", "カーディガン"])
            c_en = {"Tシャツとジーンズ": "t-shirt and blue jeans", "パーカー": "hoodie", "夏服ワンピース": "summer dress", "レザージャケット": "leather jacket", "カーディガン": "cardigan"}[cloth]
        elif f_style == "ビジネス/フォーマル":
            cloth = st.selectbox("衣装", ["ビジネススーツ", "タキシード", "イブニングドレス", "白シャツとスラックス"])
            c_en = {"ビジネススーツ": "business suit", "タキシード": "tuxedo", "イブニングドレス": "evening gown", "白シャツとスラックス": "white shirt and slacks"}[cloth]
        elif f_style == "ファンタジー/RPG職種":
            cloth = st.selectbox("役職/装備", ["騎士の鎧", "魔術師のローブ", "聖職者の服", "忍び装束", "侍の甲冑", "盗賊の軽装"])
            c_en = {"騎士の鎧": "knight armor", "魔術師のローブ": "wizard robes", "聖職者の服": "cleric vestments", "忍び装束": "ninja outfit", "侍の甲冑": "samurai armor", "盗賊の軽装": "thief gear"}[cloth]
        elif f_style == "和装":
            cloth = st.selectbox("衣装", ["着物", "浴衣", "袴", "巫女装束"])
            c_en = {"着物": "kimono", "浴衣": "yukata", "袴": "hakama", "巫女装束": "miko outfit"}[cloth]
        else: # サイバーパンク
            cloth = st.selectbox("衣装", ["ネオンジャケット", "タクティカルベスト", "サイバネティックウェア"])
            c_en = {"ネオンジャケット": "neon glowing jacket", "タクティカルベスト": "tactical vest", "サイバネティックウェア": "cybernetic techwear"}[cloth]
        res.append(c_en)

    with col2:
        status = st.selectbox("衣装の状態", ["新品同様", "着古した", "汚れた", "ボロボロ", "血に染まった"])
        res.append({"新品同様": "brand new, clean", "着古した": "worn-in", "汚れた": "dirty", "ボロボロ": "tattered, weathered", "血に染まった": "blood-stained"}[status])
        
        face = st.selectbox("表情", ["微笑み", "満面の笑み", "キリッとした顔", "不敵な笑み", "叫び", "泣き顔", "驚き", "恥じらい", "無表情"])
        res.append({"微笑み": "gentle smile", "満面の笑み": "big happy smile", "キリッとした顔": "determined face", "不敵な笑み": "smirk", "叫び": "shouting", "泣き顔": "crying", "驚き": "surprised", "恥じらい": "blushing", "無表情": "expressionless"}[face])
        
        pose = st.selectbox("ポーズ", ["立ち姿", "座る", "歩く", "戦う構え", "祈る", "自撮り", "振り返る", "しゃがむ", "腕を組む"])
        res.append({"立ち姿": "standing straight", "座る": "sitting", "歩く": "walking", "戦う構え": "fighting stance", "祈る": "praying", "自撮り": "selfie pose", "振り返る": "looking back", "しゃがむ": "squatting", "腕を組む": "arms crossed"}[pose])

    return res, f_style, cloth