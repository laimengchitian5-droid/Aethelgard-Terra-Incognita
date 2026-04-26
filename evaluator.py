import numpy as np

# BFI-2 日本語版質問リスト（30問：Standard版）
# (R) は逆転項目を示す
QUESTIONS_30 = [
    "社交的な方だ", "他人に思いやりがある", "物事を効率的にこなせない(R)", "よく心配事をする", "芸術にあまり興味がない(R)",
    "自分から主導権を握る", "他人に対して礼儀正しい", "怠けがちである(R)", "落ち込みやすく悲しくなる", "複雑な概念を理解することを楽しむ",
    "活発で元気がある", "他人の欠点を探す傾向がある(R)", "信頼できる、頼りになる", "気分が変わりやすく不安定だ", "創造的な想像力が豊かだ",
    "静かで内向的な方だ(R)", "他人に冷淡で無関心な時がある(R)", "几帳面で整頓を好む", "リラックスしていてストレスに強い(R)", "芸術の美しさに心惹かれる",
    "自分に自信があり、他人に影響を与える", "他人に対して批判的になりやすい(R)", "仕事を最後までやり遂げる", "感情的に安定している(R)", "独創的な考えをあまり持たない(R)",
    "人混みの中にいるのが好きだ", "他人に疑い深い(R)", "責任感が強い", "些細なことで動揺する", "抽象的な思考があまり得意ではない(R)"
]

# 逆転項目のインデックス（1始まり）
REVERSE_ITEMS = [3, 5, 8, 12, 16, 17, 19, 22, 24, 25, 27, 30]

# 15ファセットのマッピング（質問番号：1-30）
FACET_MAP = {
    "社交性": [1, 16], "自己主張": [6, 21], "活力": [11, 26],
    "共感性": [2, 17], "謙虚さ": [7, 22], "信頼性": [12, 27],
    "体制化": [3, 18], "勤勉性": [8, 23], "責任感": [13, 28],
    "不安": [4, 19], "抑うつ": [9, 24], "情緒不安定": [14, 29],
    "知的好奇心": [10, 25], "美的感受性": [5, 20], "創造的想像力": [15, 30]
}

def run_advanced_analysis(responses):
    """
    responses: {1: 5, 2: 3, ... 30: 1} の辞書
    """
    # 1. 逆転項目の反転処理 (1-5スケール)
    processed = {}
    for q_idx, val in responses.items():
        if q_idx in REVERSE_ITEMS:
            processed[q_idx] = 6 - val
        else:
            processed[q_idx] = val

    # 2. 15ファセット平均値算出
    facet_results = {}
    for f_name, q_indices in FACET_MAP.items():
        scores = [processed[i] for i in q_indices if i in processed]
        facet_results[f_name] = sum(scores) / len(scores) if scores else 3.0

    # 3. 5大因子（ビッグファイブ）算出
    big_five = {
        "外向性": (facet_results["社交性"] + facet_results["自己主張"] + facet_results["活力"]) / 3,
        "協調性": (facet_results["共感性"] + facet_results["謙虚さ"] + facet_results["信頼性"]) / 3,
        "誠実性": (facet_results["体制化"] + facet_results["勤勉性"] + facet_results["責任感"]) / 3,
        "神経症": (facet_results["不安"] + facet_results["抑うつ"] + facet_results["情緒不安定"]) / 3,
        "開放性": (facet_results["知的好奇心"] + facet_results["美的感受性"] + facet_results["創造的想像力"]) / 3
    }

    # 4. 物理演算 (Tensegrity Dynamics)
    r = np.array(list(facet_results.values()))
    theta = np.linspace(0, 2 * np.pi, 15, endpoint=False)
    points = np.column_stack((r * np.cos(theta), r * np.sin(theta)))
    
    # ストレス: 隣接ファセット間のスコア差
    stress = np.sum(np.abs(np.diff(np.append(r, r))))
    # 容積: 多角形の面積
    volume = 0.5 * np.abs(np.dot(x := points[:,0], np.roll(y := points[:,1], 1)) - np.dot(y, np.roll(x, 1)))
    # レジリエンス: 慣性モーメント
    resilience = np.sum(r**2)

    return {
        "facets": facet_results,
        "big_five": big_five,
        "physics": {"S": stress, "V": volume, "I": resilience}
    }
