import json
import boto3

translate = boto3.client('translate')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        source_lang = body['source_language']
        target_lang = body['target_language']
        text = body['text']
        
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'original_text': text,
                'translated_text': response['TranslatedText'],
                'source_language': source_lang,
                'target_language': target_lang
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }