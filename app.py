from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


DATA_PATH = Path("data") / "sales_output.csv"
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")


def load_sales_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    return data


sales_data = load_sales_data()
region_options = [
    {"label": "north", "value": "north"},
    {"label": "east", "value": "east"},
    {"label": "south", "value": "south"},
    {"label": "west", "value": "west"},
    {"label": "all", "value": "all"},
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
        "background": "radial-gradient(circle at top, #F8FAFC 0%, #E0F2FE 45%, #EDE9FE 100%)",
        "padding": "40px 20px 56px",
    },
    children=[
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "background": "linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.98) 100%)",
                "borderRadius": "24px",
                "boxShadow": "0 24px 70px rgba(15, 23, 42, 0.16)",
                "padding": "34px",
                "border": "1px solid rgba(148, 163, 184, 0.22)",
                "backdropFilter": "blur(10px)",
            },
            children=[
                html.Div(
                    children=[
                        html.Div(
                            "Soul Foods Insight Dashboard",
                            style={
                                "display": "inline-block",
                                "marginBottom": "14px",
                                "padding": "8px 14px",
                                "borderRadius": "999px",
                                "background": "linear-gradient(90deg, #0F62FE 0%, #7C3AED 100%)",
                                "color": "white",
                                "fontSize": "0.82rem",
                                "fontWeight": "700",
                                "letterSpacing": "0.08em",
                                "textTransform": "uppercase",
                            },
                        ),
                        html.H1(
                            "Soul Foods Pink Morsel Sales Visualiser",
                            style={
                                "marginBottom": "8px",
                                "fontSize": "clamp(2rem, 4vw, 3.2rem)",
                                "lineHeight": "1.08",
                                "color": "#0F172A",
                                "maxWidth": "14ch",
                            },
                        ),
                        html.P(
                            "Compare daily Pink Morsel sales before and after the 15 January 2021 price increase.",
                            style={
                                "marginTop": "0",
                                "marginBottom": "28px",
                                "fontSize": "1.05rem",
                                "color": "#475569",
                                "maxWidth": "760px",
                                "lineHeight": "1.6",
                            },
                        ),
                    ]
                ),
                html.Div(
                    "Choose a region to focus the chart. Sales are aggregated by day.",
                    style={
                        "marginBottom": "10px",
                        "fontSize": "0.95rem",
                        "fontWeight": "600",
                        "color": "#334155",
                    },
                ),
                dcc.RadioItems(
                    id="region-filter",
                    options=region_options,
                    value="all",
                    inline=True,
                    labelStyle={
                        "display": "inline-flex",
                        "alignItems": "center",
                        "gap": "8px",
                        "padding": "10px 14px",
                        "marginRight": "10px",
                        "marginBottom": "12px",
                        "borderRadius": "999px",
                        "border": "1px solid #CBD5E1",
                        "background": "white",
                        "boxShadow": "0 8px 20px rgba(15, 23, 42, 0.06)",
                        "cursor": "pointer",
                        "color": "#1E293B",
                        "fontWeight": "600",
                    },
                    inputStyle={
                        "accentColor": "#0F62FE",
                        "transform": "scale(1.05)",
                    },
                    style={
                        "marginBottom": "28px",
                        "display": "flex",
                        "flexWrap": "wrap",
                    },
                ),
                dcc.Graph(
                    id="sales-chart",
                    figure=build_figure("all"),
                    config={"displayModeBar": False, "responsive": True},
                    style={
                        "borderRadius": "18px",
                        "overflow": "hidden",
                        "boxShadow": "inset 0 0 0 1px rgba(148, 163, 184, 0.2)",
                        "background": "#FFFFFF",
                    },
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