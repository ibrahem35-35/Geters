from flask import Flask
import requests
import random
import base64
import os

app = Flask(__name__)

# =========================
# GitHub Settings
# =========================

GITHUB_TOKEN = os.getenv("tok")

GITHUB_USERNAME = "ibrahem35-35"

# أسماء الـ Repositories
REPO_MAIN = "O.D.H."
REPO_2 = "adm"
REPO_3 = "taq"

BRANCH = "main"
FILE_PATH = "random.txt"


# =========================
# Update GitHub File
# =========================

def update_github_file(repo_name):
    # التأكد من وجود التوكن
    if not GITHUB_TOKEN:
        return "GitHub token is not configured.", 500

    # توليد رقم عشوائي
    number = random.randint(1, 100000)

    # GitHub API URL
    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_USERNAME}/{repo_name}/contents/{FILE_PATH}"
    )

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # =========================
    # الحصول على SHA للملف
    # =========================

    try:
        response = requests.get(
            url,
            headers=headers,
            params={"ref": BRANCH},
            timeout=15
        )
    except requests.RequestException as e:
        return f"GitHub GET Connection Error: {str(e)}", 500

    sha = None

    if response.status_code == 200:
        try:
            sha = response.json()["sha"]
        except (KeyError, ValueError):
            return "GitHub GET Error: Invalid response.", 500

    elif response.status_code != 404:
        return f"GitHub GET Error: {response.text}", 500

    # =========================
    # تحويل الرقم إلى Base64
    # =========================

    content = base64.b64encode(
        str(number).encode("utf-8")
    ).decode("utf-8")

    # =========================
    # بيانات التعديل / الإنشاء
    # =========================

    data = {
        "message": f"Update random.txt: {number}",
        "content": content,
        "branch": BRANCH
    }

    # لو الملف موجود لازم SHA
    if sha:
        data["sha"] = sha

    # =========================
    # إنشاء أو تعديل الملف
    # =========================

    try:
        response = requests.put(
            url,
            headers=headers,
            json=data,
            timeout=15
        )
    except requests.RequestException as e:
        return f"GitHub PUT Connection Error: {str(e)}", 500

    if response.status_code not in [200, 201]:
        return f"GitHub PUT Error: {response.text}", 500

    return f"Done! Random number: {number}", 200


# =========================
# Routes
# =========================

@app.route("/")
def home():
    return update_github_file(REPO_MAIN)


@app.route("/2")
def homee():
    return update_github_file(REPO_2)


@app.route("/3")
def homeee():
    return update_github_file(REPO_3)


# =========================
# Run Server
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
