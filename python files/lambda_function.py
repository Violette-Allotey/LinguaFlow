import json
import boto3
from botocore.exceptions import ClientError

# Initialize AWS clients outside the handler for efficiency
s3 = boto3.client('s3')
translate = boto3.client('translate')

def lambda_handler(event, context):
    """
    This function is triggered by an S3 event. It reads a JSON file from the
    request bucket, translates its 'text' field, and saves the result to the
    response bucket.
    """
    print("Received event: " + json.dumps(event))

    # 1. Get the bucket and file name from the S3 event trigger
    try:
        record = event['Records'][0]['s3']
        source_bucket = record['bucket']['name']
        source_key = record['object']['key'] # File name

        print(f"Processing file: {source_key} from bucket: {source_bucket}")

    except (KeyError, IndexError) as e:
        print(f"Error parsing S3 event: {e}")
        return {'statusCode': 400, 'body': json.dumps('Malformed S3 event')}

    # 2. Read the JSON file from S3
    try:
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        file_content = response['Body'].read().decode('utf-8')
        data_to_translate = json.loads(file_content)
        print("Original data:", data_to_translate)

    except ClientError as e:
        print(f"Error reading from S3: {e}")
        return {'statusCode': 500, 'body': json.dumps('Failed to read source file')}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {'statusCode': 400, 'body': json.dumps('Source file is not valid JSON')}

    # 3. Extract translation parameters and text from the JSON
    # The input JSON should look like: 
    # {"source_language": "en", "target_language": "es", "text": "Hello, world!"}
    try:
        source_lang = data_to_translate['source_language'] # e.g., 'en'
        target_lang = data_to_translate['target_language'] # e.g., 'es'
        original_text = data_to_translate['text'] # e.g., 'Hello, world!'

    except KeyError as e:
        print(f"Missing key in JSON: {e}")
        return {'statusCode': 400, 'body': json.dumps('Source JSON missing required fields')}

    # 4. Call AWS Translate
    try:
        translation_result = translate.translate_text(
            Text=original_text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        translated_text = translation_result['TranslatedText']
        print(f"Translated Text: {translated_text}")

    except ClientError as e:
        print(f"Error calling Translate: {e}")
        return {'statusCode': 500, 'body': json.dumps('Translation service failed')}

    # 5. Create the output JSON structure
    output_data = {
        "original_text": original_text,
        "translated_text": translated_text,
        "source_language": source_lang,
        "target_language": target_lang
    }

    # 6. Upload the translated result to the response bucket
    destination_bucket = 'response-bucket-violette' # REPLACE WITH YOUR BUCKET NAME!
    # destination_key = f'translated-{source_key}'
    destination_key = f"{get_language_folder(target_lang)}/translated-{source_key}"

    try:
        s3.put_object(
            Bucket=destination_bucket,
            Key=destination_key,
            Body=json.dumps(output_data, ensure_ascii=False) # ensure_ascii=False allows non-ASCII characters
        )
        print(f"Successfully uploaded translated file to: s3://{destination_bucket}/{destination_key}")

    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return {'statusCode': 500, 'body': json.dumps('Failed to upload result')}

    return {
        'statusCode': 200,
        'body': json.dumps('Translation completed successfully!')
    }

# Add this after the imports
def get_language_folder(language_code):
    """Maps language codes to folder names"""
    language_map = {
        'en': 'english',
        'es': 'spanish', 
        'fr': 'french',
        'de': 'german',
        'it': 'italian'
    }
    return language_map.get(language_code, 'other')

