#estrutura

# 1) Bibliotecas

from shiny import App, ui
from faicons import icon_svg
from shinyswatch import theme

# 2) Dados



# 3) Interface do Usuário
app_ui = ui.page_navbar(  
    ui.nav_panel(
        "",
        ui.layout_columns(
            ui.navset_card_underline(
                ui.nav_panel("" , ui.output_plot("ipca_plt") , icon = icon_svg("chart-line") , value = "plt"),
                ui.nav_panel("" , ui.output_data_frame("ipca_tbl") , icon = icon_svg("table") , value = "tbl"),
                title = "Inflação (IPCA)",
                selected="plt"
            ),
            ui.navset_card_underline(
                ui.nav_panel("" , ui.output_plot("ipca_plt") , icon = icon_svg("chart-line") , value = "plt"),
                ui.nav_panel("" , ui.output_data_frame("ipca_tbl") , icon = icon_svg("table") , value = "tbl"),
                title = "Taxa de Câmbio (BRL/USD)",
                selected="plt"
            ),
        ),
        ui.layout_columns(
            ui.navset_card_underline(
                ui.nav_panel("" , ui.output_plot("ipca_plt") , icon = icon_svg("chart-line") , value = "plt"),
                ui.nav_panel("" , ui.output_data_frame("ipca_tbl") , icon = icon_svg("table") , value = "tbl"),
                title = "Atividade Econômica (PIB)",
                selected="plt"
            ),
            ui.navset_card_underline(
                ui.nav_panel("" , ui.output_plot("ipca_plt") , icon = icon_svg("chart-line") , value = "plt"),
                ui.nav_panel("" , ui.output_data_frame("ipca_tbl") , icon = icon_svg("table") , value = "tbl"),
                title = "Taxa de Câmbio (BRL/USD)",
                selected="Taxa de Juros (SELIC)"
            ),
        )
        
    ),
    title = ui.img(
        src = "https://aluno.analisemacro.com.br/download/59787/?tmstv=1712933415",
        height = 45
    ),
    fillable=True,
    fillable_mobile=True,
    theme = theme.superhero,
    window_title = "Painel de Previsao",
    sidebar = ui.sidebar(
        ui.markdown("Acompanhe as previsões automatizadas dos principais indicadores macroeconômicos do Brasil e simule cenários alternativos em um mesmo dashboard."),
        #Inputs
        ui.input_selectize(
                id = "modelo",
                label = ui.strong("Selecionar modelos:"),
                choices = ["IA" , "Ridge" , "Bayesian Ridge" , "Huber" , "Ensemble"],
                selected = ["IA" , "Ridge" , "Bayesian Ridge" , "Huber" , "Ensemble"],
                multiple = True,
                width = "100%",
                options = {"plugins": ["clear_button"]}
                ),
        ui.input_date(
            id = "inicio",
            label = ui.strong("Inicio do Gráfico:"),
            value = "2019-01-01",
            min = "2000-01-01",
            max = "2027-01-01",
            format = "mm/yyyy",
            startview = "year",
            language = "pt-BR",
            width = "100%"
        ),
        ui.input_checkbox(
                id = "ic",
                label = ui.strong("Intervalo de confiança"),
                value = True,
                width = "100%"
            ),

        ui.markdown(
            "Elaboração:ThomasKaiqueTTK | Data Science"
        )
    ),

)

# 4) Servidor
def server(input , output , session):
    ...
    
# 5) Shiny Dashboard
app = App(app_ui , server)


