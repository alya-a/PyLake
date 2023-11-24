import requests
from bs4 import BeautifulSoup

class LakeScraper:
    def __init__(self, category_link):
        self.category_link = category_link
        #edit user-agent if needed
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.lakes = []

    def get_lakes_from_category_wikipedia(self):
        try:
            response = requests.get(self.category_link, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            lake_list = soup.find('div', {'id': 'mw-pages'})

            if lake_list:
                lake_links = lake_list.find_all('a')

                # Filter out unwanted items from the list
                self.lakes = [(a.text.strip(), "https://en.wikipedia.org" + a['href']) for a in lake_links if 'may not reflect recent changes' not in a.text]

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def display_lakes(self):
        if not self.lakes:
            print("Unable to retrieve the list of lakes.")
            return

        print("\nList of lakes in Berlin:")
        for i, (lake, _) in enumerate(self.lakes, 1):
            print(f"{i}. {lake}")

    def explore_lake(self, lake_index):
        if 1 <= lake_index <= len(self.lakes):
            selected_lake, lake_link = self.lakes[lake_index - 1]
            print(f"\nInformation about {selected_lake} can be found at: {lake_link}")
            return True
        else:
            print("Invalid lake number. Please enter a valid number.")
            return False

def main():
    category_link = "https://en.wikipedia.org/wiki/Category:Lakes_of_Berlin"
    lake_scraper = LakeScraper(category_link)
    lake_scraper.get_lakes_from_category_wikipedia()
    lake_scraper.display_lakes()

    while True:
        user_input = input("\Hello there! Enter the number of the lake you want to explore (or type 'exit' to exit): ")

        if user_input.lower() == 'exit':
            print("Exiting the program. We hope you were able to find a lake to explore on your next journey!")
            break

        try:
            lake_index = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number or type 'exit' to exit.")
            continue

        success = lake_scraper.explore_lake(lake_index)
        if success:
            print("Exiting the program. We hope you were able to find a lake to explore on your next journey!")
            break

if __name__ == "__main__":
    main()
