from flask import Flask, request, make_response
from src.model import text_similarity_intersection, text_similarity_cos, text_similarity_kld
import json

app = Flask(__name__)

model_fun_mapping = {
    "Intersection": text_similarity_intersection,
    "KLD": text_similarity_kld,
    "Cos": text_similarity_cos
}

@app.route("/Similarity", methods=["POST"])
def hello_world():
    request_data = request.json
    if not request_data:
        return make_response(
            "Request body is not valid json",
            400,
        )
    metadata = request_data.get("Metadata", {})
    model = metadata.get("Model", "Cos")
    processing_fun = model_fun_mapping.get(model, "N/A")
    if processing_fun == "N/A":
        return make_response(
            f"Invalid model choice, options are {', '.join(model_fun_mapping.keys())}",
            400,
        )
    data = request_data.get("Data", {})
    if "FirstSample" not in data.keys() or "SecondSample" not in data.keys():
        return make_response(
            "Invalid request body, request must include a Data object with keys FirstSample and SecondSample",
            400,
        )
    resp = make_response(
        json.dumps(
            {
                "Score": processing_fun(data["FirstSample"], data["SecondSample"]),
                "Model": model,
            }
        )
    )
    resp.headers = {"Content-Type": "application/json"}
    return resp
