import asyncio, aiohttp, bs4, json
from bs4 import BeautifulSoup


MOODLE_SESSION = "r1tc9rfgshp7jmrgo9pm1vok0j"

class request(object):
    cookies: dict = {"MoodleSession": MOODLE_SESSION}  

class PSHS_KHUB_SCRAPER():
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session, self._rkwargs = session, {"allow_redirects": False}

    async def selector(self, *args, **kwargs) -> BeautifulSoup:
        return BeautifulSoup(*args, **kwargs)

    async def fetchSite(self, url: str) -> str | None:
        async with self.session.get(url, **self._rkwargs) as page:
            return await page.text()
    
    async def parse_a(self, i) -> list[dict[str, str]]:
        return [{"profile": i["href"], "pfp" : i.find('img')["src"], 
                 "name": i["title"]} for i in i.select("a.contact")]
        
    async def parse_d(self, tag: bs4.Tag) -> str:
        if (t := tag.select("div.no-overflow")) == []:
            return "No description was provided"
        condition = lambda i: not isinstance(i, bs4.NavigableString) and i.find_all('a')
        return '\n'.join(i.get_text() if condition(i) else str(i) for i in t[0].contents)
            
    async def parse_l(self, i: bs4.Tag) -> tuple[str]: 
        return (i.find('dt').get_text(), i.find('dd').get_text())
    
    async def parse_b(self, i: bs4.Tag) -> str: 
        return [i.find('span').decompose(), str(i)][1]
    
    async def parse_i(self, i: bs4.Tag) -> tuple[str]:
        x, y = (i.find('dl').get_text(), (i.find('dd') or i.find('a')).get_text())
        return (x[:-len(y)], y)

    async def cdetails(self, i) -> list[dict[str, str | list[dict[str, str]]]]: return [{
            "link": i.find('a')["href"], "title": i.select('h4 a')[0].text, 
            "img": i.select('a img')[0]["src"], "advisers": await self.parse_a(i),
            "description": await self.parse_d(i)
        }]
    
    async def scrape(self) -> tuple[dict, int]:
        pages    = ['https://khub.cvc.pshs.edu.ph/', 'https://khub.cvc.pshs.edu.ph/user/profile.php?id=563']
        abc      = await asyncio.gather(*[self.fetchSite(i) for i in pages]) 
        scrapers = await asyncio.gather(*[self.selector(i, "html.parser") for i in abc])
        home_courses = scrapers[0].select('div[role="main"]')[0].select('div#frontpage-course-list')[0]\
                                  .select('div.card')
        user_details = scrapers[1].select('section.node_category')
        my_info = [self.parse_i(i) for i in user_details [0].select('li.contentnode')]
        login   = [self.parse_l(i) for i in user_details[-1].select('li.contentnode')]
        badges  = [self.parse_b(i) for i in user_details [1].select('ul.badges li')]
        my_info, login, badges = await asyncio.gather(*[asyncio.gather(*i) for i in [my_info, login, badges]])
        my_info, login, badges = dict(my_info), dict(login), list(badges)
        return {"home"  : await asyncio.gather(*[self.cdetails(i) for i in home_courses if i.find('a')]),
                "user"  : {"info"  : my_info, "badges": badges, "login": login,
                           "name"  : str(scrapers[0].select('a.dropdown-item.text-username.menu-action')[0]
        .get_text()).strip()}}, 200
 
async def PSHS_KHUB_INFO() -> tuple[dict[str, str | list[dict[str, str]]], int] | None:
    async with aiohttp.ClientSession(cookies=request.cookies) as session:
        return await PSHS_KHUB_SCRAPER(session).scrape()
    
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
results = asyncio.run(PSHS_KHUB_INFO())
with open("results.json", "w") as f:
    json.dump(results, f, indent=4)