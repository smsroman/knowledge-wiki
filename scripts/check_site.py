"""Check generated navigation, assets, fragments and GitHub editing destinations."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CONFIG = tomllib.loads((ROOT / "zensical.toml").read_text())["project"]
BASE = CONFIG["site_url"]
ORIGIN = urlsplit(BASE).netloc


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if attrs.get(name):
                self.links.append((tag, attrs[name]))


def main():
    errors = []
    pages = {p: Page(p.read_text()) for p in SITE.rglob("*.html")}
    if not pages:
        raise SystemExit("No generated HTML; run zensical build first")
    checked_links = 0
    for path, page in pages.items():
        relative = path.relative_to(SITE).as_posix()
        page_url = urljoin(BASE, relative.removesuffix("index.html"))
        for tag, href in page.links:
            url = urlsplit(urljoin(page_url, href))
            if url.scheme not in ("http", "https") or url.netloc != ORIGIN:
                continue
            relative_target = unquote(url.path).lstrip("/")
            target = SITE / relative_target
            if url.path.endswith("/"):
                target /= "index.html"
            elif target.is_dir():
                target /= "index.html"
            if not target.is_file():
                errors.append(f"{relative}: missing {href}")
            elif tag == "a" and url.fragment and target in pages:
                if unquote(url.fragment) not in pages[target].ids:
                    errors.append(f"{relative}: missing fragment {href}")
            checked_links += 1

    sources = list((ROOT / "docs").rglob("*.md"))
    for source in sources:
        relative = source.relative_to(ROOT / "docs")
        target = SITE / (relative.parent / "index.html" if relative.name == "index.md"
                         else relative.with_suffix("") / "index.html")
        edit = CONFIG["repo_url"].rstrip("/") + "/" + CONFIG["edit_uri"] + relative.as_posix()
        page = pages.get(target)
        if not page or not any(href == edit for _, href in page.links):
            errors.append(f"{relative}: incorrect or missing GitHub edit link")

    if (SITE / "CNAME").read_text().strip() != ORIGIN:
        errors.append("CNAME does not match site_url")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"OK: {len(sources)} articles, {checked_links} internal links/assets, edit links and CNAME")


if __name__ == "__main__":
    main()
