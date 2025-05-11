from fastapi import FastAPI
import json
import requests
import logging
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

logger_provider = LoggerProvider(resource=Resource.create({SERVICE_NAME: "fastapi-otel"}))
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(OTLPLogExporter(endpoint="http://otel-lgtm:4318/v1/logs"))
)

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
LoggingInstrumentor().instrument(set_logging_format=True)

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/nome/{nome}")
def home(nome: str):
    return {"message": f"Hello {nome}"}


@app.get("/api")
def consulta_api():
    json_response = json.loads(requests.get("https://jsonplaceholder.typicode.com/todos/1", verify=False).text)
    logger.warning("🔥 Consulta realizada com sucesso!", extra={"rota": "/api"})
    return json_response

