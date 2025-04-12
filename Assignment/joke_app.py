# joke_app.py
import requests
from fpdf import FPDF

class JokeFetcher:
    def __init__(self, category=None, blacklist=None, response_format="json",
                 joke_type="Any", search_string=None, id_range=None,
                 amount=1, lang="en", auth_token=None, user_agent=None, return_headers=False):
        
        self.base_url = "https://v2.jokeapi.dev/joke"
        self.category = ",".join(category) if category else "Any"
        self.blacklist = ",".join(blacklist) if blacklist else None
        self.response_format = response_format
        self.joke_type = joke_type
        self.search_string = search_string
        self.id_range = id_range
        self.amount = amount
        self.lang = lang
        self.auth_token = auth_token
        self.user_agent = user_agent
        self.return_headers = return_headers
        self.jokes = []

    def fetch_jokes(self):
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
            params["idRange"] = f"{self.id_range[0]}-{self.id_range[1]}"

        headers = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        if self.user_agent:
            headers["User-Agent"] = self.user_agent

        try:
            response = requests.get(f"{self.base_url}/{self.category}", params=params, headers=headers)
            response.raise_for_status()
            if self.return_headers:
                return self._parse_response(response.json()), response.headers
            else:
                self.jokes = self._parse_response(response.json())
        except requests.RequestException as e:
            self.jokes = [f"Error fetching joke: {e}"]

    def _parse_response(self, data):
        if self.amount == 1 and "joke" in data:
            return [self._format_joke(data)]
        return [self._format_joke(j) for j in data.get("jokes", [])]

    def _format_joke(self, data):
        if data.get("error"):
            return "API Error: Could not retrieve joke."
        return data["joke"] if data["type"] == "single" else f"{data['setup']}\n{data['delivery']}"

    def save_as_txt(self, filename="jokes.txt"):
        with open(filename, "w", encoding="utf-8") as file:
            for joke in self.jokes:
                file.write(joke + "\n\n")
        return filename

    def save_as_pdf(self, filename="jokes.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for joke in self.jokes:
            pdf.multi_cell(0, 10, txt=joke + "\n", align="L")
        pdf.output(filename)
        return filename
