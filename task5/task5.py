import json
import random

def lambda_handler(event, context):

    params = event.get("queryStringParameters") or {}
    min_val = params.get("min", 1)
    max_val = params.get("max", 100)

    try:
        min_val = int(min_val)
        max_val = int(max_val)
    except:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "min and max must be integers"})
        }

    if min_val > max_val:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "min cannot be greater than max"})
        }

    random_number = random.randint(min_val, max_val)

    response = {
        "min": min_val,
        "max": max_val,
        "randomNumber": random_number
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }
