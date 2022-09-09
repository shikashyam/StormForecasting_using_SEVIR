import json
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def serverless_pipeline(model_path='./model'):
    """Initializes the model and tokenzier and returns a predict function that ca be used as pipeline"""
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    def predict(text):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        batch = tokenizer(text, truncation=True, padding="longest", return_tensors="pt").to(device)
        translated = model.generate(**batch)
        summary = tokenizer.batch_decode(translated, skip_special_tokens=True)
        return summary
    return predict

# initializes the pipeline
summarization_pipeline = serverless_pipeline()

def handler(event,context):
    try:
        # loads the incoming event into a dictonary
        body = json.loads(event['body'])
        # uses the pipeline to predict the answer
        summary = summarization_pipeline(text=body['text'])
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True

            },
            "body": json.dumps({'summary': summary})
        }
    except Exception as e:
        print(repr(e))
        return {
            "statusCode": 500,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({"error": repr(e)})
        }