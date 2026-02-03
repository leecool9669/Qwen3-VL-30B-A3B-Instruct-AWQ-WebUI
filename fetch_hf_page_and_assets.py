"""拉取 HF 页面 HTML 与界面图片到 template，不下载模型权重。"""
import os
import re
from pathlib import Path

import requests

BASE_URL = "https://hf-mirror.com"
REPO_ID = "QuantTrio/Qwen3-VL-30B-A3B-Instruct-AWQ"
TEMPLATE_DIR = Path(__file__).resolve().parent
UPSTREAM_HTML = TEMPLATE_DIR / "upstream_hf" / "hf_mirror_page.html"
ASSETS_HF = TEMPLATE_DIR / "assets" / "hf"

IMAGE_URLS = [
    "https://cdn-thumbnails.hf-mirror.com/social-thumbnails/models/QuantTrio/Qwen3-VL-30B-A3B-Instruct-AWQ.png",
    "https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3-VL/qwen3vl_arc.jpg",
    "https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3-VL/table_nothinking_vl-30a3.jpg",
    "https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3-VL/table_nothinking_text-30a3.jpg",
]


def safe_filename(url: str) -> str:
    name = Path(url.rstrip("/")).name
    return re.sub(r"[^0-9A-Za-z._-]+", "_", name)[:80] or "asset"


def main():
    proxy = os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY")
    proxies = {"http": proxy, "https": proxy} if proxy else None
    UPSTREAM_HTML.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(f"{BASE_URL}/{REPO_ID}", timeout=30, proxies=proxies)
    r.raise_for_status()
    UPSTREAM_HTML.write_text(r.text, encoding="utf-8", errors="replace")
    ASSETS_HF.mkdir(parents=True, exist_ok=True)
    for img_url in IMAGE_URLS:
        try:
            resp = requests.get(img_url, timeout=30, proxies=proxies)
            resp.raise_for_status()
            (ASSETS_HF / safe_filename(img_url)).write_bytes(resp.content)
        except Exception:
            pass


if __name__ == "__main__":
    main()
