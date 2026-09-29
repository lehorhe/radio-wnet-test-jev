# -*- coding: utf-8 -*-
"""Drugi, niezależny przebieg: odczyt kluczy CKE wprost z PDF i porównanie z polem 'poprawna'."""
import json, re, pymupdf
ZR = r'D:\TECH\jev_testy\pokaz\zrodla'
items = [json.loads(l) for l in open(r'D:\TECH\jev_testy\pokaz\zadania_matura.jsonl', encoding='utf-8')]

def key_wos():
    d = pymupdf.open(ZR + r'\wos-2026-maj-matura-rozszerzona-odpowiedzi.pdf')
    lines = []
    for pi, p in enumerate(d):
        for l in p.get_text().split('\n'):
            lines.append((pi + 1, l.strip()))
    res = {}; cur = None
    for i, (pg, l) in enumerate(lines):
        m = re.match(r'Zadanie (\d+(?:\.\d+)?)\. \(', l)
        if m: cur = m.group(1); continue
        if cur and cur not in res:
            if l == 'Rozwiązanie':
                j = i + 1
                while not lines[j][1]: j += 1
                res[cur] = (lines[j][1], lines[j][0])
            m2 = re.match(r'Rozstrzygnięcie: (Tak|Nie)\.', l)
            if m2: res[cur] = (m2.group(1), pg)
    return res

def key_mat():
    d = pymupdf.open(ZR + r'\matematyka-2026-maj-matura-podstawowa-odpowiedzi.pdf')
    res = {}
    for pi, p in enumerate(d):
        words = p.get_text('words')
        for i, w in enumerate(words[:-1]):
            if w[4] == 'Wersja' and words[i + 1][4] == 'A':
                y, xA = w[1], w[0]
                xB = [v[0] for v in words if v[4] == 'Wersja' and abs(v[1] - y) < 2 and v[0] > xA + 50][0]
                below = [v for v in words if 5 < v[1] - y < 25 and xA - 5 <= v[0] < xB - 5]
                a = [v[4] for v in below if re.fullmatch(r'[A-D]|[PF]{2}', v[4])]
                t = [words[j + 1][4].rstrip('.') for j, v in enumerate(words[:-1]) if v[4] == 'Zadanie' and v[1] < y]
                res[t[-1]] = (a[0], pi + 1)
    return res

kw, km = key_wos(), key_mat()
mism = 0
for it in items:
    z = it['zadanie']
    k, pg = (kw if it['id'].startswith('WOS') else km)[z]
    if it['typ'] == 'choice':
        exp = k
    elif k in ('Tak', 'Nie'):
        exp = (k == 'Tak')
    else:
        idx = 0 if it['id'].endswith('-a') else 1
        exp = (k[idx] == 'P')
    kpg = int(re.search(r'\d+', it['zrodlo_klucza']).group())
    ok = (exp == it['poprawna']) and (kpg == pg)
    if not ok: mism += 1
    print(('OK ' if ok else 'ROZBIEŻNOŚĆ '), it['id'], '| klucz:', k, 's.', pg, '| w pliku:', it['poprawna'], it['zrodlo_klucza'])
print('rozbieżności:', mism, '/', len(items))

# kontrola słów polskich w zadaniach z matematyki względem warstwy tekstowej strony
d = pymupdf.open(ZR + r'\matematyka-2026-maj-matura-podstawowa.pdf')
bad = 0
for it in items:
    if not it['id'].startswith('MAT'): continue
    txt = ' '.join(d[n - 1].get_text() for n in range(it['strona_pdf'] - 1, it['strona_pdf'] + 1))
    words = set(re.findall(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{4,}', txt))
    src = it['material_zrodlowy'] + ' ' + it['tresc'] + ' ' + it['polecenie'] + ' ' + ' '.join((it.get('opcje') or {}).values())
    for w in set(re.findall(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{4,}', src)):
        if w in ('sqrt',): continue
        if w not in words:
            bad += 1; print('MAT słowo spoza strony:', it['id'], w)
print('MAT: podejrzanych słów:', bad)
