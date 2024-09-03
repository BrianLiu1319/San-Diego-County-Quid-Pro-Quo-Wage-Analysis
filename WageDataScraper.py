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

    num_employees_txt = soup.find(string = lambda x: x and 'employee' in x)
    if num_employees_txt is not None:
        num_employees = int(num_employees_txt.split()[0].replace(',', ''))

    # Try to find pagination text
    pagination_text = soup.find(string=lambda x: x and 'Page' in x)

    if pagination_text and num_employees>50:
        # Extracts the last number, which should be the total pages
        total_pages = int(pagination_text.split()[-1])
        return total_pages
    else:
        # If pagination text isn't found or less than 50 employees, assume there is only 1 page
        return 1

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

    agencies = {}
    agencies['cities'] = ['San Diego', 'Carlsbad', 'Chula Vista', 'Coronado', 'Del Mar',
                   'El Cajon', 'Encinitas', 'Escondido', 'Imperial Beach', 'La Mesa',
                   'Lemon Grove', 'National City', 'Oceanside', 'Poway', 'San Marcos',
                   'Santee', 'Solana Beach', 'Vista']
    agencies['school districts'] = ['Alpine Union Elementary', 'Bonsall Unified', 'Borrego Springs Unified', 'Cajon Valley Union',
                     'Cardiff Elementary', 'Carlsbad Unified', 'Chula Vista Elementary', 'Coronado Unified',
                     'Dehesa Elementary', 'Del Mar Union Elementary', 'Encinitas Union Elementary', 'Escondido Union',
                     'Escondido Union High', 'Fallbrook Union Elementary', 'Fallbrook Union High',
                     'Grossmont Union High', 'Jamul-Dulzura Union Elementary', 'Julian Union Elementary',
                     'Julian Union High', 'Lakeside Union Elementary-San Diego', 'La Mesa-Spring Valley',
                     'Lemon Grove School District', 'Mountain Empire Unified', 'National Elementary',
                     'Oceanside Unified', 'Poway Unified', 'Ramona City Unified', 'Rancho Santa Fe Elementary',
                     'San Diego County Office of Education', 'San Diego Unified', 'San Dieguito Union High',
                     'San Marcos Unified', 'San Pasqual Union Elementary', 'Santee School District',
                     'San Ysidro Elementary', 'Solana Beach Elementary', 'South Bay Union', 'Spencer Valley Elementary',
                     'Sweetwater Union High', 'Vallecitos Elementary', 'Valley Center-Pauma Unified', 'Vista Unified',
                     'Warner Unified']

    agencies_remaining = []

    search_filter = 'K12'
    # Valid input for category - 'cities', 'school districts'
    category = 'school districts'
    all_data = []
    headers = None

    for agency in agencies[category]:
        agency = agency.lower().replace(' ', '-')
        print('\n' + agency)
        for year in years:
            if category == 'cities':
                base_url = f"https://transparentcalifornia.com/salaries/{year}/{agency}/?page="
            elif category == 'school districts':
                base_url = f"https://transparentcalifornia.com/salaries/{year}/school-districts/san-diego/{agency}/?page="

            page_data = fetch_page_data(f"{base_url}{1}")
            if page_data is None:
                continue

            numPages = get_total_pages(page_data)
            print(f"{agency} {year}: " + str(numPages) + " pages")

            if numPages > 100:
                agencies_remaining.append(f"{agency} {year}")
                continue
            elif numPages > 50:
                suffix = '&s=-name'
                numPages2 = numPages - 50
                numPages = 50
                #Z-A
                for page in range(1, numPages2 + 1):  # Loop through all pages
                    print(f"Fetching data from page {page}...")
                    page_url = f"{base_url}{page}{suffix}"
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

            #A-Z
            suffix = '&s=name'
            for page in range(1, numPages + 1):  # Loop through all pages
                print(f"Fetching data from page {page}...")
                page_url = f"{base_url}{page}{suffix}"
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
        df.to_csv(f'{search_filter.lower()}_salaries.csv', index=False)
        print(f"Data written to {search_filter.lower()}_salaries.csv")
    print(agencies_remaining)

if __name__ == '__main__':
    main()
