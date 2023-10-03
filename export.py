#!/usr/bin/env python
import argparse

import org

import re

from datetime import datetime

import shutil
import os

state_file_name = '.last_export.orgexport'

def main():
    

    ap = argparse.ArgumentParser()
    ap.add_argument('inputfile')

    args = ap.parse_args()

    #do not try to import notes from your ebookreader from before 1970
    last_export = datetime(year=1970, month=1, day=1)
    last_export_lines = []
    state_file = os.path.join(os.path.dirname(args.inputfile), state_file_name)

    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            lines = f.read()
        lines = lines.split('\n')
        last_export_lines = [l for l in lines if l]
        last_export = datetime.strptime(last_export_lines[-1], org.date_format)

    with open(args.inputfile, 'r') as inputfile:
        text = inputfile.read()

    note_sep = '''
-----------------------------------

'''

    notes = text.split(note_sep)

    note_re = re.compile(r'\n'.join([
        r'(?P<title>.+)'
        , r'((?P<type>Lesezeichen|Markierung|Notiz)[  ]+auf Seite[  ]+(?P<page>.+): )'
        #note is optional
        + r'''((?P<note>(?:.|\n)*)
)?''' + r'"(?P<quote>(?:.|\n)*)"'
        , r'''Hinzugefügt am (?P<day>\d{2}).(?P<month>\d{2}).(?P<year>\d{4}) \| (?P<hour>\d{1,2}):(?P<minute>\d{2})
''']))

    types = dict(
        Markierung='highlighted'
        , Notiz='note'
        , Lesezeichen='marker'
        )

    dont_export = ['marker']

    for note in notes:
        if not note:
            continue
        #print('---------"' + note + '"')
        m = note_re.match(note)

        assert(m)

        d = {}
        for k in ('year', 'month', 'day', 'hour', 'minute'):
            d[k] = int(m.group(k))

        created = datetime(**d)
        
        if created < last_export:
            continue
        
        book = m.group('title')
        page = m.group('page')
        typ = types[m.group('type')]
        if typ in dont_export:
            continue
        quote = m.group('quote')

        title = quote
        title = org.wrap(title, '"')
        if typ == 'note':
            title = m.group('note')

        title.replace('\n', ' ')
        n = 20
        content = ''
        title_words = title.split()
        if len(title_words) > n:
            #content += '[…] ' + org.wrap(' '.join(title_words[n:])) + '\n\n'
            title = ' '.join(title_words[:n])
            title += ' […]'


        content += '\n#+begin_quote\n' + quote + '\n#+end_quote\n'

        content += '\nFrom "' + book + '"' + ', p.' + page + '\n'
        
        s = org.headline(title, content, created, tags=[typ])
        print(s)
        print('\n')

    last_export_lines.append(datetime.now().strftime(org.date_format))
    with open(state_file, 'w+') as f:
        f.write('\n'.join(last_export_lines))

if __name__ == '__main__':
    main()
