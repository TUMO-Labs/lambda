import json
import boto3

s3 = boto3.client("s3")

BUCKET_NAME = "task9-tumo"

def lambda_handler(event, context):

    print(event)
    method = event.get("requestContext", {}).get("http", {}).get("method")
    path_params = event.get("pathParameters") or {}
    student_id = path_params.get("studentId")

    if method == "POST":

        body = event.get("body")

        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing body"})
            }

        data = json.loads(body)

        student_id = data.get("studentId")
        name = data.get("name")
        age = data.get("age")
        course = data.get("course")

        if not student_id or not name or not age or not course:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "studentId, name, age, and course are required"
                })
            }

        if not isinstance(age, int):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "age must be an integer"
                })
            }

        key = f"students/{student_id}.json"

        student_data = {
            "studentId": student_id,
            "name": name,
            "age": age,
            "course": course
        }

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(student_data)
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "message": "Student saved",
                "studentId": student_id
            })
        }

    if method == "GET":

        if not student_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "studentId required"})
            }

        key = f"students/{student_id}.json"

        try:

            obj = s3.get_object(
                Bucket=BUCKET_NAME,
                Key=key
            )

            data = json.loads(
                obj["Body"].read().decode("utf-8")
            )

            return {
                "statusCode": 200,
                "body": json.dumps(data)
            }

        except Exception:

            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Student not found"})
            }

    if method == "DELETE":

        if not student_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "studentId required"})
            }

        key = f"students/{student_id}.json"

        try:

            s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=key
            )

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "success": True,
                    "message": "Student deleted"
                })
            }

        except Exception as e:

            return {
                "statusCode": 500,
                "body": json.dumps({
                    "error": str(e)
                })
            }

    # =========================
    # Unsupported method
    # =========================

    return {
        "statusCode": 405,
        "body": json.dumps({
            "error": "Method not allowed"
        })
    }
