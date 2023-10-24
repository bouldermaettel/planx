from pathlib import Path
from htmltools import HTML, div, head_content
import pandas as pd
from shiny import ui, render, App, req, reactive
import shinyswatch.theme
from config import sponser_types, study_phase

df = pd.read_csv(Path(__file__).parent / "test_table.csv")
css_file = Path(__file__).parent / "css" / "styles.css"

app_ui = ui.page_fluid(
    shinyswatch.theme.darkly(),
    ui.panel_title( "PlanX", "Window title"), 
    ui.layout_sidebar(
    ui.panel_sidebar(
        ui.include_css(css_file), 


    ui.input_slider("n", "Gewichtung einstellen", min=0, max=20, value=20),
    ui.input_date_range(id='date', label='Datum', start=None, end=None, min=None, max=None, format='yyyy-mm-dd', 
                        startview='month', weekstart=0, language='en', separator=' to ', width=None, autoclose=True),
    ui.row(ui.column(6,ui.HTML("<p>Sponser Typ:</p>")),
           ui.column(6, ui.input_selectize("state", "",sponser_types, multiple=True))),
    ui.row(ui.column(6,ui.HTML("<p>Studienphase:</p>")),
        ui.column(6, ui.input_selectize("state", "",study_phase, multiple=True))),       
    ui.row(ui.column(9,ui.HTML("<p>never inspected:</p>")),
    ui.column(3, ui.input_switch(id="never_inspected", label="", value=False, width='400px'))),      
    ui.row(ui.column(9,ui.HTML("<p>new sponser:</p>")),
    ui.column(3, ui.input_switch("new_sponser", "", False))),   
    ui.br(),
    ui.HTML("<h4>Listen Hochladen</p>"),

    ui.row(ui.column(4,ui.HTML("<h6>Studien SAP:</p>")),
    ui.column(4, ui.input_action_button('sap', "Sudien SAP", icon=None, width=None)),
    ui.column(4, ui.input_action_button('sap', "Sudien SAP", icon=None, width=None))), 
    ui.HTML('<br>'),
    ui.input_checkbox_group("studies","",{
            "sap": ui.span("SAP Studien", style="color: #FF0000;"),
            "ethik": ui.span("Ethikkommission", style="color: #00AA00;"),
            "triggers": ui.span("Triggers aus SAP", style="color: #0000AA;"),
            "abwesend": ui.span("Abwesenheiten", style="color: white;")
        }, width='100%'), 
    

           ),
    ui.panel_main(    
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

app = App(app_ui, server)