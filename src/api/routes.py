from flask import Flask, jsonify
from nba_api.stats.endpoints import playercareerstats, teamdetails, playervsplayer, drafthistory, franchisehistory, teamyearbyyearstats
from nba_api.stats.static import players, teams

app = Flask(__name__)

@app.route('/player/<id>', methods=['GET'])
def player_career(id):
    player_id = id 
    career_get = playercareerstats.PlayerCareerStats(player_id=player_id) 
    result = career_get.get_json()
    return result

@app.route('/player/name/<id>', methods=['GET'])
def player_id(id):
    player = id
    player_get = players.find_players_by_full_name(player)
    return jsonify(player_get)

@app.route('/player/<id>/vs/<vs_id>', methods=['GET'])
def player_vs_player(id,vs_id):
    player_comparison = id
    player_vs = vs_id
    result_comparison_get = playervsplayer.PlayerVsPlayer(player_id=player_comparison, vs_player_id=player_vs)
    result_comparison = result_comparison_get.get_json()
    return result_comparison

@app.route('/team/name/<id>', methods=['GET'])
def teams_id(id):
    team = id
    team_get = teams.find_teams_by_full_name(team)
    return jsonify(team_get)

@app.route('/team/all', methods=['GET'])
def teams_all():
    team_all = teams.get_teams()
    return jsonify(team_all)

@app.route('/team/details/<id>', methods=['GET'])
def team_details(id):
    details_id = id
    details_get = teamdetails.TeamDetails(team_id=details_id)
    result_team = details_get.get_json()
    return result_team

@app.route('/draft/all', methods=['GET'])
def draft():
    draft_get = drafthistory.DraftHistory()
    draft_result = draft_get.get_json()
    return draft_result

@app.route('/franchise/all', methods=['GET'])
def franchise():
    franchise_get = franchisehistory.FranchiseHistory()
    franchise_result = franchise_get.get_json()
    return franchise_result

@app.route('/team/stats/<id>', methods=['GET'])
def team_year_stats(id):
    team_year_get = teamyearbyyearstats.TeamYearByYearStats(team_id=id)
    team_year_result = team_year_get.get_json()
    return team_year_result

if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.252', port=8080)
