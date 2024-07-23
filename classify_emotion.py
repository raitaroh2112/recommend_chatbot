from transformers import AutoTokenizer, AutoModelForSequenceClassification, LukeConfig
import torch

# モデルとトークナイザのロード
tokenizer = AutoTokenizer.from_pretrained(
    "Mizuiro-sakura/luke-japanese-large-sentiment-analysis-wrime")
config = LukeConfig.from_pretrained(
    'Mizuiro-sakura/luke-japanese-large-sentiment-analysis-wrime', output_hidden_states=True)
model = AutoModelForSequenceClassification.from_pretrained(
    'Mizuiro-sakura/luke-japanese-large-sentiment-analysis-wrime', config=config)

emotion_labels = ['joy', 'sadness', 'anticipation', 'surprise',
                  'anger', 'fear', 'disgust', 'trust']


def classify_emotion(text):
    max_seq_length = 512
    token = tokenizer(text, truncation=True, max_length=max_seq_length,
                      padding="max_length", return_tensors="pt")
    output = model(**token)
    max_index = torch.argmax(output.logits, dim=1).item()
    return emotion_labels[max_index]


if __name__ == "__main__":
    text = '不安でたまらない、どうしよう'
    emotion = classify_emotion(text)
    print(emotion)
