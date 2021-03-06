from lxml import html
from lxml.cssselect import CSSSelector
import requests
import sys as Sys
# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : number of decimals in percent complete (Int) 
        barLength   - Optional  : character length of bar (Int) 
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    Sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    Sys.stdout.flush()
    if iteration == total:
        print("\n")

folder = u"farmostwood/"
url = "http://blog.farmostwood.net/sitemap" 
sitemap = html.fromstring(requests.get(url).content)

except_list = [u"Photo", u"Fiction", u"Movie"]
category_select = CSSSelector("div.ddsg-wrapper>ul>li")
category_title_select = CSSSelector("div.ddsg-wrapper>ul>li>a")
post_title_select = CSSSelector("ul>li>a")
category_nodes = category_select(sitemap)
category_titles = category_title_select(sitemap)
category_count = len(category_nodes)

for i in range(category_count):
    if category_titles[i].text not in except_list:
        post_nodes_in_category = post_title_select(category_nodes[i])
        print "Scrapping articles in " + category_titles[i].text + "..."
               
        cur_count = 0
        post_count_in_category = len(post_nodes_in_category)
        for node in post_nodes_in_category:
            try:
                cur_count = cur_count + 1
                printProgress(cur_count, post_count_in_category)

                post_url = node.get("href")
                post_html = html.fromstring(requests.get(post_url).content)
                post_select = CSSSelector(".entrytext")
                title_select = CSSSelector("h1>a>img")
                title_text = title_select(post_html)[0].get("alt")
                title = (u"<h1>" + title_text + u"</h1>").encode("utf-8")
                post = html.tostring(post_select(post_html)[0]).encode("utf-8")
                filepath = folder + title_text + u".html"
                with open(filepath, "w+") as f:
                    f.write(title)
                    f.write(post)
            except Exception:                    
                print "Error scrapping: " + post_url
