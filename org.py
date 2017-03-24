date_format = '%Y-%m-%d %a %H:%M'

def drawer_keyword(name):
    return wrap(name.upper(), ':')

def drawer_value(key, value):
    return drawer_keyword(key) + '  ' + value

def drawer(name, entries):
    return '''%s
%s
:END:
''' % (drawer_keyword(name), '\n'.join([drawer_value(k, v) for k,v in entries]))

def date(date):
    return date.strftime(date_format)
    #return '2016-11-24 Thu 11:10'

def wrap(s, c='"'):
    return c + s + c

def paren(x, s='(', e=')'):
    return s + x + e

def brackets(x):
    return paren(x, '[', ']')

def inactive_date(date):
    return brackets(date)

def state_change(state, time):
    return '- %s %s' % (state, inactive_date(date(time)))

def headline(title, content, created=None, todo='', state_changes=[], properties=None, tags=[], indent=1):
    s = indent * '*' + ' '
    if todo:
        s += todo + ' '
    s += title
    if tags:
        s += ' ' + wrap(':'.join(tags), ':')
    s += '\n'
    if not properties:
        properties = []
    if created:
        properties.append(('created', inactive_date(date(created))))
    s += drawer('properties', properties) + '\n'
    s += content
    if state_changes:
        s += '\n\n:LOGBOOK:\n'
        s += '\n'.join([state_change(s, t) for s, t in state_changes])
        s += '\n:END:'

    return s

