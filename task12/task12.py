import json
import boto3

s3 = boto3.client("s3")
BUCKET_NAME = "task9-tumo"

def lambda_handler(event, context):

    method = event.get("requestContext", {}).get("http", {}).get("method")
    path_params = event.get("pathParameters") or {}
    note_id = path_params.get("noteId")

    if method == "POST":

        body = event.get("body")

        if not body:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing body"})}

        data = json.loads(body)
        note_id = data.get("noteId")
        content = data.get("content")

        if not note_id or not content:
            return {"statusCode": 400, "body": json.dumps({"error": "noteId and content required"})}

        key = f"notes/{note_id}.json"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps({"content": content})
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"success": True, "message": "Note saved", "noteId": note_id})
        }

    if method == "GET":

        if not note_id:
            return {"statusCode": 400, "body": json.dumps({"error": "noteId required"})}

        key = f"notes/{note_id}.json"

        try:
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
            data = json.loads(obj["Body"].read().decode("utf-8"))

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "noteId": note_id,
                    "content": data.get("content")
                })
            }

        except Exception:
            return {"statusCode": 404, "body": json.dumps({"error": "Note not found"})}

    if method == "DELETE":

        if not note_id:
            return {"statusCode": 400, "body": json.dumps({"error": "noteId required"})}

        key = f"notes/{note_id}.json"

        try:
            s3.delete_object(Bucket=BUCKET_NAME, Key=key)

            return {
                "statusCode": 200,
                "body": json.dumps({"success": True, "message": "Note deleted"})
            }

        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    return {"statusCode": 405, "body": json.dumps({"error": "Method not allowed"})}
