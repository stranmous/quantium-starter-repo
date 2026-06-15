from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


DATA_PATH = Path("data") / "sales_output.csv"
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")


def load_sales_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    data["Region"] = data["Region"].str.title()
    return data


sales_data = load_sales_data()
region_options = [
    {"label": "All regions", "value": "all"},
    *(
        {"label": region, "value": region}
        for region in sorted(sales_data["Region"].unique())
    ),
]

app = Dash(__name__)
app.title = "Soul Foods Pink Morsel Sales Visualiser"


def build_figure(region_value: str):
    filtered = sales_data if region_value == "all" else sales_data[sales_data["Region"] == region_value]
    daily_sales = (
        filtered.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    figure = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        markers=True,
        title=None,
    )
    figure.update_traces(line={"color": "#0F62FE", "width": 3}, marker={"size": 5})
    figure.update_layout(
        template="plotly_white",
        hovermode="x unified",
        margin={"l": 48, "r": 24, "t": 24, "b": 48},
        paper_bgcolor="#F8FAFC",
        plot_bgcolor="#F8FAFC",
        font={"family": "Arial, sans-serif", "color": "#1F2937"},
    )
    figure.update_xaxes(title_text="Date", gridcolor="#E5E7EB")
    figure.update_yaxes(title_text="Sales", gridcolor="#E5E7EB")
    figure.add_vline(
        x=PRICE_INCREASE_DATE,
        line_width=2,
        line_dash="dash",
        line_color="#C2410C",
    )
    figure.add_annotation(
        x=PRICE_INCREASE_DATE,
        y=1,
        xref="x",
        yref="paper",
        text="Price increase<br>15 Jan 2021",
        showarrow=False,
        yanchor="bottom",
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#C2410C",
        borderwidth=1,
        font={"color": "#7C2D12"},
    )
    return figure


app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "background": "linear-gradient(180deg, #F8FAFC 0%, #EEF2FF 100%)",
        "padding": "40px 20px",
    },
    children=[
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "background": "rgba(255, 255, 255, 0.92)",
                "borderRadius": "20px",
                "boxShadow": "0 18px 50px rgba(15, 23, 42, 0.12)",
                "padding": "32px",
                "backdropFilter": "blur(8px)",
            },
            children=[
                html.Div(
                    children=[
                        html.H1(
                            "Soul Foods Pink Morsel Sales Visualiser",
                            style={
                                "marginBottom": "8px",
                                "fontSize": "2.2rem",
                                "lineHeight": "1.15",
                                "color": "#0F172A",
                            },
                        ),
                        html.P(
                            "Compare daily Pink Morsel sales before and after the 15 January 2021 price increase.",
                            style={
                                "marginTop": "0",
                                "marginBottom": "24px",
                                "fontSize": "1.02rem",
                                "color": "#475569",
                                "maxWidth": "760px",
                            },
                        ),
                    ]
                ),
                html.Label(
                    "Region",
                    htmlFor="region-filter",
                    style={
                        "display": "block",
                        "marginBottom": "8px",
                        "fontWeight": "600",
                        "color": "#334155",
                    },
                ),
                dcc.Dropdown(
                    id="region-filter",
                    options=region_options,
                    value="all",
                    clearable=False,
                    style={"marginBottom": "24px"},
                ),
                dcc.Graph(
                    id="sales-chart",
                    figure=build_figure("all"),
                    config={"displayModeBar": False},
                ),
            ],
        )
    ],
)


@app.callback(Output("sales-chart", "figure"), Input("region-filter", "value"))
def update_chart(region_value: str):
    return build_figure(region_value)


if __name__ == "__main__":
    app.run(debug=True)