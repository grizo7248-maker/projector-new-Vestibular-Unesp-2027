import re, shutil
src = open('/app/memory/home_build/unesp.html', encoding='utf-8', errors='ignore').read()
pass

s = src
s = re.sub(r'<link rel=canonical[^>]*>', '', s)
s = re.sub(r'<iframe[^>]*>.*?</iframe>', '', s, flags=re.S)
s = re.sub(r'<iframe[^>]*>', '', s)
s = re.sub(r'<script[^>]*>\s*</script>', '', s)
s = re.sub(r'<!--\[if lte IE 9\]>.*?<!\[endif\]-->', '', s, flags=re.S)
s = re.sub(r'<!--\s*Page saved with SingleFile.*?-->', '', s, flags=re.S)
s = s.replace('<a class=apply-to-it href=https://www.vunesp.com.br/VNSP2514/Inscricao>',
              '<a class=apply-to-it href=/termos.html id=btn-inscreva-se data-testid=home-inscreva-se-btn>')
s = re.sub(r'href=(["\']?)(?:https?:)?//[^"\'\s>]+\1', 'href=#', s)
s = re.sub(r'data-host=https?://[^\s>]+', '', s)
s = s.replace('<form action=/ method=GET class=form-search>', '<form action=# method=GET class=form-search onsubmit="return false">')
s = s.replace('<meta name=viewport content="width=device-width, initial-scale=1, maximum-scale=5">',
              '<meta name=viewport content="width=device-width, initial-scale=1, maximum-scale=5, viewport-fit=cover">'
              '<meta name=format-detection content="telephone=no"><meta name=theme-color content="#ffffff">'
              '<meta name=apple-mobile-web-app-capable content=yes>')

extra = open('/app/memory/home_build/home_extra.html', encoding='utf-8').read()
if '</body>' in s:
    s = s.replace('</body>', extra + '</body>', 1)
else:
    s += extra + '</body></html>'
open('/app/frontend/public/inicio.html', 'w', encoding='utf-8').write(s)
print('ok', len(s), 'external left:', set(re.findall(r'(?:href|src|action)=["\']?(https?://[^"\'\s>]+)', s)))
