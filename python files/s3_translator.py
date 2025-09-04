import json
import boto3
import urllib.parse

s3 = boto3.client('s3')
translate = boto3.client('translate')

def get_language_folder(language_code):
    """Map language codes to folder names"""
    language_map = {
        'en': 'english',
        'es': 'spanish', 
        'fr': 'french',
        'de': 'german',
        'it': 'italian',
        'pt': 'portuguese',
        'zh': 'chinese',
        'ja': 'japanese',
        'ko': 'korean',
        'ar': 'arabic'
    }
    return language_map.get(language_code, 'other')

def lambda_handler(event, context):
    print("Lambda function started - Processing translation request")
    
    try:
        # Get bucket and file info from S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
        print(f"Processing file: {key} from bucket: {bucket}")
        
        # Get the file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        data = json.loads(file_content)
        
        print(f"Original data: {data}")
        
        # Extract translation parameters
        source_lang = data['source_language']
        target_lang = data['target_language']
        original_text = data['text']
        
        # Call AWS Translate
        translation_result = translate.translate_text(
            Text=original_text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        
        translated_text = translation_result['TranslatedText']
        print(f"Translated Text: {translated_text}")
        
        # Create the output JSON structure
        output_data = {
            "original_text": original_text,
            "translated_text": translated_text,
            "source_language": source_lang,
            "target_language": target_lang
        }
        
        # Create language-specific folder path
        language_folder = get_language_folder(target_lang)
        new_key = f"{language_folder}/translated-{key}"
        
        # Upload to response bucket with organized structure
        s3.put_object(
            Bucket='response-bucket-violette',
            Key=new_key,
            Body=json.dumps(output_data, ensure_ascii=False),
            ContentType='application/json'
        )
        
        print(f"Successfully uploaded to: s3://response-bucket-violette/{new_key}")
        return {'statusCode': 200, 'body': 'Translation completed successfully!'}
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': f"Error: {str(e)}"}






# import json
# import boto3
# import urllib.parse

# s3 = boto3.client('s3')
# translate = boto3.client('translate')

# def get_language_folder(language_code):
#     language_map = {'en': 'english', 'es': 'spanish', 'fr': 'french', 'de': 'german', 'it': 'italian'}
#     return language_map.get(language_code, 'other')

# def lambda_handler(event, context):
#     try:
#         bucket = event['Records'][0]['s3']['bucket']['name']
#         key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
#         # Get the file from S3
#         response = s3.get_object(Bucket=bucket, Key=key)
#         file_content = response['Body'].read().decode('utf-8')
#         data = json.loads(file_content)
        
#         # Translate
#         translation = translate.translate_text(
#             Text=data['text'],
#             SourceLanguageCode=data['source_language'],
#             TargetLanguageCode=data['target_language']
#         )
        
#         # Prepare output
#         output_data = {
#             'original_text': data['text'],
#             'translated_text': translation['TranslatedText'],
#             'source_language': data['source_language'],
#             'target_language': data['target_language']
#         }
        
#         # Save to response bucket with language folder
#         target_lang = data['target_language']
#         new_key = f"{get_language_folder(target_lang)}/translated-{key}"
        
#         s3.put_object(
#             Bucket='response-bucket-violette',
#             Key=new_key,
#             Body=json.dumps(output_data, ensure_ascii=False),
#             ContentType='application/json'
#         )
        
#         return {'statusCode': 200, 'body': 'Success'}
        
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return {'statusCode': 500, 'body': f"Error: {str(e)}"}