from pprint import pprint
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
from pyppeteer import launch
import os, asyncio, requests, bs4

FOLDERS = {
    'template_folder': os.getcwd(),
    'static_folder': os.getcwd()
}
MOODLE_SESSION = 'ka93d6q1oltvkt2vnvjqpgct7v'
app = Flask(__name__, **FOLDERS)
cors = CORS(app)


@app.route('/')
async def landing_page():
    return render_template('index.html')

@app.route('/comp-sci')
async def comp_sci():
    return render_template('Computer Science Files/misc.html')

@app.route("/flask/khub-login", methods=['GET'])
async def get_session():
    browser = await launch(headless=False, args=['--window-position=9999,9999'],
                           handleSIGINT=False,
                           handleSIGTERM=False,
                           handleSIGHUP=False)
    page = await browser.newPage()
    elements = dict(
        button='button[class^="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b"]',
        input_field='input[class^="whsOnd zHQkBf"]',)
    await page.goto('https://khub.cvc.pshs.edu.ph/login/index.php')
    soup = BeautifulSoup(await page.content(), 'lxml')
    await page.goto(soup.find('a', {"class": 'btn btn-secondary'})['href'])
    await asyncio.sleep(1)
    for i in ['2020caaborja@cvc.pshs.edu.ph', 'NyanFart3303']:
        await page.type(elements['input_field'], i)
        await page.click(elements['button'])
        await asyncio.sleep(3)
    await asyncio.sleep(1)
    cookies = (lambda cookies: {i: cookies[i] for i in cookies if i in ['value', 'name']})((await page.cookies())[0])
    await browser.close()
    print(dict(cookie=cookies))
    return dict(cookie=cookies), 200


async def parse_advisers(advisers):
    return [{"profile": i['href'],
             "name": i['title'],
             "pfp": i.find('img')['src']}for i in advisers]

async def parse_description(description: bs4.Tag):
    if description is None:
        return "No Description was provided"
    for i, j in enumerate(description.contents):
        if not isinstance(j, bs4.NavigableString) and j.find_all('a'):
            j = j.get_text()
        description.contents[i] = j
    return '\n'.join(str(i) for i in description.contents)
    

@app.route('/flask/khub', methods=['GET', 'POST'])
async def khub_home_page():
    with requests.session() as session:
        session.cookies.set(name='MoodleSession', value=MOODLE_SESSION)
        home_main = BeautifulSoup(session.get('https://khub.cvc.pshs.edu.ph/').text, 'lxml').select_one('div[role="main"]')
        try:
            home_courses = home_main.select_one('div[id="frontpage-course-list"]').select('div[class="card"]')
            home_courses = [{'link': i.find_all('a')[0]['href'],
                            'title': i.find('h4').find('a').text,
                            'img': i.find_all('a')[0].find('img')['src'],
                            'description': await parse_description(i.select_one('div[class="no-overflow"]')),
                            'advisers': await parse_advisers(i.select('a[class="contact"]'))} for i in home_courses]
            return jsonify(home=home_courses), 200
        except Exception as e:
            return jsonify(Messages=str(e)), 500

async def khub_autolog():
    global MOODLE_SESSION
    x = requests.get('http://localhost:5000/flask/khub')
    if x.status_code == 500:
        MOODLE_SESSION = requests.get('http://localhost:5000/flask/khub-login').json()['cookie']['value']
        x = requests.get('http://localhost:5000/flask/khub')
    return x.json()
        
@app.route('/khub')
async def PSHSKhub():
    return render_template('khub.html', info=await khub_autolog())

@app.route('/wolfram-alpha')
async def WolframAlpha():
    return render_template('wolfram-alpha.html')

@app.route('/post-test', methods=['POST'])
async def post_test():
    print(request.json)
    return {0: 1}, 200

if __name__ == '__main__':
    app.run(debug=True)