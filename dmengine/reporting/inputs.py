from .features import render_features


def render_slotlist(slots):
    return '\\quad '.join(render_slot(s) for s in slots)


def render_slot(slot):
    return '\\#%s\\#' % ' '.join(render_head(h) for h in slot)


def render_head(head):
    return render_features(head, brackets=True)
