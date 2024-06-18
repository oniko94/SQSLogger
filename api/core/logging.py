# -*- coding: utf-8 -*-
import colorama
import coloredlogs
import logging
import os

from typing import Union


colorama.init()


def create_logger(_logger: Union[logging.Logger, str]) -> logging.Logger:
    if isinstance(_logger, str):
        _logger = logging.getLogger(_logger)

    _logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(
        coloredlogs.ColoredFormatter(
            fmt="%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s",
            level_styles={
                "debug": {"color": "white"},
                "info": {"color": "green"},
                "warning": {"color": "yellow"},
                "error": {"color": "red"},
                "critical": {"color": "red", "bold": True},
            },
        )
    )
    _logger.handlers.clear()
    _logger.addHandler(handler)

    if os.getenv("DEBUG", "0") == "1":
        _logger.setLevel(logging.DEBUG)
    else:
        _logger.setLevel(logging.INFO)

    return _logger
