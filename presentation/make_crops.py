"""Cuts zoomed-in regions from the report screenshots for the slides.

The slides need large, readable text from the back of a classroom, so each
picture is only the part of the screen that matters, not the whole page.
Run:  python make_crops.py   (needs Pillow)
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
SRC = HERE.parent / "report" / "img" / "screens"   # 1800 px wide JPEGs
OUT = HERE / "screens"

# name -> (source file, crop box in source pixels: left, top, right, bottom)
CROPS = {
    "home":        ("p01-home.jpg",           (0, 0, 1800, 1125)),
    "ai-helper":   ("c02-ai-helper.jpg",      (360, 234, 1764, 774)),
    "offer":       ("c06-offers.jpg",         (252, 639, 1283, 878)),
    "quote":       ("c10-quote.jpg",          (240, 630, 1290, 860)),
    "tech-offer":  ("t03-offer.jpg",          (1106, 90, 1800, 760)),
    "warranty":    ("c17-warranty-resolved.jpg", (171, 693, 1283, 1022)),
    "wallet":      ("t13-wallet.jpg",         (360, 229, 1764, 1003)),
    "admin":       ("a01-overview.jpg",       (360, 234, 1764, 675)),
    "reports":     ("a08-reports.jpg",        (290, 275, 1415, 660)),
    "chat":        ("p05-ai-chat.jpg",        (1240, 0, 1800, 630)),
    "jobs":        ("p04-jobs.jpg",           (180, 160, 1620, 1125)),
    "tracking":    ("p06-tracking.jpg",       (180, 100, 1620, 1125)),
}


def main():
    OUT.mkdir(exist_ok=True)
    for name, (src, box) in CROPS.items():
        im = Image.open(SRC / src).convert("RGB").crop(box)
        im.save(OUT / f"{name}.png", optimize=True)
        print(name, im.size)


if __name__ == "__main__":
    main()
