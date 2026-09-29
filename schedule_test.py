from schedule_manager import (
    add_subject,
    get_subjects,
    add_task,
    get_pending_tasks
)


subject_id = add_subject(
    "Python",
    "2026-10-23",
    2
)

print("Subject ID:", subject_id)


task_id = add_task(
    subject_id,
    "Python Loops",
    "2026-10-01",
    60
)

print("Task ID:", task_id)


print("\nSubjects:")

for subject in get_subjects():
    print(subject)


print("\nPending Tasks:")

for task in get_pending_tasks():
    print(task)