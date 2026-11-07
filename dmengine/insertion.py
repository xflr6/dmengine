"""Insert vocabulary items: Cyclic, Single, Flat, Once."""

import logging
import operator

from . import meta
from . import tools
from . import vis

__all__ = ['Insertion']


log = logging.getLogger()


class Insertion(metaclass=meta.FactoryMeta('kind')):  # type: ignore[metaclass]  # noqa: E501
    """Insertion of vocabulary items into hierarchies of potentially fused heads."""

    single = False

    Matches = list

    Inserts = list

    Output = vis.ViList

    def __init__(self, vis) -> None:
        self.vis = vis

    def __call__(self, slots):
        matches = self.Matches()
        inserts = self.Inserts()
        output = self.Output()

        for slot, left, right in tools.curr_pred_succ(slots):
            log.debug(slot)
            slot_matches, slot_output = self.insert_slot(slot, left, right)
            slot_output.sort()

            if self.single:
                slot_output = slot_output[:1]

            matches.append(slot_matches)
            inserts.append(slot_output)
            output.extend(slot_output)

        log.debug('%s\n%s', slots, output)
        return matches, inserts, output


class Cyclic(Insertion):
    """Insert consuming markers as long as there is a matching marker."""

    kind = 'cyclic'

    def insert_slot(self, slot, left, right):
        slot_matches = self.Matches()
        slot_output = self.Output()

        for head, up in tools.curr_other(slot):
            head_matches = self.Matches()
            head_output = self.Output()
            is_matching = operator.methodcaller('match', head, left, right, up)

            while True:
                matching = self.vis.filter(is_matching)
                matching.sort()
                head_matches.append({'head': head.values_visible,
                                     'matches': matching})

                if not matching:
                    log.debug(' %s inserted %s no more matches',
                              head, head_matches)
                    break

                matching_str = '\n'.join(f'    {m}' for m in matching)
                log.debug(' %s matches\n%s', head, matching_str)
                most_specific = matching[0]
                head.consume(most_specific.features)
                head_output.append(most_specific)

            slot_matches.append(head_matches)
            slot_output.extend(head_output)

        return slot_matches, slot_output


class Single(Cyclic):
    """Retreat to the most specific marker for each slot."""

    kind = 'single'

    single = True


class Flat(Insertion):

    kind = 'flat'

    def insert_slot(self, slot, left, right):
        matches = self.Matches()
        output = self.Output()

        while True:
            matching = self.vis.matching_(slot, left, right)
            matching.sort()
            matches.append(matching.as_dicts())

            if not matching:
                output_str = output if output else 'nothing'
                log.debug(' inserted %s no more matches', output_str)
                break

            matching_str = '\n   '.join(f'{head} {vi}' for head, vi in matching)
            log.debug(' matches\n   %s', matching_str)
            (head, most_specific) = matching[0]
            head.consume(most_specific.features)

            log.debug(' %s', slot)
            output.append(most_specific)

        return matches, output


class Once(Insertion):
    """Insert every matching markers exactly once."""

    kind = 'once'

    def insert_slot(self, slot, left, right):
        slot_matches = self.Matches()
        slot_output = self.Output()

        for head, up in tools.curr_other(slot):
            matching = self.vis.matching(head, left, right, up)
            matching_str = '\n'.join(f'    {m}' for m in matching)
            log.debug(' %s matches\n%s', head, matching_str)

            head_matches = [{'head': head.values, 'matches': matching}]
            head_output = matching
            log.debug(' %s inserted %s', head, head_output)

            slot_matches.append(head_matches)
            slot_output.extend(head_output)

        return slot_matches, slot_output
