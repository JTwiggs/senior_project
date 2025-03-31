import asyncio
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import requests
from xml.etree import ElementTree
import re


def trim_footer(fname):
    # list to store file lines
    lines = []
    # read file
    with open(fname, 'r') as fp:
    # read an store all lines into list
        lines = fp.readlines()

    # Write file
    with open(fname, 'w') as fp:
    # iterate each line
        for number, line in enumerate(lines):
            #delete final 3 lines of the file
            if number not in [(len(lines) - 3), (len(lines) - 2), (len(lines) - 1)]:
                fp.write(line)


async def crawl_sequential(urls: List[str]):
    level = 0
    print(f'level: {level}')
    print("\n=== Sequential Crawling with Session Reuse ===")

    browser_config = BrowserConfig(
        headless=True,
        # For better performance in Docker or low-memory environments:
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )

    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )

    # Create the crawler (opens the browser)
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    try:
        session_id = "session1"  # Reuse the same session across all URLs
        while True:
            if level == 0:
                print('starting main page url collection')
                for url in urls:
                    result = await crawler.arun(
                        url=url,
                        config=crawl_config,
                        session_id=session_id
                    )
                    if result.success:
                        print(f"Successfully crawled: {url}")
                        # E.g. check markdown length
                        print(f"Markdown length: {len(result.markdown.raw_markdown)}")
                    else:
                        print(f"Failed: {url} - Error: {result.error_message}")
                    with open('ufc_base_scrape_results.md', 'w', encoding="utf-8") as f:
                        print(result.markdown, file=f)
                    with open('ufc_base_scrape_results.md', 'r', encoding="utf-8") as f:
                        lines = f.readlines()
                        lines = lines[:-3] #remove footer from the file
                urls = [line.split(" | ")[0].strip("<>") for line in lines]
                # Use list comprehension to filter only athlete URLs (this is where any custom filtering can be done)
                pattern = re.compile(r'https://www.ufc.com/athlete[^\s|>]*')
                matches = [url for url in urls if pattern.match(url)]
                # Save the filtered URLs
                with open("athlete_info_from_main.txt", "a") as f:
                    for match in matches:
                        print(match, file=f)
                # Remove the last line from the file
                with open("fighter_urls.txt", "r") as f:
                    lines = f.readlines()
                    lines = lines[:-1] #remove extra line from the file
                print('figher urls collected')
                level += 1
            else:
                print('starting fighter page info collection')
                for url in matches:
                    print(url)
                    result = await crawler.arun(
                        url=url,
                        config=crawl_config,
                        session_id=session_id
                    )
                    if result.success:
                        print(f"Successfully crawled: {url}")
                        # E.g. check markdown length
                        print(f"Markdown length: {len(result.markdown.raw_markdown)}")
                    else:
                        print(f"Failed: {url} - Error: {result.error_message}")
                    with open('ufc_fighter_data.md', 'a', encoding="utf-8") as f:
                        f.write(f"\n {url}\n")  # Add a header for each link
                        print(result.markdown, file=f)
                        f.write("\n---\n")  # Add a separator between athletes
                print('fighter data collected')
                break
    finally:
        # After all URLs are done, close the crawler (and the browser)
        await crawler.close()
        
        
def get_ufc_docs_urls():
    """
    Fetches all URLs from the UFC official website.
    Uses the sitemap (https://www.ufc.com/sitemap.xml) to get these URLs.
    
    Returns:
        List[str]: List of URLs
    """            
    sitemap_url = "https://www.ufc.com/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        
        # Parse the XML
        root = ElementTree.fromstring(response.content)
        
        # Extract all URLs from the sitemap
        # The namespace is usually defined in the root element
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        
        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []



async def main():
    urls = get_ufc_docs_urls()
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        await crawl_sequential(urls) #high level links, then loops once for fighter data
    else:
        print("No URLs found to crawl")

if __name__ == "__main__":
    asyncio.run(main())