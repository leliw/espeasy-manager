import logging
import uvicorn.logging


def setup_logging():
    ch = logging.StreamHandler()
    ch.setFormatter(
        uvicorn.logging.DefaultFormatter("%(levelprefix)s %(name)s: %(message)s")
    )
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.INFO)
