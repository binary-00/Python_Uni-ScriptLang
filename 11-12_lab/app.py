import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
import sys

# Define a function to download a book from the Project Gutenberg website
def download_book(book_id: str):
    # Construct the URL of the book
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-h/{book_id}-h.htm"
    # Send a GET request to the URL to download the book
    response = requests.get(url)
    # Save the book to an HTML file
    with open(f"{book_id}.html", "w", encoding="utf-8") as f:
        f.write(response.text)


# Define a function to extract information about the book such as its title, author and first chapter
def extract_book_info(book_id: str):
    # Open the HTML file of the book
    with open(f"{book_id}.html", "r", encoding="utf-8") as f:
        html_content = f.read()
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        # Extract the title and author of the book
        title = soup.find("h1").text
        author = soup.find("h2").text
        # Find all chapters in the book
        chapters = soup.find_all("div", class_="chapter")
        chapter_i_content = ""

        # Loop through each chapter and extract its content
        for chapter in chapters:
            chapter_title = chapter.find("h2").text.strip()
            if chapter_title == "CHAPTER I":
                paragraphs = chapter.find_all("p")
                for paragraph in paragraphs:
                    # Remove any HTML tags from the paragraph content
                    paragraph_text = "".join(paragraph.findAll(text=True))
                    chapter_i_content += paragraph_text.strip() + "\n"

        first_chapter = chapter_i_content.strip()
        return title, author, first_chapter


# Define a function to count the lengths of paragraphs in the first chapter of the book and return a dictionary of counts
def count_paragraph_lengths(book_id: str):
    _, _, first_chapter = extract_book_info(book_id)
    paragraphs = first_chapter.split("\n\n")
    paragraph_lengths = []
    for p in paragraphs:
        num_words = len(p.split())
        rounded_num_words = round(num_words / 10) * 10
        paragraph_lengths.append(rounded_num_words)
    sorted_paragraph_lengths = sorted(paragraph_lengths)
    counts = Counter(sorted_paragraph_lengths)
    return counts


# Define a function to plot a bar chart showing the distribution of paragraph lengths in the first chapter of the book
def plot_paragraph_lengths(book_id: str):
    counts = count_paragraph_lengths(book_id)
    x = list(counts.keys())
    y = list(counts.values())
    plt.bar(x, y)
    plt.xlabel("Paragraph Length (rounded to nearest 10)")
    plt.ylabel("Number of Paragraphs")
    plt.title("Distribution of Paragraph Lengths in First Chapter")
    plt.show()


# Run the download_book, extract_book_info and plot_paragraph_lengths functions when the script is executed and a book ID is provided as a command line argument
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a book identifier.")
        sys.exit(1)
    book_id = sys.argv[1]
    download_book(book_id)
    title, author, first_chapter = extract_book_info(book_id)
    print(f"Title: {title}\nAuthor: {author}\nFirst Chapter: {first_chapter}")
    plot_paragraph_lengths(book_id)
