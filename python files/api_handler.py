import json
import boto3

translate = boto3.client('translate')

def lambda_handler(event, context):
    print("API Translation function called")
    
    try:
        # Parse the request body from the event
        if 'body' in event and event['body']:
            body = json.loads(event['body'])
        else:
            body = event
        
        # Extract translation parameters
        source_lang = body['source_language']
        target_lang = body['target_language']
        text = body['text']
        
        # Call AWS Translate
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        
        translated_text = response['TranslatedText']
        
        # Return simplified response (without the API Gateway wrapper)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'original_text': text,
                'translated_text': translated_text,
                'source_language': source_lang,
                'target_language': target_lang
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }








# import json
# import boto3

# translate = boto3.client('translate')

# def lambda_handler(event, context):
#     print("API Translation function called")
#     print(f"Received event: {json.dumps(event)}")
    
#     try:
#         # Parse the request body from the event
#         if 'body' in event and event['body']:
#             body = json.loads(event['body'])
#         else:
#             # Handle direct invocation (testing)
#             body = event
        
#         # Extract translation parameters
#         source_lang = body['source_language']
#         target_lang = body['target_language']
#         text = body['text']
        
#         print(f"Translating from {source_lang} to {target_lang}: {text[:50]}...")
        
#         # Call AWS Translate
#         response = translate.translate_text(
#             Text=text,
#             SourceLanguageCode=source_lang,
#             TargetLanguageCode=target_lang
#         )
        
#         translated_text = response['TranslatedText']
#         print(f"Translation successful: {translated_text[:50]}...")
        
#         return {
#             'statusCode': 200,
#             'headers': {
#                 'Content-Type': 'application/json',
#                 'Access-Control-Allow-Origin': '*'
#             },
#             'body': json.dumps({
#                 'original_text': text,
#                 'translated_text': translated_text,
#                 'source_language': source_lang,
#                 'target_language': target_lang
#             })
#         }
        
#     except KeyError as e:
#         error_msg = f"Missing field in request: {str(e)}"
#         print(f"Error: {error_msg}")
#         return {
#             'statusCode': 400,
#             'headers': {
#                 'Content-Type': 'application/json',
#                 'Access-Control-Allow-Origin': '*'
#             },
#             'body': json.dumps({'error': error_msg})
#         }
#     except json.JSONDecodeError as e:
#         error_msg = f"Invalid JSON format: {str(e)}"
#         print(f"Error: {error_msg}")
#         return {
#             'statusCode': 400,
#             'headers': {
#                 'Content-Type': 'application/json',
#                 'Access-Control-Allow-Origin': '*'
#             },
#             'body': json.dumps({'error': error_msg})
#         }
#     except Exception as e:
#         error_msg = f"Translation failed: {str(e)}"
#         print(f"Error: {error_msg}")
#         return {
#             'statusCode': 500,
#             'headers': {
#                 'Content-Type': 'application/json',
#                 'Access-Control-Allow-Origin': '*'
#             },
#             'body': json.dumps({'error': error_msg})
#         }







# import json
# import boto3

# translate = boto3.client('translate')

# def lambda_handler(event, context):
#     print("API Translation function called")
    
#     try:
#         # Parse the JSON body from the HTTP request
#         body = json.loads(event['body'])
#         source_lang = body['source_language']
#         target_lang = body['target_language']
#         text = body['text']
        
#         print(f"Translating from {source_lang} to {target_lang}: {text[:50]}...")
        
#         # Call AWS Translate
#         response = translate.translate_text(
#             Text=text,
#             SourceLanguageCode=source_lang,
#             TargetLanguageCode=target_lang
#         )
        
#         translated_text = response['TranslatedText']
#         print(f"Translation successful: {translated_text[:50]}...")
        
#         return {
#             'statusCode': 200,
#             'headers': {
#                 'Content-Type': 'application/json',
#                 'Access-Control-Allow-Origin': '*'
#             },
#             'body': json.dumps({
#                 'original_text': text,
#                 'translated_text': translated_text,
#                 'source_language': source_lang,
#                 'target_language': target_lang
#             })
#         }
        
#     except KeyError as e:
#         error_msg = f"Missing field in request: {str(e)}"
#         print(f"Error: {error_msg}")
#         return {
#             'statusCode': 400,
#             'headers': {'Access-Control-Allow-Origin': '*'},
#             'body': json.dumps({'error': error_msg})
#         }
#     except Exception as e:
#         error_msg = f"Translation failed: {str(e)}"
#         print(f"Error: {error_msg}")
#         return {
#             'statusCode': 500,
#             'headers': {'Access-Control-Allow-Origin': '*'},
#             'body': json.dumps({'error': error_msg})
#         }






# import json
# import boto3

# translate = boto3.client('translate')

# def lambda_handler(event, context):
#     # Parse the JSON body from the HTTP request
#     try:
#         body = json.loads(event['body'])
#         source_lang = body['source_language']
#         target_lang = body['target_language']
#         text = body['text']
#     except (KeyError, json.JSONDecodeError) as e:
#         return {
#             'statusCode': 400,
#             'body': json.dumps({'error': 'Invalid JSON format. Required fields: source_language, target_language, text'})
#         }

#     # Call AWS Translate
#     try:
#         response = translate.translate_text(
#             Text=text,
#             SourceLanguageCode=source_lang,
#             TargetLanguageCode=target_lang
#         )
#         translated_text = response['TranslatedText']
        
#         return {
#             'statusCode': 200,
#             'headers': {'Content-Type': 'application/json'},
#             'body': json.dumps({
#                 'original_text': text,
#                 'translated_text': translated_text,
#                 'source_language': source_lang,
#                 'target_language': target_lang
#             })
#         }
#     except Exception as e:
#         return {
#             'statusCode': 500,
#             'body': json.dumps({'error': str(e)})
#         }