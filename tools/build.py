# -*- coding: utf-8 -*-
"""원본 드릴(ai_해커톤/drill.html)로 공개 사이트 index.html 을 만든다.

원본은 Claude 아티팩트 형식이라 <head> 가 없다. 공개 사이트에서는
완전한 HTML 문서와 링크 미리보기(Open Graph) 메타가 필요하다.

    python tools/build.py
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(os.path.dirname(ROOT), "ai_해커톤", "drill.html")
URL = "https://haweee47.github.io/ai-literacy-drill/"

TITLE = "AI 리터러시 드릴"
DESC = ("생성형 AI·ML 개념부터 AI 결과를 검증하는 판단력까지. "
        "155문항, 긴 지문 세트 8개, 실전 모드와 해설을 담았습니다. 설치·로그인 없이 바로 풉니다.")

HEAD = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{TITLE}">
<meta property="og:title" content="{TITLE} — 155문항 실전 연습">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{URL}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{URL}og.png">
<style>body{{margin:0}}[hidden]{{display:none!important}}
footer.pub{{font-size:12.5px;color:var(--muted);margin-top:34px;padding-top:14px;
  border-top:1px solid var(--line);line-height:1.8;word-break:keep-all}}
footer.pub a{{color:var(--accent)}}</style>
"""

FOOT = """  <footer class="pub">
    문항과 해설은 직접 작성했습니다. 풀이 기록은 지금 쓰는 기기의 브라우저에만 저장되고 어디로도 전송되지 않습니다.
    · <a href="https://github.com/Haweee47/ai-literacy-drill" target="_blank" rel="noopener">GitHub</a>
  </footer>
"""


def main():
    s = io.open(SRC, encoding="utf-8").read()
    cut = s.index('<div class="wrap">')
    head_part, body_part = s[:cut], s[cut:]
    # 원본의 <title> 은 위에서 새로 쓰므로 뺀다
    i = head_part.index("<title>")
    j = head_part.index("</title>") + len("</title>")
    head_part = head_part[:i] + head_part[j:]
    # 본문 끝(.wrap 닫기 직전)에 출처 줄을 넣는다
    k = body_part.index('<main id="main"></main>') + len('<main id="main"></main>')
    body_part = body_part[:k] + "\n" + FOOT + body_part[k:]

    out = HEAD + head_part.strip() + "\n</head>\n<body>\n" + body_part.strip() + "\n</body>\n</html>\n"
    p = os.path.join(ROOT, "index.html")
    io.open(p, "w", encoding="utf-8", newline="\n").write(out)
    print("index.html  %.1f KB" % (os.path.getsize(p) / 1024))


if __name__ == "__main__":
    main()
