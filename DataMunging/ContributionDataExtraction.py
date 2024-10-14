import os
import csv
import pandas as pd
import fitz  # PyMuPDF

def extract_data(filename, data, pac):
    file = open(f"C:/Users\Ericm\OneDrive\Documents/{pac}/{filename}",
                "r")

    lines = file.readlines()

    file.close()

    i = 0
    while pac not in lines[i]:
        i+=1

    #adjust lines when district # is included in the form
    if lines[i+11].strip().isdigit():
        if lines[i+11] in lines[i+10]:
            lines.pop(i+11)
        else:
            lines[i+10] = lines[i+10][0:-1] + ' District ' + lines[i+11] + '\n'
            lines.pop(i + 11)

    #adjust lines if cumulative YTD is included in the form
    if 'cumulative' in lines[i+14].lower():
        lines.pop(i+14)

    data['DATE'].append(lines[i+12].strip())
    data['NAME OF FILER'].append('Carlsbad Police Officer\'s Association Independent Expenditure Committee')
    data['NAME OF CANDIDATE'].append(lines[i + 9].strip())
    data['OFFICE SOUGHT OR HELD'].append(lines[i + 10].strip())
    data['SUPPORT OR OPPOSE'].append('SUPPORT')
    data['DESCRIPTION OF EXPENDITURE'].append(lines[i + 13].strip())
    data['AMOUNT'].append(lines[i + 14].strip())

def extract_text_from_pdf(pdf_path):
    # Open the provided PDF file
    document = fitz.open(pdf_path)

    # Initialize an empty string to store the extracted text
    extracted_text = ""

    # Iterate over each page in the PDF
    for page_num in range(len(document)):
        # Get the page
        page = document.load_page(page_num)
        # Extract the text from the page
        page_text = page.get_text()
        # Append the text to the extracted_text variable
        extracted_text += page_text + "\n"  # Add a newline after each page

    return extracted_text


def format_text(text):
    # Split the text into lines
    lines = text.splitlines()

    # Remove extra whitespace from each line and remove empty lines
    formatted_lines = [line.strip() for line in lines if line.strip()]

    # Join the lines back together with consistent line breaks
    formatted_text = "\n".join(formatted_lines)

    return formatted_text


def save_text_to_file(text, output_path):
    # Write the formatted text to a file
    with open(output_path, 'w') as file:
        file.write(text)

def convert_pdfs_to_text(pac):
    for filename in os.listdir(f"C:/Users\Ericm\OneDrive\Documents/{pac}"):
        print(filename)
        pdf_path = f"C:/Users\Ericm\OneDrive\Documents/{pac}/{filename}"  # Path to the input PDF file
        output_path = f"C:/Users\Ericm\OneDrive\Documents/{pac}/{filename[0:-4]}.txt"  # Path to the output text file

        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(pdf_path)

        # Format the extracted text
        formatted_text = format_text(extracted_text)

        # Save the formatted text to a file
        save_text_to_file(formatted_text, output_path)

        print(f"Text extracted and saved to {output_path}")


def main():
    data = {'DATE': [], 'NAME OF FILER': [], 'NAME OF CANDIDATE': [], 'OFFICE SOUGHT OR HELD': [],
            'SUPPORT OR OPPOSE': [], 'DESCRIPTION OF EXPENDITURE': [], 'AMOUNT': []}
    pac = 'Oceanside Police Officers\' Association'

    convert_pdfs_to_text(pac)

    for filename in os.listdir(f"C:/Users\Ericm\OneDrive\Documents/{pac}"):
        if '.txt' in filename:
            extract_data(filename, data, pac)
    
    df = pd.DataFrame(data)

    df['DATE'] = pd.to_datetime(df['DATE'])

    df.set_index('DATE', inplace=True)

    df.to_csv(
        f"C:/Users\Ericm\OneDrive\Documents/{pac}/{pac} ContributionsBinder.csv",
        index=True)


if __name__ == "__main__":
    main()

