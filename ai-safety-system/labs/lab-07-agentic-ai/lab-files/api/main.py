import os
import time
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI(title="Demo REST API", version="1.0.0")

# Prometheus metrics counters
REQ_COUNT = Counter("requests_total", "Total requests", ["endpoint", "status"])
REQ_LAT = Histogram("request_latency_seconds", "Latency", ["endpoint"])
ERR_COUNT = Counter("errors_total", "Total errors", ["endpoint", "type"])


class OrderIn(BaseModel):
    item: str
    quantity: int


orders = {}
order_id_seq = 1


def maybe_inject_failure(p: float = 0.0):
    if random.random() < p:
        raise RuntimeError("Injected failure for lab demonstration")


@app.get("/health")
def health():
    return {"status": "ok", "time": int(time.time())}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/v1/orders/{order_id}")
def get_order(order_id: int):
    endpoint = "/v1/orders/{id}"
    with REQ_LAT.labels(endpoint=endpoint).time():

        order = orders.get(order_id)
        if order is None:
            REQ_COUNT.labels(endpoint=endpoint, status="404").inc()
            raise HTTPException(status_code=404, detail="Order not found")

        REQ_COUNT.labels(endpoint=endpoint, status="200").inc()
        return {"id": order_id, **order}


@app.post("/v1/orders", status_code=201)
def create_order(order: OrderIn):
    global order_id_seq
    endpoint = "/v1/orders"

    with REQ_LAT.labels(endpoint=endpoint).time():

        fail_rate = float(os.getenv("FAIL_RATE", "0.0"))
        maybe_inject_failure(fail_rate)

        if order.quantity <= 0:
            REQ_COUNT.labels(endpoint=endpoint, status="400").inc()
            raise HTTPException(status_code=400, detail="Quantity must be positive")

        order_id = order_id_seq
        order_id_seq += 1

        orders[order_id] = {
            "item": order.item,
            "quantity": order.quantity,
            "created_at": int(time.time())
        }

        REQ_COUNT.labels(endpoint=endpoint, status="201").inc()
        return {"id": order_id, **orders[order_id]}


@app.get("/v1/slow")
def slow():
    endpoint = "/v1/slow"
    with REQ_LAT.labels(endpoint=endpoint).time():
        time.sleep(random.uniform(0.2, 1.2))
        REQ_COUNT.labels(endpoint=endpoint, status="200").inc()
        return {"ok": True}