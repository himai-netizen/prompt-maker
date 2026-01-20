import streamlit as st

def get_animal_settings(subject_en):
    st.subheader("🐾 動物・動作詳細")
    col1, col2 = st.columns(2)
    res = []
    with col1:
        state = st.selectbox("動作", ["立っている", "全力疾走", "咆哮", "眠っている", "獲物を狙う"])
        s_dict = {"立っている": "standing", "全力疾走": "galloping", "咆哮": "roaring", "眠っている": "sleeping", "獲物を狙う": "prowling"}
        res.append(f"{s_dict[state]} {subject_en}")
    with col2:
        size = st.selectbox("サイズ", ["普通の", "巨大な", "伝説級"])
        size_dict = {"巨大な": "huge", "伝説級": "mythical giant"}
        if size != "普通の": res.append(size_dict[size])
    return res