from datetime import datetime, timezone

try:
    from pymongo import MongoClient
    MONGO_AVAILABLE = True
except ImportError:
    MONGO_AVAILABLE = False


def get_collection(uri: str = "mongodb://localhost:27017/", db: str = "cwk_audit"):
    if not MONGO_AVAILABLE:
        raise RuntimeError("pymongo not installed. Run: pip install pymongo")
    client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    return client[db]["sandbox_runs"]


def store_run(
    script_name: str,
    static_features: dict,
    dynamic_features: dict,
    score: float,
    label: str,
    breakdown: dict,
    report_text: str,
    uri: str = "mongodb://localhost:27017/"
) -> str:
    """
    Persist one sandbox evaluation to MongoDB.
    Returns the inserted document id as a string.
    Silently skips if MongoDB is unavailable.
    """
    if not MONGO_AVAILABLE:
        return "mongo_unavailable"
    try:
        col = get_collection(uri)
        doc = {
            "script":          script_name,
            "timestamp":       datetime.now(timezone.utc).isoformat(),
            "static_features": static_features,
            "dynamic_features": dynamic_features,
            "risk_score":      score,
            "label":           label,
            "breakdown":       breakdown,
            "explanation":     report_text,
        }
        result = col.insert_one(doc)
        return str(result.inserted_id)
    except Exception as e:
        return f"mongo_error: {e}"


def query_runs(label_filter: str = None, uri: str = "mongodb://localhost:27017/") -> list:
    """Return all stored runs, optionally filtered by label."""
    if not MONGO_AVAILABLE:
        return []
    try:
        col   = get_collection(uri)
        query = {"label": label_filter} if label_filter else {}
        return list(col.find(query, {"_id": 0}))
    except Exception:
        return []