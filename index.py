from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

HOME_HTML = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8" />
    <title>首頁</title>
</head>
<body>
    <p>在網址後方輸入BV號以查看或發佈評論</p>
    <p>by b站@冰水水水수</p>   
</body>
</html>
'''

VIDEO_HTML = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8" />
    <title>{{ title }}</title>
</head>
<body>
    <h2>標題：{{ title }}</h2>
    <p>BV號：{{ bvid }}</p>
    <a href="/">返回首頁</a>
</body>
</html>
'''

@app.route('/')
def home():
    return HOME_HTML

@app.route('/<bvid>')
def show_video(bvid):
    if not bvid.startswith('BV'):
        return '無效的BV號', 400
    api_url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
    try:
        resp = requests.get(api_url, timeout=5)
        data = resp.json()
        title = data.get('data', {}).get('title', '未找到該視頻標題')
    except Exception:
        title = '獲取標題時出錯'
    return render_template_string(VIDEO_HTML, title=title, bvid=bvid)

if __name__ == '__main__':
    app.run(debug=True)
