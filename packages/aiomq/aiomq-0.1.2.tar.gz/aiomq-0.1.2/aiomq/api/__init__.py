import logging
import socket
from ssl import SSLContext
from typing import Optional, Coroutine, Type, Callable, Any

from aiohttp.abc import AbstractAccessLogger
from aiohttp.log import access_logger
from aiohttp.web import _run_app as run_app
from aiohttp.web_log import AccessLogger

from .bootstrap import app
from .db import init_db

def aio_api(host: Optional[str] = None,
            port: Optional[int] = None,
            path: Optional[str] = None,
            sock: Optional[socket.socket] = None,
            shutdown_timeout: float = 60.0,
            ssl_context: Optional[SSLContext] = None,
            print: Callable[..., None] = print,
            backlog: int = 128,
            access_log_class: Type[AbstractAccessLogger] = AccessLogger,
            access_log_format: str = AccessLogger.LOG_FORMAT,
            access_log: Optional[logging.Logger] = access_logger,
            handle_signals: bool = True,
            reuse_address: Optional[bool] = None,
            reuse_port: Optional[bool] = None) -> Coroutine[Any, Any, None]:
    return run_app(app,
                   host=host,
                   port=port,
                   path=path,
                   sock=sock,
                   shutdown_timeout=shutdown_timeout,
                   ssl_context=ssl_context,
                   print=print,
                   backlog=backlog,
                   access_log_class=access_log_class,
                   access_log_format=access_log_format,
                   access_log=access_log,
                   handle_signals=handle_signals,
                   reuse_address=reuse_address,
                   reuse_port=reuse_port)
