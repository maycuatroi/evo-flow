from evoflow.entities.core.session import Session


def create_session(*args, **kwargs):
    return Session(*args, **kwargs)
