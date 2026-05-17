import json

def lambda_handler(event, context):

    params = event.get("queryStringParameters") or {}

    value = params.get("value")
    from_unit = params.get("from")
    to_unit = params.get("to")

    if value is None or from_unit is None or to_unit is None:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "value, from and to are required"
            })
        }

    try:
        value = float(value)
    except:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "value must be a number"
            })
        }

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit == to_unit:
        result = value

    elif from_unit == "celsius" and to_unit == "fahrenheit":
        result = (value * 9/5) + 32

    elif from_unit == "fahrenheit" and to_unit == "celsius":
        result = (value - 32) * 5/9

    elif from_unit == "celsius" and to_unit == "kelvin":
        result = value + 273.15

    elif from_unit == "kelvin" and to_unit == "celsius":
        result = value - 273.15

    else:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "unsupported conversion"
            })
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "value": value,
            "from": from_unit,
            "to": to_unit,
            "result": result
        })
    }
