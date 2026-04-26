# evaluator.py
import numpy as np

def calculate_bfi2_scores(responses):
    # 逆転項目のリスト（BFI-2-S 30問版の番号に対応）
    # ※印がついた項目: 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30
    reverse_indices = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    
    processed = {}
    for i in range(1, 31):
        val = responses.get(f"Q{i}", 3)
        if i in reverse_indices:
            processed[f"Q{i}"] = 6 - val # 1<->5, 2<->4 反転
        else:
            processed[f"Q{i}"] = val

    # 5因子の平均値を算出
    scores = {
        "Extraversion (外向性)": np.mean([processed[f"Q{i}"] for i in [1, 2, 3, 4, 5, 6]]),
        "Agreeableness (協調性)": np.mean([processed[f"Q{i}"] for i in [7, 8, 9, 10, 11, 12]]),
        "Conscientiousness (誠実性)": np.mean([processed[f"Q{i}"] for i in [13, 14, 15, 16, 17, 18]]),
        "Negative Emotionality (神経症傾向)": np.mean([processed[f"Q{i}"] for i in [19, 20, 21, 22, 23, 24]]),
        "Open-Mindedness (開放性)": np.mean([processed[f"Q{i}"] for i in [25, 26, 27, 28, 29, 30]]),
    }
    return scores
