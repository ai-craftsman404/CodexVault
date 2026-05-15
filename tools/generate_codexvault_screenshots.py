from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"C:\Users\georg\codex-project\Code-Plugin-Guru")
OUT = ROOT / "assets" / "codexvault"
OUT.mkdir(parents=True, exist_ok=True)


def font(size: int):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/consola.ttf", size)
    except Exception:
        return ImageFont.load_default()


def card(title, subtitle, body_lines, path):
    img = Image.new("RGB", (1600, 900), "#0b1220")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((40, 40, 1560, 860), radius=28, fill="#111c2f", outline="#2d3b52", width=3)
    d.text((80, 80), title, font=font(42), fill="#f4f7fb")
    d.text((80, 142), subtitle, font=font(22), fill="#8fb3ff")
    y = 220
    for line in body_lines:
        if isinstance(line, tuple) and line[0] == "head":
            d.rounded_rectangle((80, y, 1480, y + 70), radius=16, fill="#1a2940", outline="#314a6b", width=2)
            d.text((110, y + 18), line[1], font=font(26), fill="#ffd58f")
            y += 98
        else:
            d.rounded_rectangle((80, y, 1480, y + 88), radius=16, fill="#132033", outline="#27364c", width=2)
            d.text((110, y + 18), line, font=font(24), fill="#f4f7fb")
            y += 106
    d.text((80, 780), "CodexVault preview screenshot", font=font(18), fill="#7d8aa5")
    img.save(path)


card(
    "CodexVault dry-run preview",
    "Non-destructive walkthrough of the full backup workflow",
    [
        ("head", "backup --workspace-root /path/to/codex-project --dry-run"),
        "discover -> manifest -> snapshot -> plan -> verify -> simulate",
        "Structured step trace printed, no artifacts created",
        "Useful for first-time users and agent-team rehearsal",
        "Highlights-only summary: headline, status, blocker, action",
    ],
    OUT / "dry-run-preview.png",
)

card(
    "CodexVault E2E verification",
    "Python test suite covering root backup, overrides, and safety paths",
    [
        ("head", "Ran 12 tests ... OK"),
        "Root backup mode covers every eligible plugin project under plugins/",
        "Targeted single-project override remains available",
        "Negative-path fixtures cover malformed JSON, checksum mismatch, traversal",
        "Agent-team simulation records a structured adjudication envelope",
    ],
    OUT / "e2e-verification.png",
)

