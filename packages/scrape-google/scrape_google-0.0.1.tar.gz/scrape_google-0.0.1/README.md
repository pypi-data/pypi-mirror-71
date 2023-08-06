# scraping

This package scrapes the string `k` from the google search and returns at max top `n` links from the first page of the google search.

### Usage

```
import scrape_google
scrape_google.scrape(k,n)
```

### Example

```
import scrape_google
list=scrape_google.scrape("Hello World",5)
print(list)
```
