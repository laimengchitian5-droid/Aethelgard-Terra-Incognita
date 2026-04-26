import numpy as np

def calculate_bfi2_scores(responses):
    reverse_indices = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    processed = {}
    for i in range(1, 31):
        val = responses.get(f"Q{i}", 3)
        processed[f"Q{i}"] = 6 - val if i in reverse_indices else val

    scores = {
        "Extraversion": np.mean([processed[f"Q{i}"] for i in range(1, 7)]),
        "Agreeableness": np.mean([processed[f"Q{i}"] for i in range(7, 13)]),
        "Conscientiousness": np.mean([processed[f"Q{i}"] for i in range(13, 19)]),
        "Negative Emotionality": np.mean([processed[f"Q{i}"] for i in range(19, 25)]),
        "Open-Mindedness": np.mean([processed[f"Q{i}"] for i in range(25, 31)]),
    }
    return scores

def get_personality_type(scores):
    # 最も高いスコアを特定
    top_trait = max(scores, key=scores.get)
    
    types = {
        "Extraversion": {"title": "開拓の先駆者 (Vanguard)", "desc": "周囲を惹きつける光を放つ存在。"},
        "Agreeableness": {"title": "調和の守護者 (Guardian)", "desc": "秩序と共感をもたらすシステムの核。"},
        "Conscientiousness": {"title": "精密なる執行者 (Architect)", "desc": "計画を完遂させる強固な意志の持ち主。"},
        "Negative Emotionality": {"title": "繊細なる観測者 (Observer)", "desc": "微細な変化を察知する鋭敏な感覚器。"},
        "Open-Mindedness": {"title": "深淵の探究者 (Seeker)", "desc": "既存の枠を超え、新世界を構想する知性。"}
    }
    return types.get(top_trait, {"title": "未確認個体", "desc": "解析中..."})
