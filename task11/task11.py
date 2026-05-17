import json
import boto3

s3 = boto3.client("s3")
BUCKET_NAME = "task9-tumo"

def lambda_handler(event, context):

    filename = event.get("pathParameters", {}).get("filename")

    if not filename:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "filename is required"})
        }

    try:
        s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=f"messages/{filename}"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "message": "File deleted",
                "filename": filename
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
