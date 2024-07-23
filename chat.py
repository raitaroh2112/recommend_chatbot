import random
from classify_emotion import classify_emotion
import pandas as pd
import json
import os
import datetime


def recommend_songs(user_input):
    emotion = classify_emotion(user_input)
    try:
        csv_path = 'data/song_database.csv'
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"The file {csv_path} does not exist.")

        df = pd.read_csv(csv_path, encoding='utf-8')

        if df[['感情ラベル', 'アーティスト', '曲名', '楽曲リンク']].isnull().any().any():
            raise ValueError(
                "The CSV file contains missing values in one of the required columns.")

        filtered_df = df[df['感情ラベル'] == emotion]
        if filtered_df.empty:
            raise ValueError(f"No songs found for the emotion: {emotion}")

        selected_df = filtered_df.sample(n=1)
        artist = selected_df['アーティスト'].values[0]
        title = selected_df['曲名'].values[0]
        link = selected_df['楽曲リンク'].values[0]

        song_info = [emotion, artist, title, link]
        return song_info

    except FileNotFoundError as e:
        print(e)
        return [emotion, "", "", ""]

    except ValueError as e:
        print(e)
        return [emotion, "", "", ""]

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [emotion, "", "", ""]


def load_responses(file_path='data/responses.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


responses = load_responses()


def respond_to_emotion(emotion):
    if responses is None:
        return "応答データが読み込まれていません。"

    if emotion in responses:
        return random.choice(responses[emotion])
    else:
        return '感情に対応する言葉が見つかりませんでした。'


def generate_response(user_message):
    submit_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')
    recommend_songs_info = recommend_songs(user_message)
    praise_words = respond_to_emotion(recommend_songs_info[0])

    if recommend_songs_info[1] and recommend_songs_info[2] and recommend_songs_info[3]:
        recommend_words = f'そんなあなたにおすすめの曲は{recommend_songs_info[1]}の『{recommend_songs_info[2]}』です。<br><a href="{recommend_songs_info[3]}" target="_blank">{recommend_songs_info[3]}</a>'

    else:
        recommend_words = '申し訳ありませんが、現在おすすめの曲が見つかりません。'

    response_message = f'{praise_words}<br>{recommend_words}'
    emotion = recommend_songs_info[0]

    return {'response_message': response_message, 'time': submit_time, 'emotion': emotion}


if __name__ == '__main__':
    test_message = "今日は悲しい"
    response = generate_response(test_message)
    print(response)
