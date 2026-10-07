from flask import Flask, request, render_template_string
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

REPO_MAIN = "O.D.H."
REPO_2 = "adm"
REPO_3 = "taq"

BRANCH = "main"
FILE_PATH = "random.txt"


# =========================
# Update GitHub File
# =========================

def update_github_file(repo_name):
    if not GITHUB_TOKEN:
        return "GitHub token is not configured.", 500

    number = random.randint(1, 100000)

    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_USERNAME}/{repo_name}/contents/{FILE_PATH}"
    )

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

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

    content = base64.b64encode(
        str(number).encode("utf-8")
    ).decode("utf-8")

    data = {
        "message": f"Update random.txt: {number}",
        "content": content,
        "branch": BRANCH
    }

    if sha:
        data["sha"] = sha

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


@app.route("/get-img")
def get_images():
    # استخراج الـ Parameters من الطلب
    target_url = request.args.get("q")
    auth_token = request.args.get("auth")

    if not target_url:
        return "Missing 'q' parameter.", 400

    # تجهيز الهيدرز لو اتبعت توكن
    headers = {}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    try:
        # طلب الـ API الخارجي
        res = requests.get(target_url, headers=headers, timeout=15)
        if res.status_code != 200:
            return f"API Error ({res.status_code}): {res.text}", res.status_code

        data = res.json()
    except requests.RequestException as e:
        return f"Request Failed: {str(e)}", 500
    except ValueError:
        return "Invalid JSON response from target API.", 500

    # استخراج مصفوفة الأسئلة والروابط
    questions = data.get("questions", [])
    img_tags = []

    BASE_IMG_URL = "https://api.bassthalk.com/"

    for item in questions:
        pic_path = item.get("picture")
        if pic_path:
            # دمج الرابط الأساسي مع المسار
            full_url = f"{BASE_IMG_URL}{pic_path}"
            img_tags.append(f'<img src="{full_url}" alt="Question Image"><br>')

    # تجميع الـ HTML المرجّع
    html_content = "\n".join(img_tags) if img_tags else "<p>No images found.</p>"

    return render_template_string(html_content), 200


# =========================
# Run Server
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
