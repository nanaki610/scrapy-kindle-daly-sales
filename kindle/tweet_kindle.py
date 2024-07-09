import csv
import json
import os
import requests
import tweepy
from dotenv import load_dotenv

load_dotenv()
# secretsで設定した値を取る
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

# 認証情報を設定
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# オブジェクト作成
client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# スクリプトファイルの絶対パスを取得
script_path = os.path.abspath(__file__)
# スクリプトファイルのディレクトリパスを取得
script_dir = os.path.dirname(script_path)
# スクリプトファイルの親ディレクトリパスを取得
parent_dir = os.path.dirname(script_dir)
# 'out.json'への絶対パスを作成。out.jsonはスクリプトファイルと同じディレクトリにある前提。
# json_file_path = os.path.join(script_dir, 'out.json')
# out.jsonへの絶対パスを作成。out.jsonは親ディレクトリにある前提。
# json_file_path = os.path.join(parent_dir, 'out.json')
csv_file_path = os.path.join(parent_dir, 'out.csv')

def create_tweet():
	# out.jsonのデータをまとめて1つの投稿でツイートする
	# with open(json_file_path, 'r', encoding='utf-8') as f:
	# 		json_data = json.load(f)
 
	# out.csvのデータをまとめて1つの投稿でツイートする
	with open(csv_file_path, 'r', encoding='utf-8') as f:
		csv_data = csv.DictReader(f)
		for index, item in enumerate(csv_data):
			# 画像を保存する
			image_url = f"{item['image']}"
			image_path = f"image_0{index+1}.jpg"
			# 画像をダウンロード
			response = requests.get(image_url)
			if response.status_code == 200:
					with open(image_path, 'wb') as file:
							file.write(response.content)
			# ダウンロードした画像をアップロード
			media = api.media_upload(filename=image_path)

			tweet_text = f"本日のkindleセール情報 ({index+1}/3)\n\n"
			tweet_text += f"{item['title']}\n {item['price']}円\n {item['url']}"
			media = api.media_upload(filename=image_path)
			# ツイートする
			print(tweet_text)
			client.create_tweet(text=tweet_text, media_ids=[media.media_id])

			# 画像を削除
			os.remove(image_path)
	# jsonファイルを削除
	os.remove(csv_file_path)

	print("ツイートしました。")