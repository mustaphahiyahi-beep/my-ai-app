def ask_ai(question):
    return "AI غير مفعل حالياً"
    try:
        url = "https://api.deepseek.com/v1/chat/completions"

        headers = {
            "Authorization": "sk-72885bff6559440286c83919058fbcc6",
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
