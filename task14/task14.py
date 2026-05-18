import json
import boto3

s3 = boto3.client("s3")

BUCKET_NAME = "task9-tumo"

def lambda_handler(event, context):

    print(event)
    method = event.get("requestContext", {}).get("http", {}).get("method")
    path_params = event.get("pathParameters") or {}
    city_from_path = path_params.get("city")

    if method == "POST":
        body = event.get("body")

        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "Missing body"
                })
            }
        data = json.loads(body)
        city = data.get("city")
        temperature = data.get("temperature")
        humidity = data.get("humidity")

        if city is None or temperature is None or humidity is None:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "city, temperature, humidity required"
                })
            }

        if temperature >= 30:
            status = "Hot"

        elif temperature >= 20:
            status = "Warm"

        elif temperature >= 10:
            status = "Cool"

        else:
            status = "Cold"

        weather_data = {
            "city": city,
            "temperature": temperature,
            "humidity": humidity,
            "status": status
        }

        key = f"weather/{city.lower()}.json"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(weather_data)
        )

        return {
            "statusCode": 200,
            "body": json.dumps(weather_data)
        }

    if method == "GET":

        if not city_from_path:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "city required"
                })
            }
        key = f"weather/{city_from_path.lower()}.json"

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
                "body": json.dumps({
                    "error": "Weather data not found"
                })
            }

    return {
        "statusCode": 405,
        "body": json.dumps({
            "error": "Method not allowed"
        })
    }
