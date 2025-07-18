import os
from flask import Flask, render_template, request
from docx import Document
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/", methods=["GET", "POST"])
def index():
    resume_text = ""
    job_desc = ""
    generated_resume = ""
    cover_letter = ""

    if request.method == "POST":
        job_desc = request.form.get("job_description", "")
        resume_file = request.files.get("resume_file")

        if resume_file:
            if resume_file.filename.endswith(".docx"):
                document = Document(resume_file)
                resume_text = "\n".join(
                    [para.text for para in document.paragraphs])
            else:
                resume_text = resume_file.read().decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role":
                "system",
                "content":
                "You are a helpful assistant that rewrites resumes."
            }, {
                "role":
                "user",
                "content":
                f"Here's a resume:\n{resume_text}\n\nHere's the job description:\n{job_desc}\n\nTailor the resume to match."
            }])

        generated_resume = response.choices[0].message.content

    return render_template("index.html",
                           resume_text=resume_text,
                           job_desc=job_desc,
                           generated_resume=generated_resume,
                           cover_letter=cover_letter)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
