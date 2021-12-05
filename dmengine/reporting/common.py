TRANSLATE = [('->', '$\\rightarrow$'),
             ('...', '\\dots '),
             ('[', '$[$'),
             (']', '$]$'),
             ('_', '\\_')]


def translate(string):
    for old, new in TRANSLATE:
        string = string.replace(old, new)
    return string


def tabular(table, *, row_headings=True, col_headings=True,
            cnt_content=False, cnt_table=False):
    n_cols = len(table[0])
    result = ['\\begin{tabular}[t]{l%s*{%d}{%s}}\n' %
        ('|' if row_headings else '', n_cols - 1, 'c' if cnt_content else 'l')]
    table = iter(table)
    if col_headings:
        result.append('\t%s\\\\\\hline\n' % '\t&'.join(next(table)))
    for row in table:
        cols = iter(row)
        result.append('\t%s\t&%s\\\\\n' % (next(cols), '\t&'.join(cols)))
    result.append('\\end{tabular}\n')
    if cnt_table:
        result.insert(0, '\\begin{center}\n')
        result.append('\\end{center}\n')
    return ''.join(result)
