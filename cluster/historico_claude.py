# -*- coding: utf-8 -*-
"""
Historico legivel da conversa do Claude Code do vlab (o .jsonl mais recente em .claude_persist):
VOCE / CLAUDE / COMANDO (exato) / RESULTADO (fim da saida). So le; nao muda nada.
Uso: python3 historico_claude.py [N]      (N = ultimos eventos; padrao 60)
"""
import glob
import json
import os
import sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
P = '/home/jovyan/privado/.claude_persist/.claude/projects'
arqs = glob.glob(P + '/*/*.jsonl')
if not arqs:
    print('nenhum historico em', P)
    sys.exit(0)
f = max(arqs, key=os.path.getmtime)
ev = []
for l in open(f, encoding='utf-8'):
    try:
        d = json.loads(l)
    except Exception:
        continue
    c = (d.get('message') or {}).get('content')
    t = d.get('timestamp', '')[11:19] + ' UTC'
    if isinstance(c, str):
        ev.append((t, 'VOCE' if d.get('type') == 'user' else 'CLAUDE', c))
        continue
    for b in c or []:
        if not isinstance(b, dict):
            continue
        k = b.get('type')
        if k == 'text':
            ev.append((t, 'CLAUDE', b.get('text', '')))
        elif k == 'tool_use':
            i = b.get('input') or {}
            ev.append((t, 'COMANDO', i.get('command') or json.dumps(i, ensure_ascii=False)[:400]))
        elif k == 'tool_result':
            r = b.get('content')
            r = r if isinstance(r, str) else ' '.join(x.get('text', '') for x in (r or []) if isinstance(x, dict))
            ev.append((t, 'RESULTADO', r[-700:]))
print('historico:', f, '| eventos:', len(ev), '\n')
for t, k, x in ev[-N:]:
    print(f'[{t}] {k}:\n  ' + x.strip()[:1500].replace('\n', '\n  ') + '\n')
