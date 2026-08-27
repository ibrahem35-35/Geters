from flask import Flask
import requests
import random
import base64
import os

app = Flask(__name__)

# بيانات GitHub
GITHUB_TOKEN = "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"

GITHUB_USERNAME = "ibrahem35-35"
REPO_NAME = "O.D.H."
BRANCH = "main"

FILE_PATH = "random.txt"


@app.route("/")
def home():
    # توليد رقم عشوائي
    number = random.randint(1, 100000)

    # GitHub API
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # نشوف الملف موجود ولا لأ
    response = requests.get(
        url,
        headers=headers,
        params={"ref": BRANCH}
    )

    sha = None

    if response.status_code == 200:
        sha = response.json()["sha"]

    elif response.status_code != 404:
        return f"GitHub GET Error: {response.text}", 500

    # تحويل الرقم إلى Base64
    content = base64.b64encode(
        str(number).encode("utf-8")
    ).decode("utf-8")

    data = {
        "message": f"Update random.txt: {number}",
        "content": content,
        "branch": BRANCH
    }

    # لو الملف موجود لازم SHA
    if sha:
        data["sha"] = sha

    # إنشاء / تعديل الملف
    response = requests.put(
        url,
        headers=headers,
        json=data
    )

    if response.status_code not in [200, 201]:
        return f"GitHub PUT Error: {response.text}", 500

    return f"Done! Random number: {number}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
