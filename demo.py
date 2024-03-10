from loguru import logger

# 自定义日志格式
logger.add("file.log", format="{time} {level} {message}", level="DEBUG")

logger.debug("这是一条具有自定义格式的日志信息")
