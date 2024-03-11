import logging

from typing import Union
from app import ENVIRONMENT


class AppConfig:
    def __init__(self, name: str = "Titanic Survivor App", log_level: Union[int, str] = 20):
        self._name = name

        if log_level == "dev" or log_level == "DEV":
            self._log_level = "DEBUG"
        elif log_level == "prod" or log_level == "PROD":
            self._log_level = "INFO"
        else:
            raise ValueError(f"Provided environment '{ENVIRONMENT}' is not supported. Please select the environment "
                             f"from ['dev', 'prod', 'DEV', 'PROD']")

        self._log_config = self._init_logger()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        assert isinstance(name, str)
        self._name = name

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, log_level):
        assert (isinstance(log_level, Union[int, str]) and
                log_level in [10, 20, 30, 40, 50, "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])

        match log_level:
            case 10 | "DEBUG":
                self._log_level = "DEBUG"
            case 20 | "INFO":
                self._log_level = "INFO"
            case 30 | "WARNING":
                self._log_level = "WARNING"
            case 40 | "ERROR":
                self._log_level = "ERROR"
            case 50 | "CRITICAL":
                self._log_level = "CRITICAL"

        self._log_config = self._init_logger()

    @property
    def log_config(self):
        return self._log_config

    def _init_logger(self):

        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                'access': {
                    '()': 'uvicorn.logging.AccessFormatter',
                    'fmt': '%(levelprefix)s %(asctime)s - %(client_addr)s - "%(request_line)s" %(status_code)s',
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "use_colors": True
                },
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(levelprefix)s %(asctime)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "use_colors": True
                },
            },
            "handlers": {
                'access': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'access',
                    'stream': 'ext://sys.stdout'
                },
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
            },
            "loggers": {
                self._name: {
                    "handlers": ["default"],
                    "level": f"{self._log_level}",
                    "propagate": False
                },
                "uvicorn": {
                    "handlers": ["default"],
                    "level": f"{self._log_level}",
                    "propagate": True
                },
                'uvicorn.access': {
                    'handlers': ['access'],
                    'level': f"{self._log_level}",
                    'propagate': False
                },
                'uvicorn.error': {
                    'level': f"{self._log_level}",
                    'propagate': False
                }
            },
        }
        return log_config

    def get_logger(self):
        return logging.getLogger(self._name)


app_config = AppConfig(log_level=ENVIRONMENT)
