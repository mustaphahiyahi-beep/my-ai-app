def ask_ai(question):
    try:
        url = "https://api.deepseek.com/v1/chat/completions"

        headers = {
            "Authorization": "Bearer YOUR_API_KEY",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a cybersecurity expert"},
                {"role": "user", "content": question}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        return response.json()  # 👈 مؤقتاً لعرض الخطأ

    except Exception as e:
        return str(e)
