from shiny import ui, render, App, req, reactive
from pathlib import Path
from config import sponser_types, study_phase
css_file = Path(__file__).parent  / "../css" / "styles.css"



sidebar =   ui.panel_sidebar(
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
            ui.row(ui.column(6, ui.input_selectize("state", "Sponser Filter",sponser_types, multiple=True)),
                    ui.column(6, ui.input_selectize("state", "Study Filter",study_phase, multiple=True))),

            ui.row(ui.column(6,ui.input_file("sap", "SAP Studien", accept=[".xlsx"], multiple=False)),
                            #  ui.column(6,ui.input_checkbox("header1", "Header:", True))
                             ),
            ui.row(ui.column(6,ui.input_file("ethik", "Ethikkommission", accept=[".xlsx"], multiple=False)),
                            #  ui.column(6,ui.input_checkbox("header1", "Header:", True))
                             ),
            ui.row(ui.column(6,ui.input_file("triggers", "Triggers aus SAP", accept=[".xlsx"], multiple=False)),
                            #  ui.column(6,ui.input_checkbox("header1", "Header:", True))
                             ),
            ui.row(ui.column(6,ui.input_file("abwesenheiten", "Abwesenheiten", accept=[".xlsx"], multiple=False)),
                            #  ui.column(6,ui.input_checkbox("header1", "Header:", True))
                             ),
            
            # ui.input_checkbox_group("studies","",{
            #         "sap": ui.span("SAP Studien", style="color: #FF0000;"),
            #         "ethik": ui.span("Ethikkommission", style="color: #00AA00;"),
            #         "triggers": ui.span("Triggers aus SAP", style="color: #0000AA;"),
            #         "abwesend": ui.span("Abwesenheiten", style="color: darkgrey;")
            #     }, width='100%'),
           )