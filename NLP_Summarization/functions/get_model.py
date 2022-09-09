from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

def get_model(model):
  """Loads model from Hugginface model hub"""
  try:
    model = AutoModelForSeq2SeqLM.from_pretrained(model)
    model.save_pretrained('./model')
  except Exception as e:
    raise(e)

def get_tokenizer(tokenizer):
  """Loads tokenizer from Hugginface model hub"""
  try:
    tokenizer = AutoTokenizer.from_pretrained(tokenizer)
    tokenizer.save_pretrained('./model')
  except Exception as e:
    raise(e)

get_model('sshleifer/distilbart-cnn-12-6')
get_tokenizer('sshleifer/distilbart-cnn-12-6')