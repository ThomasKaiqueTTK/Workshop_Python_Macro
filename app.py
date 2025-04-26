#estrutura

# 1) Bibliotecas

from shiny import App, ui, render
from faicons import icon_svg
from shinyswatch import theme
import pandas as pd
import plotnine as p9
from mizani import breaks

# 2) Dados
ipca = pd.read_parquet("previsao/ipca.parquet")
cambio = pd.read_parquet("previsao/cambio.parquet")
pib = pd.read_parquet("previsao/pib.parquet")
selic = pd.read_parquet("previsao/selic.parquet")


datas = {
    "min": pib.index.min().date(),
    "max": selic.index.max().date(),
    "value": pib.index[-36].date()
}

modelos = (
    pd.concat([
        ipca,
        cambio,
        pib,
        selic
    ])
    .query("Tipo not in ['Câmbio' , 'IPCA' , 'SELIC' , 'PIB']")
    .Tipo
    .unique()
)


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
                ui.nav_panel("" , ui.output_plot("cambio_plt") , icon = icon_svg("chart-line") , value = "plt"),
                ui.nav_panel("" , ui.output_data_frame("cambio_tbl") , icon = icon_svg("table") , value = "tbl"),
                title = "Taxa de Câmbio (BRL/USD)",
                selected="plt"
            ),
        ),
        ui.layout_columns(
            ui.navset_card_underline(
                ui.nav_panel("" , ui.output_plot("pib_plt") , icon = icon_svg("chart-line") , value = "plt"),
                ui.nav_panel("" , ui.output_data_frame("pib_tbl") , icon = icon_svg("table") , value = "tbl"),
                title = "Atividade Econômica (PIB)",
                selected="plt"
            ),
            ui.navset_card_underline(
                ui.nav_panel("" , ui.output_plot("selic_plt") , icon = icon_svg("chart-line") , value = "plt"),
                ui.nav_panel("" , ui.output_data_frame("selic_tbl") , icon = icon_svg("table") , value = "tbl"),
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
                choices = modelos,
                selected = modelos,
                multiple = True,
                width = "100%",
                options = {"plugins": ["clear_button"]}
                ),
        ui.input_date(
            id = "inicio",
            label = ui.strong("Inicio do Gráfico:"),
            value = datas["value"],
            min = datas["min"],
            max = datas["max"],
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
    
    @render.plot
    def ipca_plt():
        y = "IPCA"
        modelos1 = [y] + list([input.modelo()])
        modelos2 = ipca.query("Tipo != @y").Tipo.unique().tolist()
        df = (ipca
             .reset_index()
             .assign(Tipo = lambda x: pd.Categorical(x.Tipo,[y] + modelos2))
             .query("Tipo in @modelos1")
        )
        plt = (
            p9.ggplot(ipca.reset_index()) +
            p9.aes(x = "index" , y = "Valor" , color ="Tipo") +
            p9.geom_line() + 
            p9.scale_x_date(date_breaks="1 year", date_labels="%Y") +
            p9.scale_y_continuous(breaks=breaks.breaks_extended(n = 6)) +
            p9.scale_color_manual(
                                values = {
                                    y: "black", 
                                    "IA": "green",
                                    "Ridge": "blue",
                                    "Bayesian Ridge": "orange",
                                    "Huber": "red",
                                    "Ensemble": "brown"
                                }
            ) + 
            p9.labs(
                y = "Var. %",
                x = "",
                color = ""
            ) +
            p9.theme(legend_position="bottom")
        )
    
# 5) Shiny Dashboard
app = App(app_ui , server)


