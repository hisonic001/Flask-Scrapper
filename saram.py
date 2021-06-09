import requests
from bs4 import BeautifulSoup

def get_last_page(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    last_page = '3'
    return (int(last_page))

def extract_job(html):
    title = html.find("h2", {"class": "job_tit"}).get_text()
    company = html.find("strong", {"class": "corp_name"}).find("span")
    company = company.get_text(strip=True)
    location = html.find("div", {"class": "job_condition"}).find("a").get_text()
    job_id = html["value"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "link":f"https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx={job_id}"
    }


def extract_saram_jobs(last_page,URL):
    jobs = []
    for page in range(1,last_page+1):
        print(f'page is {page},{last_page}')
        result = requests.get(f"{URL}&recruitPage={page}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "item_recruit"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs(word):
    URL = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&keydownAccess=&searchword={word}"
    last_page = get_last_page(URL)
    jobs = extract_saram_jobs(last_page,URL)
    return jobs

# # word 바꿔주기