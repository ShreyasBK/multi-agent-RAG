import logging
import sys
from pythonjsonlogger.json import JsonFormatter
from backend.app.core.config import settings


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("multi-agent-rag")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # BetterStack log shipper (optional)
    if settings.betterstack_source_token:
        try:
            from logtail import LogtailHandler
            betterstack = LogtailHandler(source_token=settings.betterstack_source_token)
            betterstack.setFormatter(JsonFormatter(fmt="%(asctime)s %(levelname)s %(message)s"))
            logger.addHandler(betterstack)
        except ImportError:
            logger.warning("logtail not installed — BetterStack logging disabled")

    return logger


logger = setup_logging()
