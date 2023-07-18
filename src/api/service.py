import requests

class API():
    def __init__(self, base_url):
        self.base_url = base_url

    def get_player_by_name(self, player_name):
        url = f"{self.base_url}/player/name/{player_name}"
        response = requests.get(url)
        data = response.json()
        return data

    def get_player_career(self, player_id):
        url = f"{self.base_url}/player/{player_id}"
        response = requests.get(url)
        data = response.json()
        return data

    def get_player_vs_player(self, player_id, player_vs_id):
        url = f"{self.base_url}/player/{player_id}/vs/{player_vs_id}"
        response = requests.get(url)
        data = response.json()
        return data

    def get_all_teams(self):
        url = f"{self.base_url}/team/all"
        response = requests.get(url)
        data = response.json()
        return data

    def get_team_details(self, team_id):
        url = f"{self.base_url}/team/details/{team_id}"
        response = requests.get(url)
        data = response.json()
        return data

    def get_all_draft(self):
        url = f'{self.base_url}/draft/all'
        response = requests.get(url)
        data = response.json()
        return data

    def get_all_franchise(self):
        url = f'{self.base_url}/franchise/all'
        response = requests.get(url)
        data = response.json()
        return data

    def get_team_year_stats(self, team_year_stats):
        url = f'{self.base_url}/team/stats/{team_year_stats}'
        response = requests.get(url)
        data = response.json()
        return data
