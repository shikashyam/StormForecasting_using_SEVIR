from transformers import RobertaTokenizer, RobertaForTokenClassification
import torch

def get_model(model):
  """Loads model from Hugginface model hub"""
  try:
    model = RobertaForTokenClassification.from_pretrained(model)
    model.save_pretrained('./model')
  except Exception as e:
    raise(e)

def get_tokenizer(tokenizer):
  """Loads tokenizer from Hugginface model hub"""
  try:
    tokenizer = RobertaTokenizer.from_pretrained(tokenizer)
    tokenizer.save_pretrained('./model')
  except Exception as e:
    raise(e)

get_model('Jean-Baptiste/roberta-large-ner-english')
get_tokenizer('Jean-Baptiste/roberta-large-ner-english')