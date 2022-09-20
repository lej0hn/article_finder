from bs4 import BeautifulSoup
import requests
import re 

keyword = input('Please input a keyword to search: ')
urls = [f"https://www.cnn.gr/",f"https://www.typosthes.gr/",f"https://www.in.gr/",f"https://www.kathimerini.gr/",f"https://www.protothema.gr/",f"https://www.avgi.gr/"]
links = {}

####Returns the rough html with the keyword####
def parser(url, keyword):
    print('Source is: ', url, '\n')
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    results = doc.find_all(text = re.compile("(?i)" + keyword + "*"))
    return results


####Prints and returns dictionary with name of article as key
#  and it's link as value ####
def searcher(url,results):
    if len(results) != 0:
        for result in results:
            name = " ".join(result.split())
            link = result.parent.parent.parent.get('href')
            if link is None:
                link = result.parent.parent.parent.find('a').get('href')
            if name not in links.keys():   #Avoid double appearance of one article
                links[name] = url+link
        
            for item in links:
                print(item , " : ", links[item], '\n')    
            #Exporting to txt file named article_names 
            with open('article_names.txt', 'w') as f:
                for key in links:
                    f.write(key)
                    f.write(" : ")
                    f.write(links[key])
                    f.write('\n\n')
                    f.write('---------------------------------------------------------------\n')
            f.close()
    else:
        print('No results found in: ', url)
        with open('article_names.txt', 'a') as f:
            f.write('No results found in: ')
            f.write(url)
            f.write('\n')
        f.close()
    return links



for url in urls:
    try:
        links = searcher(url,parser(url,keyword))
    except:
        pass
if len(links) == 0:
    with open('article_names.txt', 'a') as f:
        f.write('No results found')
    f.close()
    print('No results found')

