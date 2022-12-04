import plotly.figure_factory as ff


class Map:

    def __init__(self, data):
        self.data = data

    def plot(self, year, state):
        print("In plot")
        df = self.data.query('Year == ' + str(year) + " & state_id == '" + str(state)+"'")

        fig = ff.create_choropleth(fips=df['county_fips'], values=df['corn_yield_per_acre'],
                                   scope=[state],
                                   binning_endpoints=[ 100, 125, 150,175, 200, 225, 250, 275, 300],
                                   county_outline={'color': 'rgb(0,0,0)', 'width': 1},
                                   state_outline={'color': 'rgb(0,0,0)', 'width': 1},
                                   round_legend_values=True,
                                   show_hover=True,
                                   show_state_data=True,
                                   legend_title='Corn Yield in bushel/acre',
                                   title='Corn Yield by County for ' + str(year) + ' in ' + state)
        fig.layout.template = None
        return fig
