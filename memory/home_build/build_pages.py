import re, os, json
PUB = '/app/frontend/public'
BK = '/app/memory/backups/pages_seduc'
home = open(PUB + '/inicio.html', encoding='utf-8').read()

# ---------- assets VUNESP (css, fontes, header, footer) ----------
headpart = home[:home.find('<body')]
css = ''.join(re.findall(r'<style[^>]*>(.*?)</style>', headpart, re.S))
fonts = ''.join(re.findall(r'@font-face\{[^}]*\}', css))
os.makedirs(PUB + '/vunesp', exist_ok=True)
open(PUB + '/vunesp/chrome.css', 'w', encoding='utf-8').write(re.sub(r'@font-face\{[^}]*\}', '', css))
open(PUB + '/vunesp/fonts.css', 'w', encoding='utf-8').write(fonts)
h0 = home.find('<header'); h1 = home.find('</header>') + 9
header = home[h0:h1]
header = header.replace('<a href=# title="Clique aqui para voltar para a home">', '<a href=/ class=vn-home title="Clique aqui para voltar para a home">')
f0 = home.find('<footer id=rodape>'); f1 = home.find('</footer>', f0) + 9
footer = home[f0:f1]
open(PUB + '/vunesp/parts.json', 'w', encoding='utf-8').write(json.dumps({'h': header, 'f': footer}))

# ---------- textos ----------
OLD_CARD = 'Concurso Público de Provas e Títulos para Provimento de Cargos Efetivos de Professor com Lotação em Estabelecimentos de Ensino da Rede Estadual do Ceará, vinculados à Secretaria da Educação do Estado do Ceará (SEDUC).'
NEW_CARD = 'Fundação VUNESP — Vestibular da Universidade Estadual Paulista (Unesp). Inscrições de 04/09 a 20/10/2026, às 23h59. 5.850 vagas. Taxa de inscrição: R$ 225,00.'
REPL = [
    ('SECRETARIA DA EDUCAÇÃO DO ESTADO DO CEARÁ - SEDUC/CE', 'VESTIBULAR | VESTIBULAR UNESP 2027'),
    ('Edital Nº 014/2026-SEDUC/SEPLAG', 'Vestibular Unesp 2027 - VNSP2514'),
    (OLD_CARD, NEW_CARD),
    ('Concurso Público para Professor da Secretaria da Educação do Estado do Ceará (SEDUC/CE) - Edital 014/2026', 'Vestibular Unesp 2027 - Fundação VUNESP'),
    ('Concurso Público SEDUC/CE - Edital Nº 014/2026', 'Vestibular Unesp 2027 - VNSP2514'),
    ('014/2026-SEDUC/SEPLAG', 'VNSP2514'),
    ('Concurso Professor Seduc 2026 | CEV/UECE', 'Vestibular Unesp 2027 | Fundação VUNESP'),
    ('© CEV/UECE — CONCURSO PROFESSOR SEDUC 2026', '© FUNDAÇÃO VUNESP — VESTIBULAR UNESP 2027'),
    ('Concurso Professor Seduc 2026', 'Vestibular Unesp 2027'),
    ("'150.00'", "'225.00'"), ('R$ 150,00', 'R$ 225,00'), ('150,00', '225,00'),
    ('<img src="/seduc/cev-logo.png" alt="CEV/UECE" style="height:56px;', '<img src="/vunesp/vunesp-logo.png" alt="Fundação VUNESP" style="height:48px;'),
    ('CEV/UECE — Concursos Públicos', 'Fundação VUNESP — Vestibulares e Concursos'),
    ('Concurso Público para Professor da Secretaria da Educação do Estado do Ceará', 'Vestibular Unesp 2027'),
    ('Secretaria da Educação do Estado do Ceará (SEDUC/CE)', 'Universidade Estadual Paulista (Unesp) - VNSP2514'),
    ('Cebraspe - Concursos e Seleções com Integridade', 'Fundação VUNESP'),
    ('sac@cebraspe.org.br', 'atendimento@vunesp.com.br'),
    ('/seduc/seduc-theme.js?v=5', '/seduc/seduc-theme.js?v=10'),
    ('/seduc/seduc-theme.css?v=7', '/seduc/seduc-theme.css?v=10'),
    ('#008d3c', '#1172db'), ('#006b2d', '#0b4f9c'), ('#00a84a', '#1172db'), ('#0e2a1a', '#0a2540'),
    ('#008C00', '#1172db'), ('#0f6a10', '#0b4f9c'), ('#e8f5e9', '#eef5fd'), ('#f4faf6', '#eef5fd'), ('#1f3d2b', '#0b4f9c'), ('#2e7d32', '#1172db'), ('#eef6f0', '#eef5fd'), ('#d5e3da', '#d3e3f6'), ('#eaf6ee', '#e6f0fc'), ('#d9e6dd', '#d3e3f6'),
]
PAGES = ['inscricao.html', 'dados-inscricao.html', 'confirmacao.html', 'inscricao-realizada.html', 'pagamento-pix.html', 'minhas-inscricoes.html']
for p in PAGES:
    t = open(BK + '/' + p, encoding='utf-8').read()
    t = re.sub(r'<footer id="aocp-footer" class="seduc-footer".*?</footer>', '', t, flags=re.S)
    for a, b in REPL:
        t = t.replace(a, b)
    if p == 'confirmacao.html':
        t = t.replace('</body>', '<style>html body #pgInformacoes{padding-top:0!important}html body #pgInformacoes .blocoPadrao{margin-top:0!important;padding-top:0!important}html body #pgInformacoes .dados{padding-top:0!important}html body #TopoInformacoes{margin-top:0!important}html body #TopoInformacoes>div{padding-top:0!important}</style></body>', 1)
    open(PUB + '/' + p, 'w', encoding='utf-8').write(t)
    left = re.findall(r'(?i)seduc(?!/)|ceará|\bcev\b|uece|professor', re.sub(r'data:[^"\')\s]{100,}', '', t[t.find('<body'):]))
    print(p, 'restante:', len(left), set(x.lower() for x in left))

# ---------- tema (css/js) ----------
c = open(BK + '/seduc-theme.css', encoding='utf-8').read()
for a, b in REPL:
    if a.startswith('#'):
        c = c.replace(a, b)
c = c.replace('#008442', '#1172db')
open(PUB + '/seduc/seduc-theme.css', 'w', encoding='utf-8').write(c)
open(PUB + '/seduc/seduc-theme.js', 'w', encoding='utf-8').write(open('/app/memory/home_build/chrome_loader.js', encoding='utf-8').read())
print('ok')
