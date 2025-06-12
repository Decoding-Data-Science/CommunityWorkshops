from content_generator_lambda import lambda_handler

def main():
    # Mock event and context
    event = {
        "topic" : "AI in health industry"
    }
    context = None
    
    result = lambda_handler(event, context)
    print(result)
    
if __name__ == "__main__":
     main()