import streamlit as st

def get_logo_settings(subject_en):
    st.subheader("🔡 ロゴデザイン詳細")
    text = st.text_input("ロゴ文字列", "LOGO")
    mat = st.selectbox("質感", ["ゴールド", "クローム", "ネオン", "マグマ"])
    m_dict = {"ゴールド": "gold mirror finish", "クローム": "chrome shiny", "ネオン": "neon glow", "マグマ": "molten magma"}
    res = [f'"{text}" text logo', subject_en, m_dict[mat], "professional graphic design"]
    return res