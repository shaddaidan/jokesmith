# joke_app.py
import requests
from fpdf import FPDF
import streamlit as st

class JokeFetcher:
    def __init__(self, category="Any", joke_type="single", amount=1, lang="en"):
        self.base_url = "https://v2.jokeapi.dev/joke"
        self.category = category
        self.joke_type = joke_type
        self.amount = amount
        self.lang = lang
        self.jokes = []

    def fetch_jokes(self):
        url = f"{self.base_url}/{self.category}?amount={self.amount}&type={self.joke_type}&lang={self.lang}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if self.amount == 1:
                self.jokes = [self._format_joke(data)]
            else:
                self.jokes = [self._format_joke(j) for j in data.get("jokes", [])]
        except requests.RequestException as e:
            self.jokes = [f"Error fetching joke: {e}"]

    def _format_joke(self, data):
        if data.get("error"):
            return "API Error: Could not retrieve joke."
        if data["type"] == "single":
            return data["joke"]
        else:
            return f"{data['setup']}\n{data['delivery']}"

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
