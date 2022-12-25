#!/usr/bin/env python

import requests
import json
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button
from textual.containers import Vertical, Container, Horizontal
from rich.syntax import Syntax

class RESTClient():

    def __init__(self):
        self.API = 'http://192.168.3.21'
    
    def make_url(self, api, path):
        return f'{api}{path}'

    def perform(self, path):
        url = self.make_url(self.API, path)
        print(url)
        try:
            if path == '/led':
                response = requests.get(url)
            else:
                response = requests.post(url)

            if response.status_code == 200:
                return json.dumps(json.loads(response.content), indent=4)
            else:
                return '{}'
        except:
            print('Request error')
            return ''

    def status(self):
        return self.perform('/led')

    def turn_on(self):
        return self.perform('/led/on')

    def turn_off(self):
        return self.perform('/led/off')
        
    def toggle(self):
        return self.perform('/led/toggle')
        
    def change(self):
        return self.perform('/led/change')

class PicoledApp(App):
    BINDINGS = []
    CSS_PATH = 'picoled_app.css'

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder = "http://192.168.3.21", id = "address")
        yield Horizontal(
            Vertical(
                Button("Get Status", id = "btn-status"),
                Button("Turn On", id = "btn-on"),
                Button("Turn Off", id = "btn-off"),
                Button("Toggle", id = "btn-toggle"),
                Button("Change Program", id = "btn-change"),
                classes='buttons'),
            Vertical(
                Static(id="response", expand=True),
                classes='column'))
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        client = RESTClient()
        api = self.query_one("#address").value.strip()

        if not (api == ''):
            client.API = api

        response = ''
        if event.button.id == "btn-status":
            response = client.status()
        elif event.button.id == "btn-on":
            response = client.turn_on()
        elif event.button.id == "btn-off":
            response = client.turn_off()
        elif event.button.id == "btn-toggle":
            response = client.toggle()
        elif event.button.id == "btn-change":
            response = client.change()

        syntax = Syntax(response, 'json', line_numbers=True)
        self.query_one('#response').update(syntax)

if __name__ == "__main__":
    app = PicoledApp()
    app.run()
