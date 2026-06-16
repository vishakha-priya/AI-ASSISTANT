from flask import Flask,flash,render_template,request,jsonify
import os
from dotenv import load_dotenv
from groq import Groq
app=Flask(__name__)
load_dotenv()
api_key=os.getenv("GROQ_API_KEY")

client=Groq(api_key=api_key)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form["question"]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    answer = response.choices[0].message.content

    return jsonify({
        "response": answer
    })
@app.route("/summarize", methods=["POST"])
def summarize():
    email_text = request.form.get("email")

    prompt = f"""
    Summarize the following email in 2-3 sentences:

    {email_text}
    """

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {
                "role": "system",
                "content": "Act like an expert email assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=512
    )

    summary = response.choices[0].message.content.strip()

    return jsonify({
        "response": summary
    }), 200
if __name__=="__main__":
    app.run(debug=True) #if this file is imported as module in another file and do not run 