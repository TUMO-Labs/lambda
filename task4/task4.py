import json

def lambda_handler(event, context):

    params = event.get("queryStringParameters") or {}

    # 1. Get values
    a = params.get("a")
    b = params.get("b")
    operation = params.get("operation")

    # 2. Validate input
    if a is None or b is None or operation is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing parameters"})
        }

    # 3. Convert to numbers
    try:
        a = float(a)
        b = float(b)
    except:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "a and b must be numbers"})
        }

    # 4. Do calculation
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Cannot divide by zero"})
            }
        result = a / b
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid operation"})
        }

    # 5. Response
    response = {
        "a": a,
        "b": b,
        "operation": operation,
        "result": result
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }
