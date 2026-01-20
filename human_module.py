import streamlit as st

def get_human_settings(subject_en):
    st.subheader("👤 人物・ファッション詳細")
    res = []
    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("年齢層", 5, 80, 20)
        res.append(f"{age}yo {subject_en}")

        f_style = st.selectbox("ファッションスタイル", ["現代カジュアル", "ビジネス/フォーマル", "ファンタジー/RPG職種", "和装", "サイバーパンク"])

        if f_style == "現代カジュアル":
            cloth = st.selectbox("衣装", ["Tシャツとジーンズ", "パーカー", "夏服ワンピース", "レザージャケット"])
            c_dict = {"Tシャツとジーンズ": "t-shirt and blue jeans", "パーカー": "hoodie", "夏服ワンピース": "summer dress", "レザージャケット": "leather jacket"}
        elif f_style == "ビジネス/フォーマル":
            cloth = st.selectbox("衣装", ["ビジネススーツ", "タキシード", "イブニングドレス"])
            c_dict = {"ビジネススーツ": "business suit", "タキシード": "tuxedo", "イブニングドレス": "evening gown"}
        elif f_style == "ファンタジー/RPG職種":
            cloth = st.selectbox("役職/装備", ["騎士の鎧", "魔術師のローブ", "忍び装束", "侍の甲冑", "盗賊の軽装"])
            c_dict = {"騎士の鎧": "knight armor", "魔術師のローブ": "wizard robes", "忍び装束": "ninja outfit", "侍の甲冑": "samurai armor", "盗賊の軽装": "thief gear"}
        elif f_style == "和装":
            cloth = st.selectbox("衣装", ["着物", "浴衣", "袴"])
            c_dict = {"着物": "kimono", "浴衣": "yukata", "袴": "hakama"}
        else:
            cloth = st.selectbox("衣装", ["ネオンジャケット", "タクティカルベスト"])
            c_dict = {"ネオンジャケット": "neon glowing jacket", "タクティカルベスト": "tactical vest"}
        
        res.append(c_dict[cloth])

    with col2:
        c_status = st.selectbox("衣装の状態", ["新品同様", "着古した", "汚れた", "ボロボロ", "血に染まった"])
        status_dict = {"新品同様": "brand new, clean", "着古した": "worn-in", "汚れた": "dirty", "ボロボロ": "tattered, weathered", "血に染まった": "blood-stained"}
        res.append(status_dict[c_status])

        pose = st.selectbox("ポーズ", ["立ち姿", "座る", "歩く", "戦う構え", "祈る", "自撮り", "振り返る"])
        pose_dict = {"立ち姿": "standing straight", "座る": "sitting", "歩く": "walking", "戦う構え": "fighting stance", "祈る": "praying", "自撮り": "selfie pose", "振り返る": "looking back"}
        res.append(pose_dict[pose])

    return res