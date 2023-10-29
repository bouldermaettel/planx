from pathlib import Path
from itables.sample_dfs import get_dict_of_test_dfs
from itables.shiny import DT
from htmltools import HTML, div, head_content
import pandas as pd
from shiny import ui, render, App, req, reactive
import shinyswatch.theme
from sidebar import sidebar
from main_panel import main_panel

test = pd.read_json(Path(__file__).parent / "../new_test.json")
sponsors =  [name for index, (name, df) in enumerate(test.items())]
dfs = [df.to_dict() for index, (name, df) in enumerate(test.items())]
dfs_string = [str(df) for df in dfs]
# dfs = [df.from_dict() for df in dfs]
bools = [False]*len(sponsors)
new_df = pd.DataFrame([sponsors, dfs_string, bools]).T

countries = pd.read_json(Path(__file__).parent / "../countries.json")

print(type(new_df))
test_df = pd.DataFrame(dfs[0], index=[0]).T

# # construct new  df
df = pd.read_csv(Path(__file__).parent / "../test_table.csv")
df['summary'] = df.apply(lambda x: f"Number of Studies: {x['Number of Studies']} {ui.br()} Type: {x['Type']} <br> Never inspected: {x['Never inspected']} <br> New Sponsor: {x['New Sponsor']})", axis=1)
df_new = df[['Sponser', 'summary']]


app_ui = ui.page_fluid(
    # shinyswatch.theme.darkly(),
    # shinyswatch.theme.minty(),
    shinyswatch.theme.sketchy(),
    # shinyswatch.theme.superhero(),

    ui.panel_title( "PlanX", "Window title"), 
    ui.layout_sidebar(
    sidebar,
    main_panel,
    # ui.panel_main( ui.output_data_frame('original_results'))
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
    

    inputs = [input['see_details0'], input['see_details1'],input['see_details2']]

    [print(input) for input in inputs if input]

    @reactive.Effect
    @reactive.event(input['see_details0'])
    def _():
        m = ui.modal(
            f"This is a message from {i}",
            title="Modal dialog",
            easy_close=True,
            footer=None,
        )
        ui.modal_show(m)
    @output
    @render.image
    def image():
        from pathlib import Path

        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / "PlanX.png"), "width": "100px"}
        return img
    
    @output
    @render.data_frame
    def original_results():
        return render.DataTable(
            df_new,
            # escape=True,
            row_selection_mode="multiple",
            width="100%",
            height="100%",
            filters=True
            
        )
    


app = App(app_ui, server)