import streamlit as st
import pandas as pd
import json
from src.api.service import API

class NBAFunctionsPlayers():
    def __init__(self):
        self.api = API(base_url="http://localhost:5000")

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