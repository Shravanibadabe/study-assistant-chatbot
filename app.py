from flask import Flask, render_template, request, jsonify

from gemini_service import ask_gemini

from schedule_manager import (
    add_subject,
    get_subjects,
    add_task,
    get_pending_tasks,
    complete_task
)


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:

        return jsonify({
            "response": "Please enter a message."
        })


    try:

        answer = ask_gemini(message)

        return jsonify({
            "response": answer
        })


    except Exception as e:

        print("Gemini error:", e)

        return jsonify({
            "response": "Sorry, I couldn't process your request right now."
        }), 500


@app.route("/subjects", methods=["GET"])
def subjects():

    try:

        data = get_subjects()

        return jsonify(data)

    except Exception as e:

        print("Subject error:", e)

        return jsonify({
            "error": "Unable to load subjects."
        }), 500


@app.route("/subjects", methods=["POST"])
def create_subject():

    data = request.get_json()

    name = data.get("name")
    exam_date = data.get("exam_date")
    priority = data.get("priority", 1)

    if not name:

        return jsonify({
            "error": "Subject name is required."
        }), 400


    try:

        subject_id = add_subject(
            name,
            exam_date,
            priority
        )

        return jsonify({
            "message": "Subject added successfully.",
            "id": subject_id
        })


    except Exception as e:

        print("Add subject error:", e)

        return jsonify({
            "error": "Unable to add subject."
        }), 500


@app.route("/tasks", methods=["GET"])
def tasks():

    try:

        data = get_pending_tasks()

        return jsonify(data)

    except Exception as e:

        print("Task error:", e)

        return jsonify({
            "error": "Unable to load tasks."
        }), 500


@app.route("/tasks", methods=["POST"])
def create_task():

    data = request.get_json()

    subject_id = data.get("subject_id")
    topic = data.get("topic")
    due_date = data.get("due_date")
    duration = data.get("duration", 60)

    if not subject_id or not topic:

        return jsonify({
            "error": "Subject and topic are required."
        }), 400


    try:

        task_id = add_task(
            subject_id,
            topic,
            due_date,
            duration
        )

        return jsonify({
            "message": "Task added successfully.",
            "id": task_id
        })


    except Exception as e:

        print("Add task error:", e)

        return jsonify({
            "error": "Unable to add task."
        }), 500


@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def mark_task_complete(task_id):

    try:

        updated = complete_task(task_id)

        if updated == 0:

            return jsonify({
                "error": "Task not found."
            }), 404


        return jsonify({
            "message": "Task completed successfully."
        })


    except Exception as e:

        print("Complete task error:", e)

        return jsonify({
            "error": "Unable to complete task."
        }), 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )