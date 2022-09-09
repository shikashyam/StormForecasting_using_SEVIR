import json
import torch
from transformers import RobertaForTokenClassification, RobertaTokenizer,pipeline

def serverless_pipeline(model_path='./model'):
    """Initializes the model and tokenzier and returns a predict function that ca be used as pipeline"""
    tokenizer = RobertaTokenizer.from_pretrained(model_path)
    model = RobertaForTokenClassification.from_pretrained(model_path)
    def predict(text):
        #device = "cuda" if torch.cuda.is_available() else "cpu"
        # batch = tokenizer(text, truncation=True, padding="longest", return_tensors="pt").to(device)
        # translated = model.generate(**batch)
        # summary = tokenizer.batch_decode(translated, skip_special_tokens=True)
        NER_Model = pipeline("ner", model=model, tokenizer=tokenizer)
        NER_Results=NER_Model(text)
        mylist=[]
        for item in NER_Results:
            #print(item['entity'] + ':' + item['word'])
            data=(item['entity'],item['word'])
            mylist.append(data)

        return dict(mylist)
    return predict

# initializes the pipeline
NER_pipeline = serverless_pipeline()

def handler(event,context):
    try:
        # loads the incoming event into a dictonary
        body = json.loads(event['body'])
        # uses the pipeline to predict the answer
        NER_dict = NER_pipeline(text=body['text'])
        json_object = json.dumps(NER_dict, indent = 4) 
        print(json_object)
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True

            },
            "body": json_object
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