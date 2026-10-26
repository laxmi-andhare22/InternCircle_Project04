import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

# Headers to avoid blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def scrape_hacker_news():
    """Scrape Tech Headlines from Hacker News"""
    print("\n--- Scraping Hacker News (Tech Headlines) ---")
    url = "https://news.ycombinator.com"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        headlines = []
        titles = soup.find_all('span', class_='titleline')
        
        for i, title_span in enumerate(titles[:10], 1):
            link_tag = title_span.find('a')
            if link_tag:
                title = link_tag.text.strip()
                link = link_tag.get('href', '')
                headlines.append({"id": i, "title": title, "link": link})
                print(f"{i}. {title}")
        
        # Save to file
        with open("tech_headlines.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["ID", "Title", "Link", "Scraped_At"])
            writer.writeheader()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for item in headlines:
                writer.writerow({"ID": item["id"], "Title": item["title"], "Link": item["link"], "Scraped_At": now})
        
        print(f"\nSaved {len(headlines)} headlines to tech_headlines.csv")
        return headlines
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Hacker News: {e}")
        return []

def scrape_quotes():
    """Scrape Quotes from quotes.toscrape.com"""
    print("\n--- Scraping Quotes (quotes.toscrape.com) ---")
    url = "http://quotes.toscrape.com"
    all_quotes = []
    
    try:
        # Scrape first 3 pages
        for page in range(1, 4):
            print(f"Scraping page {page}...")
            page_url = f"{url}/page/{page}/"
            response = requests.get(page_url, headers=HEADERS, timeout=10)
            
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes = soup.find_all('div', class_='quote')
            
            if not quotes:
                break
                
            for q in quotes:
                text = q.find('span', class_='text').text.strip() if q.find('span', class_='text') else ""
                author = q.find('small', class_='author').text.strip() if q.find('small', class_='author') else ""
                tags = [tag.text for tag in q.find_all('a', class_='tag')]
                all_quotes.append({"text": text, "author": author, "tags": ", ".join(tags)})
                print(f'  "{text[:50]}..." - {author}')
        
        # Save to file
        with open("quotes.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Text", "Author", "Tags"])
            writer.writeheader()
            writer.writerows(all_quotes)
        
        with open("quotes.txt", "w", encoding='utf-8') as f:
            for i, q in enumerate(all_quotes, 1):
                f.write(f"{i}. {q['text']} - {q['author']} [{q['tags']}]\n")
        
        print(f"\nSaved {len(all_quotes)} quotes to quotes.csv and quotes.txt")
        return all_quotes
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping quotes: {e}")
        return []

def generate_report():
    """Generate summary report"""
    print("\n--- Generating Report ---")
    report = f"Web Scraping