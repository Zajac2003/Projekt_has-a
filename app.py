from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


def format_duration(seconds):
    total_seconds = max(1, int(seconds))
    if total_seconds < 60:
        return f"{total_seconds} s"

    minutes, remaining_seconds = divmod(total_seconds, 60)
    if minutes < 60:
        if remaining_seconds:
            return f"{minutes} min {remaining_seconds} s"
        return f"{minutes} min"

    hours, remaining_minutes = divmod(minutes, 60)
    if remaining_minutes:
        return f"{hours} h {remaining_minutes} min"
    return f"{hours} h"


def estimate_analysis_time(row):
    algorithm = row["algorithm"].lower()
    hash_length = len(row["hash"])

    base_seconds = {
        "md5": 35,
        "sha1": 90,
        "bcrypt": 720,
        "argon2id": 1800,
    }.get(algorithm, 180)

    if hash_length > 50:
        base_seconds *= 1.35
    elif hash_length < 35:
        base_seconds *= 0.85

    return format_duration(base_seconds)


DEMO_ROWS = [
    {
        "id": 1,
        "username": "anna.kowalska",
        "email": "anna.kowalska@example.edu",
        "hash": "$2b$12$F9xX3d5n8vYp0mV6tXl3EeYq8B7m1JgkQe2r4W1b9cD6f7a8s9h0u",
        "algorithm": "bcrypt",
        "status": "Nieznany",
    },
    {
        "id": 2,
        "username": "mateusz.nowak",
        "email": "mateusz.nowak@example.edu",
        "hash": "5f4dcc3b5aa765d61d8327deb882cf99",
        "algorithm": "MD5",
        "status": "Nieznany",
    },
    {
        "id": 3,
        "username": "ola.wisniewska",
        "email": "ola.wisniewska@example.edu",
        "hash": "e10adc3949ba59abbe56e057f20f883e",
        "algorithm": "MD5",
        "status": "Nieznany",
    },
    {
        "id": 4,
        "username": "piotr.zielinski",
        "email": "piotr.zielinski@example.edu",
        "hash": "$argon2id$v=19$m=65536,t=3,p=4$demo$placeholder",
        "algorithm": "Argon2id",
        "status": "Nieznany",
    },
    {
        "id": 5,
        "username": "karolina.wojcik",
        "email": "karolina.wojcik@example.edu",
        "hash": "12dea96fec20593566ab75692c9949596833adc9",
        "algorithm": "SHA1",
        "status": "Nieznany",
    },
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/rows")
def rows():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify(
            [
                {**row, "analysis_time": estimate_analysis_time(row)}
                for row in DEMO_ROWS
            ]
        )

    filtered = []
    for row in DEMO_ROWS:
        haystack = " ".join(str(value) for value in row.values()).lower()
        if query in haystack:
            filtered.append({**row, "analysis_time": estimate_analysis_time(row)})
    return jsonify(filtered)


@app.route("/api/simulate", methods=["POST"])
def simulate():
    payload = request.get_json(silent=True) or {}
    row_id = payload.get("id")

    for row in DEMO_ROWS:
        if row["id"] == row_id:
            return jsonify(
                {
                    "id": row_id,
                    "status": "Symulacja zakończona",
                    "result": "Demo: wykryto dopasowanie w słowniku pokazowym",
                    "candidate": "password123",
                    "analysis_time": estimate_analysis_time(row),
                }
            )

    return jsonify({"error": "Nie znaleziono wiersza"}), 404


if __name__ == "__main__":
    app.run(debug=True)