import os

LOCAL_LLM_KIND = os.getenv("LOCAL_LLM_KIND", "")
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "")

SIMILARITY_MIN = float(os.getenv("SIMILARITY_MIN", "0.25"))
QA_MIN_COUNT = int(os.getenv("QA_MIN_COUNT", "15"))
SCHEMA_VERSION = os.getenv("SCHEMA_VERSION", "1.0")

LOG_PATH = os.getenv("LOG_PATH", "logs/run.jsonl")
