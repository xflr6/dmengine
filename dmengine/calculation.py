# calculation.py - rules, vocabulary item insertion, readjustments

"""Calculate the outputs for rules, vocabulary item insertion, readjustments."""

import logging

from . import insertion

__all__ = ['Calculator']


log = logging.getLogger()


class Calculator(object):
    """Execute pre-insertion rules, vocabulary item insertion, post-insertion readjustments."""

    Insertion = insertion.Insertion

    def __init__(self, insertion, inputs, rules, vis, readjustments):
        self.insertion = self.Insertion(insertion, vis)
        self.inputs = inputs
        self.rules = Rules(rules)
        self.readjustments = Readjustments(readjustments)

    def __call__(self):
        self.logs = logs = []
        self.outputs = outputs = []
        self.spellouts = spellouts = []

        for input_pre in self.inputs:
            log.debug(f'-- \n{input_pre}')

            input_pro, input_pst = self.rules(input_pre)

            matches, inserts, output_pre = self.insertion(input_pst)

            output_pro, output_pst = self.readjustments(output_pre)

            spellout = output_pst.exponents.spellout

            log.debug('"{}"'.format(spellout.encode('ascii', 'backslashreplace')))
            logs.append({
                'input_pre': input_pre, 'input_pro': input_pro, 'input_pst': input_pst,
                'matches': matches, 'inserts': inserts,
                'output_pre': output_pre, 'output_pro': output_pro, 'output_pst': output_pst,
                'spellout': spellout,
            })

            outputs.append(output_pst)

            spellouts.append(spellout)

        return logs, outputs, spellouts


class Executor(object):
    """Sequentially compute outputs for each rule to the given input item."""

    Outputs = list

    def __init__(self, rules):
        self.rules = rules

    def __call__(self, item):
        outputs = self.Outputs()

        for r in self.rules:
            copy = item.copy()
            if r(copy):
                item = copy
                log.debug(f' {r}\n{item}')

            outputs.append(item)

        result = outputs[-1] if outputs else item

        return outputs, result


class Rules(Executor):
    """Execute pre-insertion rules on hierarchies of heads."""


class Readjustments(Executor):
    """Execute post-insertion readjustments sequences of vis."""
