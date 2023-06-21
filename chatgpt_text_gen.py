# ChatGPT APIを呼び出してテキストを生成するプログラム
import json
import openai
from typing import Optional

# ChatGPT APIを呼び出してテキストを生成するクラス
class ChatGPT:
    # 初期化時にはAPIキーをJSONファイルから読み込む
    def __init__(self, secret_file: str = "secret.json") -> None:
        # JSONファイルからAPIキーを読み込む
        try:
            with open(secret_file) as f:
                secrets = json.load(f)
                openai.api_key: str = secrets.get("OPENAI_API_KEY")
        except Exception as e:
            print(f"Error loading API key: {e}")
            return
        # 使用するモデルを指定
        self.model = "gpt-3.5-turbo"

    # プロンプトからテキストを生成
    def generate_text(
            self, 
            prompt: str, 
            max_tokens: Optional[int] = 100
            ) -> str:
        # messagesを作成
        messages = [{"role": "user", "content": prompt}]
        # OpenAI APIを呼び出してテキストを生成
        try:
            response = openai.ChatCompletion.create(
                model=self.model, 
                messages=messages, 
                max_tokens=max_tokens)
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""
        
    # ファイルから固定部分のプロンプトを読み込み、追加のテキストと結合してテキストを生成
    def generate_from_file(
            self, 
            filepath: str, 
            additional_text: str, 
            max_tokens: Optional[int] = 100
            ) -> str:
        # ファイルからプロンプトを読み込む
        try:
            with open(filepath, 'r', encoding="utf-8") as f:
                file_prompt = f.read()
        except Exception as e:
            print(f"Error loading file: {e}")
            return ""
        # ファイルの内容と追加のテキストを結合
        full_prompt = file_prompt + additional_text
        # 結合したプロンプトを使ってテキストを生成
        return self.generate_text(full_prompt, max_tokens)
