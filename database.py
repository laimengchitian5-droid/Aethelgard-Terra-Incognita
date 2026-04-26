import json
import os
from datetime import datetime

def save_log(prompt, response):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "user": prompt,
        "assistant": response
    }
    
    # クラウド上でディレクトリが存在しない場合のエラー防止
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # 追記モードで保存
    with open("data/session_logs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")
