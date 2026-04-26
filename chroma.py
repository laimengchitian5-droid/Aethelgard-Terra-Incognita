def get_theme_color(stage):
    themes = {
        "Awakening": "#00d4ff", # 水色
        "Frontier": "#7000ff",  # 紫
        "Singularity": "#ff0070" # 赤紫
    }
    return themes.get(stage.split(":")[1].strip().split(" ")[0], "#00d4ff")
