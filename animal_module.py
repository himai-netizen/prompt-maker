import streamlit as st

def get_animal_settings(subject_en):
    st.subheader("🐾 動物・動作詳細")
    col1, col2 = st.columns(2)
    res = []
    with col1:
        state = st.selectbox("状態・動作", ["立っている", "歩いている", "全力疾走", "座っている", "寝ている", "咆哮している", "威嚇", "ジャンプ", "空を飛んでいる", "泳いでいる"])
        s_dict = {"立っている": "standing", "歩いている": "walking", "全力疾走": "galloping at full speed", "座っている": "sitting", "寝ている": "sleeping", "咆哮している": "roaring", "威嚇": "intimidating stance", "ジャンプ": "jumping mid-air", "空を飛んでいる": "flying", "泳いでいる": "swimming"}
        res.append(f"{s_dict[state]} {subject_en}")
    with col2:
        size = st.selectbox("サイズ感", ["普通の", "巨大な", "伝説級の", "手のひらサイズの"])
        size_dict = {"普通の": "", "巨大な": "huge", "伝説級の": "mythical giant", "手のひらサイズの": "tiny palm-sized"}
        if size != "普通の": res.append(size_dict[size])
    return res, state