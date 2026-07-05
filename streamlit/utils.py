THEMES = {
    "Monochrome": {
        "primary":    "#111827",
        "secondary":  "#374151",
        "accent":     "#6B7280",
        "highlight":  "#F3F4F6",
        "danger":     "#DC2626",
        "success":    "#16A34A",
        "warning":    "#D97706",
        "chart_seq":  ["#111827","#374151","#4B5563","#6B7280","#9CA3AF","#D1D5DB"],
        "churn_color":"#DC2626",
        "retain_color":"#16A34A",
    },
    "Ocean Blue": {
        "primary":    "#0C3A6B",
        "secondary":  "#1565C0",
        "accent":     "#42A5F5",
        "highlight":  "#E3F2FD",
        "danger":     "#D32F2F",
        "success":    "#2E7D32",
        "warning":    "#F57F17",
        "chart_seq":  ["#0C3A6B","#1565C0","#1976D2","#42A5F5","#90CAF9","#BBDEFB"],
        "churn_color":"#D32F2F",
        "retain_color":"#2E7D32",
    },
    "Forest Green": {
        "primary":    "#1B4332",
        "secondary":  "#2D6A4F",
        "accent":     "#52B788",
        "highlight":  "#D8F3DC",
        "danger":     "#C0392B",
        "success":    "#1B4332",
        "warning":    "#B7791F",
        "chart_seq":  ["#1B4332","#2D6A4F","#40916C","#52B788","#74C69D","#B7E4C7"],
        "churn_color":"#C0392B",
        "retain_color":"#1B4332",
    },
    "Royal Purple": {
        "primary":    "#4A1D96",
        "secondary":  "#6D28D9",
        "accent":     "#A78BFA",
        "highlight":  "#EDE9FE",
        "danger":     "#B91C1C",
        "success":    "#15803D",
        "warning":    "#B45309",
        "chart_seq":  ["#4A1D96","#5B21B6","#6D28D9","#7C3AED","#8B5CF6","#A78BFA"],
        "churn_color":"#B91C1C",
        "retain_color":"#15803D",
    },
}

def get_theme(name: str) -> dict:
    return THEMES.get(name, THEMES["Ocean Blue"])

def get_theme_names() -> list:
    return list(THEMES.keys())
