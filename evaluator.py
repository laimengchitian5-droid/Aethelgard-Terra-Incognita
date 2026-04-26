# evaluator.py
import numpy as np

def calculate_bfi2_scores(responses):
    # 逆転項目の番号 (BFI-2-S 30問版準拠)
    reverse_indices = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 28, 30]
    
    processed = {}
    for i in range(1, 31):
        val = responses.get(f"Q{i}", 3)
        if i in reverse_indices:
            processed[f"Q{i}"] = 6 - val
        else:
            processed[f"Q{i}"] = val

    # 因子ごとの集計（各因子6問ずつ）
    scores = {
        "Extraversion": np.mean([processed[f"Q{i}"] for i in [1, 2, 3, 4, 5, 6]]),
        "Agreeableness": np.mean([processed[f"Q{i}"] for i in [7, 8, 9, 10, 11, 12]]),
        "Conscientiousness": np.mean([processed[f"Q{i}"] for i in [13, 14, 15, 16, 17, 18]]),
        "Negative Emotionality": np.mean([processed[f"Q{i}"] for i in [19, 20, 21, 22, 23, 24]]),
        "Open-Mindedness": np.mean([processed[f"Q{i}"] for i in [25, 26, 27, 28, 29, 30]]),
    }
    return scores
