from pathlib import Path
from itables.sample_dfs import get_dict_of_test_dfs
from itables.shiny import DT
from htmltools import HTML, div, head_content
import pandas as pd
from shiny import ui, render, App, req, reactive
import shinyswatch.theme
# from config import sponser_types, study_phase
from sidebar import sidebar

df = pd.read_csv(Path(__file__).parent / "test_table.csv")
countries = pd.read_json(Path(__file__).parent / "countries.json")
test = pd.read_json(Path(__file__).parent / "new_test.json")
css_file = Path(__file__).parent  / "css" / "styles.css"

# countries['action'] = ui.input_action_button(id, label, *, icon=None, width=None, **kwargs)

app_ui = ui.page_fluid(
    shinyswatch.theme.darkly(),
    ui.panel_title( "PlanX", "Window title"), 
    ui.layout_sidebar(
    sidebar,
    ui.panel_main(   


    [ui.row(ui.column(2,ui.HTML(f"<h3> {name} <br> <br> <h6>"),
                      ui.input_action_button(f'see_details{index}', f'See details', icon="🤩 ")),
                    #   ui.output_image("image")), 
            ui.column(3,ui.HTML(DT(df, head_content=False)))) for index, (name, df) in enumerate(test.items())],


        # Display the different tables in different tabs
    # ui.navset_tab(
    #     *[ui.nav(name, ui.HTML(DT(df))) for name, df in get_dict_of_test_dfs().items()]
    # ),
       ui.navset_tab(
        *[ui.nav('test', ui.HTML(DT(countries)))]
    ),
    ui.include_css(css_file),
    ui.output_table("test_table"),
    ui.output_ui("never_inspected"),
    ui.output_ui("selection_upload"),
    ui.output_text("value"),
    ),
        
))

def server(input, output, session):
    @output
    @render.table
    def test_table():
        return df
    
    @output
    @render.ui
    def never_inspected():
        return input.never_inspected()
    
    @output
    @render.ui
    def selection_upload():
        req(input.studies())
        return ", ".join(input.studies())
    
    studies = reactive.Value(0)

    @reactive.Effect
    @reactive.event(input.studies)
    def _():
        newstudies = input.studies()
        studies.set(newstudies)

    @output
    @render.text
    def value():
        return str(studies.get()) # is a tuple
    @output
    @render.image
    def image():
        from pathlib import Path

        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "PlanX.png"), "width": "100px"}
        return img

app = App(app_ui, server)