import requests
import pandas as pd
from bs4 import BeautifulSoup


def fetch_page_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def get_total_pages(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    pagination_text = soup.find(string=lambda x: x and 'Page' in x)
    if pagination_text:
        total_pages = int(pagination_text.split()[-1])  # Extracts the last number, which should be the total pages
        return total_pages
    return 1  # Default to 1 if not found

def parse_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')

    data = []
    if table is None:
        print('No table found')
        return [None, None]

    headers = [header.text.strip() for header in table.find_all('th')]

    # Reordering headers: Add 'Year' and 'City' at the beginning
    headers = ['Year', 'City'] + headers

    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) > 0:
            row_data = []
            for i, col in enumerate(columns):
                if i == 1:  # Assuming Job Title is in the second column (index 1)
                    text_lines = list(col.stripped_strings)
                    job_title = text_lines[0] if len(text_lines) > 0 else ''

                    if len(text_lines) > 1:
                        city_year = text_lines[1].split(',')
                        city = city_year[0].strip()
                        year = city_year[1].strip() if len(city_year) > 1 else ''
                    else:
                        city = ''
                        year = ''

                    # Append in the desired order: Year, City, Job Title
                    row_data = [year, city] + row_data
                    row_data.append(job_title)
                else:
                    row_data.append(' '.join(col.stripped_strings))

            # Adjust the number of fields in the row_data to match the headers
            if len(row_data) < len(headers):
                row_data += [''] * (len(headers) - len(row_data))
            elif len(row_data) > len(headers):
                # Add new headers if new fields are encountered
                new_headers = ['Field ' + str(i+1) for i in range(len(headers), len(row_data))]
                headers += new_headers

            data.append(row_data)

    return headers, data


def main():
    years = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    cities = ['carlsbad', 'chula-vista', 'coronado', 'el-cajon', 'escondido', 'la-mesa', 'national-city', 'oceanside',
              'san-diego']
    search_filter = 'Police'
    all_data = []
    headers = None

    for city in cities:
        for year in years:
            base_url = f"https://transparentcalifornia.com/salaries/search/?a={city}&q={search_filter}&y={year}&page="
            numPages = get_total_pages(fetch_page_data(f"{base_url}{1}"))
            print(f"{city} {year}: " + str(numPages) + " pages")

            for page in range(1, numPages + 1):  # Loop through all pages
                print(f"Fetching data from page {page}...")
                page_url = f"{base_url}{page}"
                html_content = fetch_page_data(page_url)

                if not html_content:
                    print(f"No data returned for page {page}")
                    break

                page_headers, page_data = parse_table(html_content)

                if page_headers is None or page_data is None:
                    continue

                if headers is None:
                    headers = page_headers
                else:
                    # Update headers if new headers are found
                    for h in page_headers:
                        if h not in headers:
                            headers.append(h)

                all_data.extend(page_data)

    if len(all_data) != 0:
        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(all_data, columns=headers)
        df.to_csv(f'police_salaries.csv', index=False)
        print(f"Data written to police_salaries.csv")


if __name__ == '__main__':
    main()