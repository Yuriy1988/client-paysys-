class RULES:
    pass


def handler_registrar():
    registry = []

    def scorers_registrar(if_true, if_false):
        def handler(func):
            func.score_if_true = if_true
            func.score_if_false = if_false
            registry.append(func)
            return func

        return handler

    scorers_registrar.handlers = registry
    return scorers_registrar

score = handler_registrar()  # Takes 2 parameters score_if_true and score_if_false


def get_score(payment):
    _score = 0
    for handler in score.handlers:
        if handler(payment):
            _score += handler.score_if_true
        else:
            _score += handler.score_if_false
    return _score


@score(1, -1)
def is_trust_location(payment):
    pass


@score(-1, 0)
def is_in_blacklist(payment):
    pass


@score(1, 0)
def is_in_whitelist(payment):
    pass


@score(1, -1)
def is_normal_amount(payment):
    pass


@score(1, -1)
def is_normal_count(payment):
    pass
