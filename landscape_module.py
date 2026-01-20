import streamlit as st

def get_landscape_settings(subject_en):
    st.subheader("⛰️ 風景・環境詳細")
    col1, col2 = st.columns(2)
    res = [subject_en]
    with col1:
        time = st.selectbox("時間帯", ["朝", "昼", "夕焼け", "夜", "深夜"])
        t_dict = {"朝": "morning", "昼": "midday", "夕焼け": "sunset", "夜": "night", "深夜": "midnight"}
        res.append(f"at {t_dict[time]}")
    with col2:
        vibe = st.selectbox("雰囲気", ["平和", "幻想的", "不気味", "荒廃"])
        vibe_dict = {"平和": "peaceful", "幻想的": "ethereal", "不気味": "eerie", "荒廃": "ruined"}
        res.append(vibe_dict[vibe])
    return res