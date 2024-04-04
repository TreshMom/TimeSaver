from transformers import pipeline
import random
from model.data.data_ru_to_eng import ru_bart
from model.train import predict
from template import templates, sorry

moods = [
    'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 'confusion', 'curiosity',
    'desire', 'disappointment', 'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear', 
    'gratitude', 'grief', 'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization', 
    'relief', 'remorse', 'sadness', 'surprise', 'neutral'
]

token = 'Я ненавижу!'

def generate_template(token):
    model = pipeline(model=ru_bart)
    mood = (model(token))[0]['label']
    if mood in templates:
        return (random.choice(templates[mood]) + " " + random.choice(sorry))
    else:
        return "Я не понимаю твоего настроения. Я сейчас занят, но обязательно напишу позже!"

answer = generate_template(token)
print(answer)
