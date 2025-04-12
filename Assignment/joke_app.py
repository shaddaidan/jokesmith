# Import necessary modules
import requests  # For making HTTP requests to the joke API
from fpdf import FPDF  # For saving jokes as a PDF file

# Define a class for fetching and handling jokes
class JokeFetcher:
    # Constructor: initializes the object with optional parameters for customizing the joke request
    def __init__(self, category=None, blacklist=None, response_format="json",
                 joke_type="Any", search_string=None, id_range=None,
                 amount=1, lang="en", auth_token=None, user_agent=None, return_headers=False):
        
        self.base_url = "https://v2.jokeapi.dev/joke"  # Base URL for the Joke API
        self.category = ",".join(category) if category else "Any"  # Join multiple categories into a string
        self.blacklist = ",".join(blacklist) if blacklist else None  # Join multiple blacklist flags
        self.response_format = response_format
        self.joke_type = joke_type  # 'single', 'twopart', or 'Any'
        self.search_string = search_string  # Used to filter jokes by keyword
        self.id_range = id_range  # Specific ID range of jokes
        self.amount = amount  # Number of jokes to fetch
        self.lang = lang  # Language code
        self.auth_token = auth_token  # Optional authentication token
        self.user_agent = user_agent  # Optional custom user-agent
        self.return_headers = return_headers  # Whether to return response headers
        self.jokes = []  # List to store fetched jokes

    # Method to fetch jokes from the API
    def fetch_jokes(self):
        # Set up query parameters
        params = {
            "amount": self.amount,
            "type": self.joke_type if self.joke_type != "Any" else None,
            "lang": self.lang,
            "format": self.response_format
        }
        if self.blacklist:
            params["blacklistFlags"] = self.blacklist
        if self.search_string:
            params["contains"] = self.search_string
        if self.id_range:
            params["idRange"] = f"{self.id_range[0]}-{self.id_range[1]}"  # Format as 'start-end'

        # Optional request headers
        headers = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        if self.user_agent:
            headers["User-Agent"] = self.user_agent

        try:
            # Make the API call
            response = requests.get(f"{self.base_url}/{self.category}", params=params, headers=headers)
            response.raise_for_status()  # Raise an error for bad HTTP status

            # Parse response based on return_headers flag
            if self.return_headers:
                return self._parse_response(response.json()), response.headers
            else:
                self.jokes = self._parse_response(response.json())
        except requests.RequestException as e:
            # If an error occurs, store the error as a joke
            self.jokes = [f"Error fetching joke: {e}"]

    # Internal method to parse the API JSON response
    def _parse_response(self, data):
        if self.amount == 1 and "joke" in data:
            return [self._format_joke(data)]  # Single joke
        return [self._format_joke(j) for j in data.get("jokes", [])]  # Multiple jokes

    # Internal method to format a joke for display
    def _format_joke(self, data):
        if data.get("error"):
            return "API Error: Could not retrieve joke."
        # Return either single or two-part joke format
        return data["joke"] if data["type"] == "single" else f"{data['setup']}\n{data['delivery']}"

    # Save jokes to a plain text file
    def save_as_txt(self, filename="jokes.txt"):
        with open(filename, "w", encoding="utf-8") as file:
            for joke in self.jokes:
                file.write(joke + "\n\n")  # Write each joke with spacing
        return filename

    # Save jokes to a PDF file
    def save_as_pdf(self, filename="jokes.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for joke in self.jokes:
            pdf.multi_cell(0, 10, txt=joke + "\n", align="L")  # Add joke text to PDF
        pdf.output(filename)  # Save the PDF file
        return filename
