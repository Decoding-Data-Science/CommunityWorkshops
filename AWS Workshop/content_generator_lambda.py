import json
import boto3
import botocore.config
from datetime import datetime
import requests


"""
Amazon Nova Premier v1 Model Format
    
{
    "modelId": "amazon.nova-premier-v1:0",
    "contentType": "application/json",
    "accept": "application/json",
    "body": {
        "inferenceConfig": {
            "max_new_tokens": 1000
        },
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "text": "this is where you place your input text"
            }
            ]
        }
        ]
    }
}
"""


"""
Content request to Amazon Bedrock
"""
def generate_content(topic:str) -> str:
    
    ## Get the quote to add in the prompt
    quote = get_inspiration_quote()
    print(f"Quote: {quote}")
    
    prompt = f"""Generate a blog post on the topic {topic} in 200 words
        Start with this inspirational quote: {quote}
    """
    
    body = {
        "inferenceConfig": {
            "max_new_tokens": 1000
        },
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    try:
        bedrock = boto3.client(
            service_name = 'bedrock-runtime',
            region_name = 'us-east-1',
            config = botocore.config.Config(
                connect_timeout = 10,
                read_timeout = 10,
                retries = {
                    'max_attempts': 10,
                    'mode': 'standard'
                }
            )
        )
        
        response = bedrock.invoke_model(
            modelId = 'us.amazon.nova-premier-v1:0',
            contentType  = 'application/json',
            accept = 'application/json',
            body = json.dumps(body)
        )
        
        response_content = response.get('body').read()
        print(response_content)
        response_json = json.loads(response_content)
        blog_content = response_json['output']['message']['content'][0]['text']
        return blog_content
        
        
    except Exception as e:
        print(f"Error: {e}")
        raise e
    

"""
Upload content to S3
"""
def upload_to_s3(bucket_name, file_name, blog_content):
    
    s3 = boto3.client('s3')
    
    try:
        s3.put_object(
            Bucket = bucket_name,
            Key = file_name,
            Body = blog_content
        )
        print("Blog uploaded to S3 successfully !!")
        print(f"File uploaded to {bucket_name}/{file_name}")
    except Exception as e:
        print(f"Error uploading to s3: {e}")

    

"""
Main Lambda Function
"""
def lambda_handler(event, context):
    
    print(f"Received event: {event}")
    print(f"Received context: {context}")
    
    # Parse the body if it comes from API Gateway
    if 'body' in event and event['body']:
        body = json.loads(event['body'])
        topic = body['topic']
    else:
        # Direct Lambda invocation
        topic = event['topic']
        
    generated_blog = generate_content(topic=topic)
    
    if generated_blog:
        current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        file_name = f'blogs/{current_time}.txt'
        upload_to_s3(bucket_name="YOUR_BUCKET_NAE", file_name=file_name, blog_content=generated_blog)
        
        return {
            'statusCode': 200,
            'headers': {
                  'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'content': generated_blog,
                'message': 'Blog generated successfully!!',
                'topic': topic,
                'file_name': file_name,
                'timestamp': current_time
            })
        }
        
    else:
       return {
            'statusCode': 500,
            'headers': {
                  'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Blog generation failed!!'
            })
        }
        
        
"""
Simple function to get a quote using requests library (requires Lambda Layer)
"""
def get_inspiration_quote():
    try:
        response = requests.get('https://dummyjson.com/quotes/random', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('quote', 'Stay inspired!')
        else:
            return 'Stay inspired!'
    except:
        return 'Stay inspired!'