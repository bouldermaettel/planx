from pathlib import Path
import shiny.experimental as exp
from itables.sample_dfs import get_dict_of_test_dfs
from itables.shiny import DT
from htmltools import HTML, div, head_content
import pandas as pd
from shiny import ui, render, App, req, reactive

df = pd.read_csv(Path(__file__).parent / "../test_table.csv")
countries = pd.read_json(Path(__file__).parent / "../countries.json")
test = pd.read_json(Path(__file__).parent / "../new_test.json")
sponsors =  [name for index, (name, df) in enumerate(test.items())]
dfs = [df.to_dict() for index, (name, df) in enumerate(test.items())]
dfs_string = [str(df) for df in dfs]
print(type(dfs[0]))
bools = [False]*len(sponsors)
new_df = pd.DataFrame([sponsors, dfs_string, bools]).T
print(new_df)
# df_nested = pd.DataFrame(df, head_content=False) for index, (name, df) in enumerate(test.items())])))
css_file = Path(__file__).parent  / "../css" / "styles.css"


items = [exp.ui.accordion_panel(ui.HTML(f"Section {letter} <br> test"), ui.HTML(f"Some narrative for section {letter} <br> tets <br> tets <br> tets <br> tets <br> tets <br> tets <br> tets")) for letter in "ABCDE"]
# # construct new  df
df = pd.read_csv(Path(__file__).parent / "../test_table.csv")
df['summary'] = df.apply(lambda x: f"Number of Studies: {x['Number of Studies']} <br> Type: {x['Type']} <br> Never inspected: {x['Never inspected']} <br> New Sponsor: {x['New Sponsor']}", axis=1)
df['choose'] = [True]*len(df)
df_new = df[['Sponser', 'summary', 'choose']]


main_panel =    ui.panel_main(  
                ui.navset_tab( 
                    ui.nav('Sponsors',
                        [ui.row(ui.column(2,ui.HTML(f"<h3> <a href=\"https://en.wikipedia.org/wiki/Aruba\">{name}</a> <br> <br> <h6>"),
                            ui.input_checkbox(f'see_details{index}', f'See details')),
                            # ui.output_image("image")), 
                            ui.column(3,ui.HTML(DT(df, head_content=False)))) for index, (name, df) in enumerate(test.items())]),

                    ui.nav('Centers',
                        [ui.row(ui.column(2,ui.HTML(f"<h3> <a href=\"https://en.wikipedia.org/wiki/Aruba\">{name}</a> <br> <br> <h6>"),
                            ui.input_action_button(f'see_details{index}', f'See details', icon="🤩 ")),
                            ui.column(3,ui.HTML(DT(df, head_content=False)))) for index, (name, df) in enumerate(test.items())]),
                
                    *[ui.nav('test', ui.HTML(DT(countries)))],

                    ui.nav('DT Test', ui.HTML(DT(df_new))),


                    ui.nav('Accordion Test', exp.ui.accordion(*items, id="acc")),
                    
                    

                    # ui.nav('DT tst3', ui.output_data_frame('original_results')),
                    # 
                    ui.nav('DT tst3', ui.output_data_frame('original_results')))
                    
                    ),

                    
                    # ui.include_css(css_file),)
                    # ui.output_table("test_table"),
                    # ui.output_ui("never_inspected"),
                    # ui.output_ui("selection_upload"),
                    # ui.output_text("value"))