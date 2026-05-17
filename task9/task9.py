import json
import boto3

s3 = boto3.client("s3")
BUCKET_NAME = "task9-tumo"

def lambda_handler(event, context):

    body = event.get("body")

    if body is None:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Missing body"})
        }

    try:
        data = json.loads(body)
    except:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Invalid JSON"})
        }

    filename = data.get("filename")
    name = data.get("name")
    message = data.get("message")

    if not filename or not name or not message:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "filename, name and message required"})
        }

    key = f"messages/{filename}"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps({
            "name": name,
            "message": message
        })
    )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "success": True,
            "message": "Data saved to S3",
            "path": key
        })
    }
