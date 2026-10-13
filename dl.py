import http.cookiejar, re, urllib.parse, urllib.request


def download(url, dest):
    """Laster ned fra en offentlig URL. Takler Google Drives bekreftelsesside for store filer."""
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [("User-Agent", "Mozilla/5.0")]
    for attempt in range(4):
        try:
            with opener.open(url, timeout=120) as r:
                ctype = r.headers.get("Content-Type", "")
                data = r.read()
            if "text/html" in ctype:
                html = data.decode("utf-8", "ignore")
                m = re.search(r'href="(/uc\?export=download[^"]+)"', html) or \
                    re.search(r'action="(https://drive\.usercontent\.google\.com/download[^"]*)"', html)
                if m:
                    nxt = m.group(1).replace("&amp;", "&")
                    if nxt.startswith("/"):
                        nxt = "https://drive.google.com" + nxt
                    # skjema-variant: legg ved skjulte felter
                    fields = dict(re.findall(r'name="([^"]+)" value="([^"]*)"', html))
                    if fields and "usercontent" in nxt:
                        nxt += ("&" if "?" in nxt else "?") + urllib.parse.urlencode(fields)
                    url = nxt
                    continue
                raise RuntimeError(f"Fikk HTML i stedet for fil fra {url[:80]}")
            with open(dest, "wb") as f:
                f.write(data)
            if len(data) < 1000:
                raise RuntimeError(f"For liten fil ({len(data)} byte) fra {url[:80]}")
            return dest
        except Exception as e:  # noqa
            print(f"Nedlasting feilet (forsøk {attempt+1}): {e}", flush=True)
            last = e
    raise last


