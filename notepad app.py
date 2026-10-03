# ============================================
# Olympic Games Data Analytics Dashboard
# 1896–2024
# ============================================

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# --------------------------------------------
# 1. Load the cleaned Olympic dataset
# --------------------------------------------

df = pd.read_csv("data/cleaned_olympics.csv")


# --------------------------------------------
# 2. Clean Medal column
# --------------------------------------------

df["Medal"] = df["Medal"].astype(str).str.strip()


# --------------------------------------------
# 3. Keep only actual medals
# --------------------------------------------

medal_df = df[
    df["Medal"].isin(["Gold", "Silver", "Bronze"])
].copy()


# --------------------------------------------
# 4. Create Dash application
# --------------------------------------------

app = Dash(__name__)


# --------------------------------------------
# 5. Get countries with actual medals
# --------------------------------------------

countries = sorted(
    medal_df["Team"].dropna().unique()
)


# --------------------------------------------
# 6. Dashboard Layout
# --------------------------------------------

app.layout = html.Div(
    [

        html.H1(
            "Olympic Games Data Analytics (1896–2024)",
            style={
                "textAlign": "center",
                "fontSize": "36px"
            }
        ),

        html.H3(
            "Interactive Country-wise Medal Dashboard",
            style={
                "textAlign": "center",
                "color": "#444444"
            }
        ),

        # Country selector
        html.Div(
            [

                html.Label(
                    "Select a Country:",
                    style={
                        "fontWeight": "bold",
                        "fontSize": "18px"
                    }
                ),

                dcc.Dropdown(
                    id="country-dropdown",

                    options=[
                        {
                            "label": country,
                            "value": country
                        }
                        for country in countries
                    ],

                    value=countries[0],

                    clearable=False

                )

            ],

            style={
                "width": "65%",
                "margin": "20px auto"
            }
        ),

        # Medal distribution
        dcc.Graph(
            id="medal-chart"
        ),

        # Medal trend
        dcc.Graph(
            id="trend-chart"
        )

    ],

    style={
        "backgroundColor": "#F7F9FC",
        "minHeight": "100vh",
        "padding": "20px"
    }
)


# --------------------------------------------
# 7. Callback
# --------------------------------------------

@app.callback(
    [
        Output("medal-chart", "figure"),
        Output("trend-chart", "figure")
    ],

    Input(
        "country-dropdown",
        "value"
    )
)


def update_charts(selected_country):

    # ----------------------------------------
    # Filter selected country
    # ----------------------------------------

    filtered_df = medal_df[
        medal_df["Team"] == selected_country
    ].copy()


    # ----------------------------------------
    # Different colors for medals
    # ----------------------------------------

    medal_colors = {
        "Gold": "#FFD700",
        "Silver": "#A9A9A9",
        "Bronze": "#CD7F32"
    }


    # ----------------------------------------
    # Medal Distribution
    # ----------------------------------------

    medal_data = (
        filtered_df["Medal"]
        .value_counts()
        .reindex(
            ["Gold", "Silver", "Bronze"],
            fill_value=0
        )
        .reset_index()
    )

    medal_data.columns = [
        "Medal",
        "Count"
    ]


    fig1 = px.bar(
        medal_data,

        x="Medal",

        y="Count",

        color="Medal",

        color_discrete_map=medal_colors,

        text="Count",

        title=f"Medal Distribution - {selected_country}",

        labels={
            "Medal": "Medal Type",
            "Count": "Number of Medals"
        }
    )


    fig1.update_traces(
        textposition="outside"
    )


    fig1.update_layout(
        title_x=0.5,

        plot_bgcolor="white",

        paper_bgcolor="white",

        xaxis_title="Medal Type",

        yaxis_title="Number of Medals",

        legend_title="Medal Type"
    )


    # ----------------------------------------
    # Medal Trend Over Time
    # ----------------------------------------

    trend_data = (
        filtered_df
        .groupby(
            ["Year", "Medal"]
        )
        .size()
        .reset_index(
            name="Count"
        )
    )


    fig2 = px.line(
        trend_data,

        x="Year",

        y="Count",

        color="Medal",

        markers=True,

        color_discrete_map=medal_colors,

        title=f"Medal Trend Over Time - {selected_country}",

        labels={
            "Year": "Olympic Year",
            "Count": "Number of Medals",
            "Medal": "Medal Type"
        }
    )


    fig2.update_layout(
        title_x=0.5,

        plot_bgcolor="white",

        paper_bgcolor="white",

        xaxis_title="Olympic Year",

        yaxis_title="Number of Medals",

        legend_title="Medal Type"
    )


    return fig1, fig2


# --------------------------------------------
# 8. Run the application
# --------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)