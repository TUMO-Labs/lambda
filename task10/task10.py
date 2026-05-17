import json
import boto3

s3 = boto3.client("s3")
BUCKET_NAME = "task9-tumo"

def lambda_handler(event, context):

    filename = event.get("pathParameters", {}).get("filename")

    if not filename:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "filename is required"})
        }

    key = f"messages/{filename}"

    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        content = obj["Body"].read().decode("utf-8")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "filename": filename,
                "content": json.loads(content)
            })
        }

    except s3.exceptions.NoSuchKey:
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "file not found"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }
