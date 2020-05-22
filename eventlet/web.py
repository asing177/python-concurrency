from eventlet.green import urllib2
import eventlet
import re

# http://daringfireball.net/2009/11/liberal_regex_for_matching_urls
url_regex = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')


def fetch(url, seen, pool):
    """Fetch a url, stick any found urls into the seen set, and
    dispatch any new ones to the pool."""
    print("fetching", url)
    data = ''
    with eventlet.Timeout(5, False):
        data = urllib2.urlopen(url).read()
    for url_match in url_regex.finditer(data):
        new_url = url_match.group(0)
        # only send requests to eventlet.net so as not to destroy the internet
        if new_url not in seen and 'eventlet.net' in new_url:
            seen.add(new_url)
            # while this seems stack-recursive, it's actually not:
            # spawned greenthreads start their own stacks
            pool.spawn_n(fetch, new_url, seen, pool)


def crawl(start_url):
    """Recursively crawl starting from *start_url*.  Returns a set of
    urls that were found."""
    pool = eventlet.GreenPool()
    seen = set()
    fetch(start_url, seen, pool)
    pool.waitall()
    return seen

seen = crawl("http://eventlet.net")
print("I saw these urls:")
print("\n".join(seen))