import streamlit as st

def get_landscape_settings(subject_en):
    st.subheader("⛰️ 風景・環境詳細")
    col1, col2 = st.columns(2)
    res = [subject_en]
    
    with col1:
        # 1. 時間帯の選択（都会や空に合う選択肢を拡充）
        time = st.selectbox("時間帯", [
            "指定なし", "朝（日の出）", "昼（快晴）", "夕焼け", "夜（星空）", 
            "深夜（月明かり）", "ブルーアワー", "マジックアワー", "サイバーパンクな夜（ネオン）"
        ])
        t_dict = {
            "指定なし": "",
            "朝（日の出）": "at sunrise, morning light",
            "昼（快晴）": "midday, bright sunlight, clear sky",
            "夕焼け": "sunset, golden hour, orange sky",
            "夜（星空）": "night, starry sky, milky way",
            "深夜（月明かり）": "midnight, moonlight, deep shadows",
            "ブルーアワー": "blue hour, twilight",
            "マジックアワー": "magic hour, soft lighting",
            "サイバーパンクな夜（ネオン）": "night, neon lights, glowing city signs"
        }
        if time != "指定なし":
            res.append(t_dict[time])
            
        # 2. 天候・環境エフェクト
        weather_ls = st.selectbox("天候・特殊効果", [
            "指定なし", "快晴", "曇り空", "雨・しとしと", "激しい雷雨", "雪景", "霧・霞", "オーロラ", "砂嵐"
        ])
        w_ls_dict = {
            "指定なし": "",
            "快晴": "clear weather",
            "曇り空": "cloudy sky, overcast",
            "雨・しとしと": "raining, wet surfaces",
            "激しい雷雨": "thunderstorm, lightning bolts",
            "雪景": "snowing, winter atmosphere",
            "霧・霞": "foggy, misty, hazy",
            "オーロラ": "aurora borealis, northern lights",
            "砂嵐": "sandstorm, dusty atmosphere"
        }
        if weather_ls != "指定なし":
            res.append(w_ls_dict[weather_ls])

    with col2:
        # 3. 雰囲気（都会的・幻想的な要素を強化）
        vibe = st.selectbox("雰囲気", [
            "指定なし", "平和・穏やか", "幻想的・エリアル", "不気味・ダーク", "荒廃・ディストピア", 
            "神秘的", "賑やか・活気", "都会的・モダン", "サイバーパンク", "雄大・壮大"
        ])
        v_dict = {
            "指定なし": "",
            "平和・穏やか": "peaceful and calm",
            "幻想的・エリアル": "ethereal, fantasy world, dreamlike",
            "不気味・ダーク": "eerie, spooky, dark atmosphere",
            "荒廃・ディストピア": "ruined, post-apocalyptic, dystopia",
            "神秘的": "mysterious, divine, sacred",
            "賑やか・活気": "lively, bustling, high energy",
            "都会的・モダン": "urban, metropolitan, modern architecture",
            "サイバーパンク": "cyberpunk style, futuristic, neon-tinted",
            "雄大・壮大": "magnificent, epic scale, grand panorama"
        }
        if vibe != "指定なし":
            res.append(v_dict[vibe])

        # 4. 画角・パース（風景ならではの迫力）
        perspective = st.selectbox("構図・パース", [
            "指定なし", "広角（パノラマ）", "魚眼レンズ", "俯瞰（空撮）", "見上げる（アオリ）", "消失点（奥行き）"
        ])
        p_dict = {
            "指定なし": "",
            "広角（パノラマ）": "wide angle lens, panoramic view",
            "魚眼レンズ": "fisheye lens perspective",
            "俯瞰（空撮）": "aerial view, bird's eye view",
            "見上げる（アオリ）": "low angle view, looking up",
            "消失点（奥行き）": "one-point perspective, vanishing point, leading lines"
        }
        if perspective != "指定なし":
            res.append(p_dict[perspective])
            
    return res, vibe