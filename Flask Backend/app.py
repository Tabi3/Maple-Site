from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from flask_cors import CORS
from bs4 import BeautifulSoup
from pyppeteer import launch
import os, asyncio, requests, bs4, aiohttp

FOLDERS = {
    'template_folder': os.getcwd(),
    'static_folder': os.getcwd()
}
MOODLE_SESSION = 'ka93d6q1oltvkt2vnvjqpgct7v'
app = Flask(__name__, **FOLDERS)
cors = CORS(app)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class PSHS_KHUB_SCRAPER():
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session, self._rkwargs = session, {"allow_redirects": False}

    async def selector(self, *args, **kwargs) -> BeautifulSoup:
        return BeautifulSoup(*args, **kwargs)

    async def fetchSite(self, url: str) -> str | None:
        async with self.session.get(url, **self._rkwargs) as page:
            return await page.text()
    
    async def parse_a(self, i) -> list[dict[str, str]]:
        return [{"profile" : i["href"],  "pfp" : i.find('img')["src"], 
                 "name"    : i["title"]
        } for i in i.select("a.contact")]
        
    async def parse_d(self, tag: bs4.Tag) -> str:
        if (t := tag.select("div.no-overflow")) == []:
            return "No description was provided"
        condition = lambda i: not isinstance(i, bs4.NavigableString) and i.find_all('a')
        try:
            return '\n'.join(i.get_text() if condition(i) else str(i) for i in t[0].contents)
        except IndexError:
            print(tag.prettify())
            
    async def parse_l(self, i: bs4.Tag) -> tuple[str]: 
        return (i.find('dt').get_text(), i.find('dd').get_text())
    
    async def parse_b(self, i: bs4.Tag) -> str: 
        return [i.find('span').decompose(), str(i)][1]
    
    async def parse_i(self, i: bs4.Tag) -> tuple[str]:
        x, y = (i.find('dl').get_text(), (i.find('dd') or i.find('a')).get_text())
        return (x[:-len(y)], y)

    async def cdetails(self, i) -> list[dict[str, str | list[dict[str, str]]]]: 
        return [{"link" :         i.find('a')["href"],    "title" : i.select('h4 a')[0].text, 
                  "img" : i.select('a img')[0]["src"], "advisers" : await self.parse_a(i)   ,
                 "description" : await self.parse_d(i)
        }]
    
    async def scrape(self) -> tuple[dict, int]:
        siteurls = ['https://khub.cvc.pshs.edu.ph/', 'https://khub.cvc.pshs.edu.ph/user/profile.php?id=563']
        sitehtml = await asyncio.gather(*[self.fetchSite(i) for i in siteurls]) 
        scrapers = await asyncio.gather(*[self.selector(i, 'html.parser') for i in sitehtml])
        home_courses = scrapers[0].select('div[role="main"]')[0].select('div#frontpage-course-list')[0]\
                                                                .select('div.card')
        user_details = scrapers[1].select('section.node_category')
        my_info = [self.parse_i(i) for i in user_details[-0].select('li.contentnode')]
        login   = [self.parse_l(i) for i in user_details[-1].select('li.contentnode')]
        badges  = [self.parse_b(i) for i in user_details[+1].select( 'ul.badges li' )]
        my_info, login, badges = await asyncio.gather(*[asyncio.gather(*i) for i in [my_info, login, badges]])
        my_info, login, badges = dict(my_info), dict(login), list(badges)
        return {"home" : await asyncio.gather(*[self.cdetails(i) for i in home_courses if i.find('a')]),
                "user" : {"info"  : my_info, "badges": badges, "login": login,
                          "name"  : str(scrapers[0].select('a.dropdown-item.text-username.menu-action')[0]
        .get_text()).strip()}}, 200


@app.route('/')
async def landing_page():
    return render_template('index.html')

@app.route('/comp-sci')
async def comp_sci():
    return render_template('Computer Science Files/misc.html')

@app.route("/flask/khub-login", methods=['GET', 'POST'])
async def get_session():
    BTN: str = 'button[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ '\
               'VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 '\
               'qIypjc TrZEUc lw1w4b"]'
    INP: str = 'input[class^="whsOnd zHQkBf"]'
    try:
        browser: webdriver.Firefox = webdriver.Firefox()
        WURL: str = 'https://accounts.google.com/'
        
        browser.get(WURL)
        
        CRED: list[str] = [i[1] for i in request.json.items()]
        
        browser.find_element('css selector', INP).send_keys(CRED[0])
        browser.find_element('css selector', BTN).click()
        browser.switch_to.new_window()
        browser.get('https://khub.cvc.pshs.edu.ph/')
        browser.switch_to.window(browser.window_handles[0])
        
        await asyncio.sleep(0.75)
        
        browser.find_element('css selector', INP).send_keys(CRED[1])
        browser.find_element('css selector', BTN).click()
        browser.switch_to.window(browser.window_handles[1])
        
        await asyncio.sleep(0.75)
        
        browser.find_element('css selector', 'a[title="Google"]').click()
        COOKIES = browser.get_cookies()[0]['value']
        print(COOKIES)
        browser.quit()
        return dict(cookie=COOKIES), 200
    except Exception as e:
        browser.quit()
        return dict(msg="Wrong credentials", other=str(e)), 500


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
async def PSHS_KHUB_INFO() -> tuple[dict[str, list], int]:
    kwargs = {"cookies" : request.cookies}
    async with aiohttp.ClientSession(**kwargs) as session:
        return await PSHS_KHUB_SCRAPER(session).scrape()

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

@app.route('/post-test', methods=['POST', 'GET'])
async def post_test():
    print(request.cookies)
    return {0: 1}, 200

if __name__ == '__main__':
    app.run(debug=True)