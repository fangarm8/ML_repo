import pandas as pd
import asyncio
import aiohttp
import chardet
from bs4 import BeautifulSoup

async def save_html(url, filename):
    timeout = aiohttp.ClientTimeout(total=30)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                raw_data = await response.read()
                detected_encoding = chardet.detect(raw_data)['encoding']
                body = raw_data.decode(detected_encoding)
                soup = BeautifulSoup(body, 'html.parser')
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(soup.text)
                print(f"HTML сохранен в {filename}")
        except asyncio.TimeoutError:
            print(f"Timeout occurred while scraping {url}")
            return None
        except (aiohttp.ClientError, UnicodeDecodeError) as e:
            print(f"Error scraping {url}: {e}")
            return None


async def process_csv(df):
    tasks = []
    for i, url in enumerate(df.iloc[:, 0]):
        filename = f"../data/web_pages/new_html/{i:03}.txt"
        tasks.append(save_html(url, filename))
    await asyncio.gather(*tasks)

csv_file = '../data/good_urls.csv'
df = pd.read_csv(csv_file)
loop = asyncio.get_event_loop()
loop.run_until_complete(process_csv(df))