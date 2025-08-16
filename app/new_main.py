# Em construção 

from fastapi import FastAPI
import json, requests, logging

# --- OTel core imports
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Traces
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Logs
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

# Metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

# Instrumentations
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

resource = Resource.create({SERVICE_NAME: "fastapi-otel"})

# ---- Traces
trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-lgtm:4318/v1/traces"))
)
trace.set_tracer_provider(trace_provider)

# ---- Logs
logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(OTLPLogExporter(endpoint="http://otel-lgtm:4318/v1/logs"))
)
set_logger_provider(logger_provider)

# ---- Metrics
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://otel-lgtm:4318/v1/metrics")
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# ---- App + instr.
app = FastAPI()
FastAPIInstrumentor().instrument_app(app)   # traces + (if meter set) metrics
RequestsInstrumentor().instrument()         # traces + (if meter set) metrics

# Logging -> OTel logs
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
def home_nome(nome: str):
    return {"message": f"Hello {nome}"}

@app.get("/api")
def consulta_api():
    r = requests.get("https://jsonplaceholder.typicode.com/todos/1", verify=False)
    json_response = r.json()
    logger.warning(" Consulta realizada com sucesso!", extra={"rota": "/api"})
    return json_response
