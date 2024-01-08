import importlib
import logging
import multiprocessing

import watchfiles
from typer import Typer

app = Typer()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger.addHandler(handler)
handler.setFormatter(formatter)


def start(import_str: str):
    module, obj = import_str.split(":")
    module = importlib.import_module(module)
    obj = getattr(module, obj)
    obj()


@app.command()
def main(import_str: str, reload: bool = True):
    if not reload:
        raise NotImplementedError("Not implemented yet")

    logger.info(f"Starting {import_str}")
    t = worker_factory(import_str)
    try:
        t.start()
        for change in watchfiles.watch("main.py"):
            logger.info(f"Detected change in {change}")
            t.terminate()
            t = worker_factory(import_str)
            t.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt")
        raise
    finally:
        t.terminate()
    logger.info("quitting")


def worker_factory(import_str):
    return multiprocessing.Process(target=start, args=(import_str,))


if __name__ == "__main__":
    app()
