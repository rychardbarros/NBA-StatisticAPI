import streamlit as st
import pandas as pd
import json
from src.api import API

class NBAStatisticApp:
    def __init__(self):
        self.api = API(base_url="http://localhost:5000")

    def run(self):
        st.title('NBA Statistic :basketball:')
        st.subheader('Aqui você pode comparar e analisar dados de jogadores e times da NBA!')
        
        option = st.selectbox(
            'Escolha uma Opção:',
            ('Descobrir ID Jogador', 'Dados Jogador', 'Jogador x Jogador', 'Detalhes Time',
             'Todos os Times e seu ID', 'Historico das Franquias','Desempenho de Equipe por Temp','Draftados')
        )

        st.write('Selecionado:', option)

        if option == 'Descobrir ID Jogador':
            self.discover_player_id()

        elif option == 'Dados Jogador':
            self.player_data()

        elif option == 'Todos os Times e seu ID':
            self.all_teams()

        elif option == 'Detalhes Time':
            self.team_details()

        elif option == 'Jogador x Jogador':
            self.player_vs_player()

        elif option == 'Draftados':
            self.draft_players()

        elif option == 'Historico das Franquias':
            self.franchise_history()

        elif option == 'Desempenho de Equipe por Temp':
            self.team_stats_years()

    def discover_player_id(self):
        message = st.chat_message('assistant')
        message.write('O id serve para você verificar as estatísticas de um jogador quando escolher uma das outras opções')
        prompt_player = st.text_input('Digite aqui o Nome do Jogador')
        st.write(f'Resposta: {prompt_player}')
        try:
            data = self.api.get_player_by_name(prompt_player)
            df = pd.DataFrame(data)
            st.write(df)
        except json.JSONDecodeError:
            st.write('Aguarde um momento!, Se demorar verifique se inseriu algo Errado.')

    def player_data(self):
        message = st.chat_message('assistant')
        message.write('Aqui são todos os Dados da carreira de um jogador')
        player_status = st.text_input('Digite o ID do Jogador sem pontos ou vírgula')
        st.write(f'Resposta: {player_status}')
        try:
            data_player = self.api.get_player_career(player_status)
            result_set = data_player['resultSets'][0]
            columns = result_set['headers']
            df_player = pd.DataFrame(result_set['rowSet'], columns=columns)
            st.write(df_player)

            columns_x = [
                'PTS', 'GP', 'MIN', 'FGM', 'FGA',
                'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM',
                'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB',
                'AST', 'STL', 'BLK', 'TOV', 'PF'
            ]

            if 'SEASON_ID' in df_player.columns and 'TEAM_ABBREVIATION' in df_player.columns:
                df_player['SEASON_TEAM'] = df_player['SEASON_ID'] + ' - ' + df_player['TEAM_ABBREVIATION']
                chart_data = df_player[['SEASON_TEAM'] + columns_x]
                chart_data.set_index('SEASON_TEAM', inplace=True)
                st.bar_chart(chart_data)
            else:
                st.write('As colunas necessárias ("SEASON_ID" e "TEAM_ABBREVIATION") não estão presentes nos dados do jogador.')
        except json.JSONDecodeError:
            st.write('Aguarde um momento! Se demorar, verifique se não inseriu algo errado.')

    def all_teams(self):
        message = st.chat_message('assistant')
        message.write('Aqui são todos os Times da NBA')
        try:
            data_team = self.api.get_all_teams()
            df_team = pd.DataFrame(data_team)
            st.write(df_team)
        except json.JSONDecodeError:
            st.write('Aguarde um momento! Se demorar, verifique se não inseriu algo errado.')

    def team_details(self):
        message = st.chat_message('assistant')
        message.write('Aqui estão alguns detalhes sobre o Time. Alguns Campos podem está vazios por falta de Informações Especificas')
        team_details_id = st.text_input('Digite o ID do Time sem pontos ou vírgula')
        st.write(f'Resposta: {team_details_id}')
        try:
            data_team_details = self.api.get_team_details(team_details_id)
            for table in data_team_details['resultSets']:
                table_name = table['name']
                headers = table['headers']
                rows = table['rowSet']
                df = pd.DataFrame(rows, columns=headers)
                df = df.dropna(axis=1, how='all')
                st.write(f'Campo: {table_name}')
                st.write(df)
        except json.JSONDecodeError:
            st.write('Aguarde um momento! Se demorar, verifique se não inseriu algo errado.')

    def player_vs_player(self):
        message = st.chat_message('assistant')
        message.write('Aqui voce vai encontrar Dados de Jogador x Jogador. Alguns Campos podem está vazios por falta de Informações Especificas')
        player_id = st.text_input('Digite o ID do primeiro jogador sem pontos ou vírgula')
        player_vs_id = st.text_input('Digite o ID do segundo jogador sem pontos ou vírgula')
        st.write(f'Resposta: Primeiro ID:{player_id} | Segundo ID:{player_vs_id}')
        try:
            comparison = self.api.get_player_vs_player(player_id, player_vs_id)
            for table in comparison['resultSets']:
                table_name = table['name']
                headers = table['headers']
                rows = table['rowSet']
                # Substituir campos vazios por uma string vazia ("")
                rows_cleaned = [[cell if cell is not None else "" for cell in row] for row in rows]
                df = pd.DataFrame(rows_cleaned, columns=headers)
                st.write(f'Campo: {table_name}')
                st.write(df)
        except json.JSONDecodeError:
            st.write('Aguarde um momento! Se demorar, verifique se não inseriu algo errado.')

    def draft_players(self):
        message = st.chat_message('assistant')
        message.write('Aqui você encontra todos os draftados da NBA')
        try:
            data_draft = self.api.get_all_draft()
            draft_list = data_draft['resultSets'][0]['rowSet']
            draft_columns = data_draft['resultSets'][0]['headers']
            df_draft = pd.DataFrame(draft_list, columns=draft_columns)
            options = st.multiselect("Filtre por Nome:", list(df_draft['PLAYER_NAME']))
            if options:
                filtered_data = df_draft[df_draft['PLAYER_NAME'].isin(options)]
                st.write(filtered_data)
            st.write(df_draft)
        except json.JSONDecodeError:
            st.write('Aguarde um momento! Se demorar, verifique se não inseriu algo errado.')

    def franchise_history(self):
        message = st.chat_message('assistant')
        message.write('Aqui você encontra o Histórico de todas as franquias da NBA')
        try:
            data_franchise = self.api.get_all_franchise()
            franchise_header = data_franchise['resultSets'][0]['headers']
            franchise_rowset = data_franchise['resultSets'][0]['rowSet']
            df_franchise = pd.DataFrame(franchise_rowset, columns=franchise_header)

            options_franchise = st.multiselect("Filtrar por nome do Time:", list(df_franchise['TEAM_NAME']))
            selected_columns = st.multiselect("Selecione as colunas:", ['Geral'] + [
                'YEARS', 'GAMES', 'WINS',
                'LOSSES', 'WIN_PCT', 'PO_APPEARANCES',
                'DIV_TITLES', 'CONF_TITLES', 'LEAGUE_TITLES'
            ])

            if options_franchise:
                filtered_franchise = df_franchise[df_franchise['TEAM_NAME'].isin(options_franchise)]
            else:
                filtered_franchise = df_franchise

            if 'Geral' in selected_columns:
                selected_columns = [
                    'TEAM_NAME', 'YEARS', 'GAMES', 'WINS',
                    'LOSSES', 'WIN_PCT', 'PO_APPEARANCES',
                    'DIV_TITLES', 'CONF_TITLES', 'LEAGUE_TITLES'
                ]
                filtered_franchise = filtered_franchise[selected_columns]
                st.write(filtered_franchise)
                st.bar_chart(filtered_franchise.set_index('TEAM_NAME'))

            else:
                if selected_columns:
                    selected_columns.insert(0, 'TEAM_NAME')
                    filtered_franchise = filtered_franchise[selected_columns]
                    st.write(filtered_franchise)
                    filtered_franchise = filtered_franchise.set_index('TEAM_NAME')
                    for column in selected_columns:
                        if column != 'TEAM_NAME':
                            st.subheader(column)
                            st.bar_chart(filtered_franchise[column])
                else:
                    st.write(filtered_franchise)

        except json.JSONDecodeError:
            st.write('Aguarde um momento! Se demorar, verifique se não inseriu algo errado.')

    def team_stats_years():
        st.write('em prod')


# TODO: Criar função para tratar dados e gerar grafico das estatistica do time 

app = NBAStatisticApp()
app.run()
