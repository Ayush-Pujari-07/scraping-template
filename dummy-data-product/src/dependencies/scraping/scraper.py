import requests
from bs4 import BeautifulSoup
import pandas as pd

hrefs = []
texts = []
complete_links = {}
header = ({'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0", 'Accept-Language': "en-US, en;q=0.5"})


# Extraction compete links form the website.
def main_extractor():
    url_ = input("Enter the URL of the Page: ")
    try:
        page = requests.get(url=url_, headers=header)
        soup_link = BeautifulSoup(page.content, 'html.parser')
        head_links = soup_link.find_all('a', attrs={"class": "nav-link dropdown-toggle"})
        for link in head_links:
            hrefs.append(link.get('href'))
            texts.append(link.text.strip())
            print(link.text)
        # Get the complete Links
        for i in range(len(hrefs)):
            if 'https:/' not in hrefs[i]:
                new_link = "https://www.bls.gov" + hrefs[i]
                complete_links[texts[i]] = new_link
            else:
                complete_links[texts[i]] = hrefs[i]
        print(complete_links)
    except:
        url_ = input("Enter the URL of the Page: ")


# Choose the segment to extract from the given links
def choose_segment():
    metadata_segment = int(input("Choose segment:\n1.Home\n2.Subjects\n3.Data Tools\n4.Publications\n5.Economic "
                                 "Releases\n6.Classroom\n7.Beta\n8.None\n"))
    if metadata_segment == 1:
        return complete_links['Home']
    elif metadata_segment == 2:
        return complete_links['Subjects']
    elif metadata_segment == 3:
        return complete_links['Data Tools']
    elif metadata_segment == 4:
        return complete_links['Publications']
    elif metadata_segment == 5:
        return complete_links['Economic Releases']
    elif metadata_segment == 6:
        return complete_links['Classroom']
    elif metadata_segment == 7:
        return complete_links['Beta']
    else:
        print("Thank you for exploring!!")
        pass


# Get the Metadata links for further scraping and extracting data
def get_metadata():
    url_metadata = choose_segment()
    final_metadata_links = []
    final_metadata_titles = []
    metadata_page = requests.get(url=url_metadata, headers=header)
    soup_metadata = BeautifulSoup(metadata_page.content, 'html.parser')
    # Get the Links for the segments metadata
    title = soup_metadata.title.text.split(':')[0].strip()
    if title == 'Subject Area Categories' and title != 'K‐12':
        links = soup_metadata.find('table', attrs={'class': 'on-this-page-table'}).find_all('a')
        # print(links)
        for link in links:
            final_metadata_links.append(url_metadata + link.get('href'))
            final_metadata_titles.append(link.text)
        print(final_metadata_titles)
        print(final_metadata_links)
    elif title != 'Subject Area Categories' and title != 'K‐12':
        links = soup_metadata.find('div', attrs={'class': 'in-this-page-content'}).find_all('a')
        # print(links)
        for link in links:
            final_metadata_links.append(url_metadata + link.get('href'))
            final_metadata_titles.append(link.text)
        print(final_metadata_titles)
        print(final_metadata_links)
    else:
        links = soup_metadata.find('div', attrs={'id': 'k12-banner'}).find_all('a')
        # print(links)
        for link in links:
            final_metadata_links.append(url_metadata + link.get('href'))
            final_metadata_titles.append(link.text)
        print(final_metadata_titles)
        print(final_metadata_links)
    segment_metadata = pd.DataFrame()
    segment_metadata['Titles'] = final_metadata_titles
    segment_metadata['Links'] = final_metadata_links
    segment_metadata.to_csv(f'D:\\Data Science Project\\Taiyo.AI\\ts-mesh-pipeline-main\\dummy-data-product\\src'
                            f'\\dependencies\\scraping\\{title}.csv')


main_extractor()
get_metadata()
