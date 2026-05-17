import json

def lambda_handler(event, context):

    body = event.get("body")

    if body is None:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "Missing body"
            })
        }

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "Invalid JSON"
            })
        }

    name = data.get("name")
    age = data.get("age")
    course = data.get("course")

    if not name or not age or not course:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "name, age and course are required"
            })
        }

    message = f"Student {name} registered for {course}"

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "success": True,
            "message": message
        })
    }
