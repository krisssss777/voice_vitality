import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# 1. 貼上你的 API Key
API_KEY = "AIzaSyCGSGEivNIumAqm_d3H2IsDTnPDW7WjpS0"
genai.configure(api_key=API_KEY)

# 2. 定義「聲命力教練」的專家魂
instruction = """
你現在是『聲命力 Voice Vitality』品牌的專業演講與簡報教練。
你的任務是協助那些不敢開口或缺乏經驗的人。
你需要：
1. 提供具體的演講開場、結構建議。
2. 協助將中文稿優化為地道、專業的英文演講稿。
3. 語氣要溫暖、鼓勵、專業。
4. 所有的回答都要圍繞在「聲音、演講、表達、溝通、簡報」這五大主題。
"""

# 自動尋找可用模型並注入指令
available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
selected_model = available_models[0] if available_models else 'gemini-1.5-flash'
model = genai.GenerativeModel(selected_model, system_instruction=instruction)

app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        user_message = data.get("message")
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"教練連線中，請稍後：{str(e)}"})

if __name__ == '__main__':
    # 這是雲端部署的關鍵：自動偵測伺服器提供的 Port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
