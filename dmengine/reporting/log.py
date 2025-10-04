from itertools import pairwise, product, repeat

from .features import render_features
from .inputs import render_slotlist, render_slot, render_head
from .paradigms import is_transitive, para_logs
from .vis import render_exponent, render_vi


def render_log(paradigms, worklog, rules, readjustments):
    return '\n'.join(lines(paradigms, worklog, rules, readjustments))


def lines(paradigms, worklog, rules, readjustments):
    yield '\\footnotesize'
    for paradigm, logs in para_logs(paradigms, worklog):
        yield '\\subsection{%s}' % paradigm['name']
        if is_transitive(paradigm):
            sub_obj = product(*paradigm['headers'])
        else:
            sub_obj = zip(paradigm['headers'][0], repeat(''))
        for log, (sub, obj) in zip(logs, sub_obj):
            if obj:
                yield '\\minisec{%s:%s}' % (sub, obj)
            else:
                yield '\\minisec{%s}' % sub
            yield 'Input (Rule applied)'
            yield '\\begin{itemize}'
            yield '\\item %s' % render_slotlist(log['input_pre'])
            for i, (pre, pst) in enumerate(pairwise([log['input_pre']] + log['input_pro'])):
                if pst is not pre:
                    rule = rules[i]
                    yield '\\item %s %s' % (render_slotlist(pst), rule['ref'])
            yield '\\end{itemize}\n'
            if not log['inserts']:
                continue
            yield 'Matches'
            yield '\\begin{itemize}'
            for slt, slt_match in zip(log['input_pst'], log['matches']):
                yield '\\item %s' % render_slot(slt)
                yield '\\begin{itemize}'
                for hd, hd_match in zip(slt, slt_match):
                    yield '\\item %s' % render_head(hd)
                    yield '\\begin{itemize}'
                    for match in hd_match:
                        yield '\\item %s' % render_features(match['head'])
                        if not match['matches']:
                            continue
                        yield '\\begin{itemize}'
                        for m in match['matches']:
                            yield '\\item %s %s' % (render_vi(m), m['ref'])
                        yield '\\end{itemize}'
                    yield '\\end{itemize}'
                yield '\\end{itemize}'
            yield '\\end{itemize}\n'
            yield 'Inserts'
            yield '\\begin{itemize}'
            yield '\\item %s' % insertlist(log['inserts'])
            yield '\\end{itemize}\n'
            yield 'Output (Readjustment applied)'
            yield '\\begin{itemize}'
            yield '\\item %s' % vilist(log['output_pre'])
            for i, (pre, pst) in enumerate(pairwise([log['output_pre']] + log['output_pro'])):
                if pst is not pre:
                    readjustment = readjustments[i]
                    yield '\\item %s %s' % (vilist(pst), readjustment['ref'])
            yield '\\end{itemize}\n'
            yield 'Spellout'
            yield '\\begin{itemize}'
            yield '\\item %s' % render_exponent(log['spellout'])
            yield '\\end{itemize}\n'


def explist(exponents):
    return '\\quad '.join(render_exponent(e) for e in exponents)


def insertlist(slots):
    return '\\quad '.join(
            '\\#%s\\#' % ','.join(
                '%s %s' % (render_exponent(vi['exponent']), vi['ref'].rstrip())
                for vi in slot)
           for slot in slots)


def vilist(vis):
    return explist(vi['exponent'] for vi in vis)
