import streamlit as st
import pandas as pd
import json
from src.api.service import API

class NBAFunctionsTeams():
    def __init__(self):
        self.api = API(base_url="http://192.168.0.252:8080")
    
    def all_teams(self):
        message = st.chat_message('assistant')
        message.write('Aqui são todos os Times da NBA')
        try:
            data_team = self.api.get_all_teams()
            df_team = pd.DataFrame(data_team)
            st.write(df_team)
        except json.JSONDecodeError:
            st.warning('Aguarde um momento! Se demorar, verifique se não inseriu algo errado.')

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
            st.warning('Aguarde um momento! Se demorar, verifique se não inseriu algo errado.')

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
            st.warning('Aguarde um momento! Se demorar, verifique se não inseriu algo errado.')

    def team_stats_years(self):
        message = st.chat_message('assistant')
        message.write('Aqui você encontra o Desempenho da equipe por Temporada, voce precisa inserir o ID do time.')
        teamYear_id = st.text_input('Digite o ID do Time sem pontos ou vírgula')
        try:
            data_teamStats_years = self.api.get_team_year_stats(teamYear_id)
            teamStats_columns = data_teamStats_years['resultSets'][0]['headers']
            teamStats_rowSet = data_teamStats_years['resultSets'][0]['rowSet']
            teamStats_df = pd.DataFrame(teamStats_rowSet, columns=teamStats_columns)
            st.write(teamStats_df)

            options_teamStats = st.multiselect("Filtrar por Temporada:", list(teamStats_df['YEAR']))
            if not options_teamStats:
                st.warning("Selecione uma ou mais Temporadas caso queira visualizar com Grafico.")
                return

            filtered_data = teamStats_df[teamStats_df['YEAR'].isin(options_teamStats)]
            if options_teamStats:
                filtered_data = teamStats_df[teamStats_df['YEAR'].isin(options_teamStats)]
                st.write(filtered_data)
            else:
                filtered_data = teamStats_df.copy()

            columns_x = [
                        'GP', 'WINS', 'LOSSES', 'WIN_PCT', 'CONF_RANK', 'DIV_RANK', 'PO_WINS',
                        'PO_LOSSES', 'CONF_COUNT', 'DIV_COUNT', 'FGM', 
                        'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 
                        'DREB', 'REB', 'AST', 'PF', 'STL', 'TOV', 'BLK', 'PTS', 'PTS_RANK'
                        ]

            if 'YEAR' in filtered_data.columns and 'TEAM_NAME' in filtered_data.columns:
                filtered_data['YEAR'] = filtered_data['YEAR'] + ' - ' + filtered_data['TEAM_NAME']
                chart_data = filtered_data[['YEAR'] + columns_x]
                chart_data.set_index('YEAR', inplace=True)
                st.bar_chart(chart_data)
 
        except json.JSONDecodeError:
            st.warning('Aguarde um momento! Se demorar, verifique se não inseriu algo errado.')
            