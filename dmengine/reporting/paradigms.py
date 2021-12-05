from .common import tabular
from .features import render_features
from .inputs import render_slotlist
from .tools import grouper
from .vis import render_exponent


def is_transitive(paradigm):
    filled_headers = tuple(bool(h) for h in paradigm['headers'])
    return {(True, False): False, (True, True): True}[filled_headers]


def intrans_paradigm(headers, cells, *, center=False):
    table = list(zip(headers[0], cells))
    return tabular(table, col_headings=False, cnt_table=center)


def trans_paradigm(headers, cells, *, caption='', center=False):
    hrows, hcols = headers
    ncols = len(hcols)
    table = [[caption] + hcols]
    table.extend([head] + list(row)
        for head, row in zip(hrows, grouper(ncols, cells)))
    return tabular(table, cnt_table=center)


def collumns(cells, n_cols, n_rows):
    n_cells = n_cols * n_rows
    for i in range(n_cols):
        yield cells[i:n_cells:n_rows]


def folded_paradigm(headers, cells, *, center=False):
    r_headers, c_headers = headers
    n_rows, n_cols = map(len, headers)
    tabs = (tabular([['', h]] + list(zip(r_headers, col)), cnt_table=center)
            for h, col in zip(c_headers, collumns(cells, n_rows, n_cols)))
    return '\n'.join(tabs)


def para_logs(paradigms, worklog):
    log_cursor = 0
    for paradigm in paradigms:
        log_slice = slice(log_cursor, log_cursor + len(paradigm['inputs']))
        yield paradigm, worklog[log_slice]
        log_cursor = log_slice.stop


def paradigms(paradigms, worklog):
    tabs = []
    for paradigm, logs in para_logs(paradigms, worklog):
        spellouts = [l['spellout'] for l in logs]
        para_func = trans_paradigm if is_transitive(paradigm) else intrans_paradigm
        tabs.append('\\subsection{%s}\n' % paradigm['name'])
        tabs.append(para_func(paradigm['headers'],
                              list(map(render_exponent, spellouts))))
    return ''.join(tabs)


def trans_inp(inp):
    return ''.join(render_features(f, brackets=True) for f in inp)


def input_paradigms(paradigms):
    tabs = ['\\small\n']
    for paradigm in paradigms:
        tab = ['\\subsection{%s}\n' % paradigm['name']]
        para_func = folded_paradigm if is_transitive(paradigm) else intrans_paradigm
        tab.append(para_func(paradigm['headers'],
                             list(map(trans_inp, paradigm['inputs'])),
                             center=True))
        tabs.append(''.join(tab))
    return ''.join(tabs)


def input_paradigms_processed(paradigms, worklog):
    tabs = ['\\small\n']
    for paradigm, logs in para_logs(paradigms, worklog):
        tab = ['\\subsection{%s}\n' % paradigm['name']]
        para_func = folded_paradigm if is_transitive(paradigm) else intrans_paradigm
        tab.append(para_func(paradigm['headers'],
                             [render_slotlist(log['input_pst']) for log in logs],
                             center=True))
        tabs.append(''.join(tab))
    return ''.join(tabs)
