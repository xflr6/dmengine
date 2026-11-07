from .features import render_features


def render_slotlist(slots) -> str:
    return '\\quad '.join(map(render_slot, slots))


def render_slot(slot) -> str:
    return '\\#%s\\#' % ' '.join(map(render_head, slot))


def render_head(head):
    return render_features(head, brackets=True)
