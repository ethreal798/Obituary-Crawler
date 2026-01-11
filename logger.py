from loguru import logger
from config import LOGGER_HANDLERS

# 清除默认 handler
logger.remove()

# 动态添加所有 handler
for handler_config in LOGGER_HANDLERS:
    logger.add(**handler_config)

# 导出 logger
__all__ = ["logger"]

