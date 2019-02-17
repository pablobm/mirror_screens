class DisplayInfo:
    def __init__(self, displays):
        self.displays = displays

    @property
    def primary(self):
        return self._find_screen_with_primary_marker() or self._find_first_screen_with_current_mode_marker()

    def _find_screen_with_primary_marker(self):
        try:
            return next(d for d in self.displays if d.marked_primary)
        except StopIteration:
            # No screeen marked as primary
            None

    def _find_first_screen_with_current_mode_marker(self):
        try:
            return next(d for d in self.displays if d.current_mode)
        except StopIteration:
            # No screeen with a mode marked as current
            None

    @property
    def secondaries(self):
        primary = self.primary
        return [d for d in self.displays if d != primary]


class Display:
    def __init__(self):
        self.name = None
        self.marked_primary = False
        self.modes = []

    @property
    def current_mode(self):
        try:
            return next(d for d in self.modes if d.marked_current)
        except StopIteration:
            # No screeen with a mode marked as current
            None

    @property
    def max_mode(self):
        best = None
        max_prod = 0
        for m in self.modes:
            if max_prod < m.w * m.h:
                best = m
                max_prod = m.w * m.h
        return best


class Mode:
    def __init__(self, w, h, marked_current=False):
        self.w = w
        self.h = h
        self.marked_current = marked_current

    def correction_for(self, other):
        return CorrectionFactor(float(self.w) / other.w, float(self.h) / other.h)

    def __str__(self):
        return '%sx%s' % (self.w, self.h)

    def __repr__(self):
        attrs = [repr(self.w), repr(self.h)]
        if self.marked_current:
            attrs.append("marked_current=True")

        _attrs = ", ".join(attrs)
        return "%s(%s)" % (self.__class__.__name__, _attrs)


class CorrectionFactor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '%sx%s' % (self.x, self.y)
