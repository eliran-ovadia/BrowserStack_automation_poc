# flows/base_flow.py
import logging


class BaseFlow:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def log_step(self, message: str, level: str = "INFO"):
        """Log a test step without forcing screenshots."""
        if level.upper() == "CRITICAL":
            self.logger.critical(f"STEP: {message}")
        elif level.upper() == "ERROR":
            self.logger.error(f"STEP: {message}")
        else:
            self.logger.info(f"STEP: {message}")
