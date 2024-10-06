import asyncio
import aiohttp
import pandas as pd
import re


def clean_url(url):
    cleaned_url = re.sub(r'^\s*\d+\s*', '', url)
    return cleaned_url.strip()

def save_product(df):
    df.to_csv("../data/good_urls.csv", index=False)

async def scrape(url):
    timeout = aiohttp.ClientTimeout(total = 30)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    async with aiohttp.ClientSession(timeout = timeout, headers = headers) as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                good_urls.append(url)
        except asyncio.TimeoutError:
            print(f"Timeout occurred while scraping {url}")
            return None
        except (aiohttp.ClientError, UnicodeDecodeError) as e:
            print(f"Error scraping {url}: {e}")
            return None


async def scrab_m():
    tasks = []
    df = pd.read_csv('../data/URL_list.csv')
    df['max(page)'] = df['max(page)'].apply(clean_url)
    for index, row in df.iterrows():
        task = asyncio.create_task(scrape(row['max(page)']))
        tasks.append(task)
    await asyncio.gather(*tasks)

good_urls = []
loop = asyncio.get_event_loop()
loop.run_until_complete(scrab_m())
df_url = pd.DataFrame(good_urls, columns=['url'])
save_product(df_url)