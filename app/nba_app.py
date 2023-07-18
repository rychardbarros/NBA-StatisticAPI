import streamlit as st
from app.utils.func_players import NBAFunctionsPlayers
from app.utils.func_teams import NBAFunctionsTeams

class NBAStatisticApp:
    def __init__(self):
        self.nba_functions_players = NBAFunctionsPlayers()
        self.nba_functions_teams = NBAFunctionsTeams()

    def run(self):
        st.title('NBA Statistic :basketball:')
        st.subheader('Aqui você pode comparar e analisar dados de jogadores e times da NBA!')
        
        option = st.selectbox(
            'Escolha uma Opção:',
            ('Descobrir ID Jogador', 'Dados Jogador', 'Jogador x Jogador', 'Detalhes Time',
             'Todos os Times e seu ID', 'Historico das Franquias','Desempenho de Equipe por Temporada','Draftados')
        )

        st.write('Selecionado:', option)

        if option == 'Descobrir ID Jogador':
            self.nba_functions_players.discover_player_id()

        elif option == 'Dados Jogador':
            self.nba_functions_players.player_data()

        elif option == 'Todos os Times e seu ID':
            self.nba_functions_teams.all_teams()

        elif option == 'Detalhes Time':
            self.nba_functions_teams.team_details()

        elif option == 'Jogador x Jogador':
            self.nba_functions_players.player_vs_player()

        elif option == 'Draftados':
            self.nba_functions_players.draft_players()

        elif option == 'Historico das Franquias':
            self.nba_functions_teams.franchise_history()

        elif option == 'Desempenho de Equipe por Temporada':
            self.nba_functions_teams.team_stats_years()
