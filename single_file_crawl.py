import asyncio
from crawl4ai import AsyncWebCrawler

#manual collection of relevant fighters for the upcoming UFC
links = [
    'https://www.ufc.com/athlete/austin-lingo',
'https://www.ufc.com/athlete/ben-sosoli',
'https://www.ufc.com/athlete/brad-riddell',
'https://www.ufc.com/athlete/daniel-rodriguez',
'https://www.ufc.com/athlete/dusko-todorovic',
'https://www.ufc.com/athlete/isabela-de-padua',
'https://www.ufc.com/athlete/jack-shore',
'https://www.ufc.com/athlete/jai-herbert',
'https://www.ufc.com/athlete/jamie-mullarkey',
'https://www.ufc.com/athlete/jiri-prochazka',
'https://www.ufc.com/athlete/joe-solecki',
'https://www.ufc.com/athlete/jonathan-pearce',
'https://www.ufc.com/athlete/khaos-williams',
'https://www.ufc.com/athlete/loma-lookboonmee',
'https://www.ufc.com/athlete/makhmud-muradov',
'https://www.ufc.com/athlete/mallory-martin',
'https://www.ufc.com/athlete/mark-madsen',
'https://www.ufc.com/athlete/modestas-bukauskas',
'https://www.ufc.com/athlete/peter-barrett',
'https://www.ufc.com/athlete/philip-rowe',
'https://www.ufc.com/athlete/philipe-lins',
'https://www.ufc.com/athlete/roman-bogatov',
'https://www.ufc.com/athlete/sergey-morozov',
'https://www.ufc.com/athlete/tj-brown',
'https://www.ufc.com/athlete/tom-aspinall',
'https://www.ufc.com/athlete/tony-gravely',
'https://www.ufc.com/athlete/tristan-connelly',
'https://www.ufc.com/athlete/tyson-nam',
'https://www.ufc.com/athlete/vanessa-melo'
]

async def main():
    async with AsyncWebCrawler() as crawler:
        for link in links:
            result = await crawler.arun(link)
            
            # Append the result to the file instead of overwriting
            with open('athlete_info.md', 'a', encoding="utf-8") as f:
                f.write(f"\n# {link}\n")  # Add a header for each link
                f.write(result.markdown)
                f.write("\n---\n")  # Add a separator between athletes

asyncio.run(main())
print('')

if __name__ == "__main__":
    asyncio.run(main())