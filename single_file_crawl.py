import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://www.ufc.com/athlete/brandon-moreno")
        print(result.markdown)  # Print first 300 chars
        with open('individual_moreno.md', 'w') as f:
            f.write(result.markdown)

asyncio.run(main())
print('')

if __name__ == "__main__":
    asyncio.run(main())