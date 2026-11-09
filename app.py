from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_FILE = "ecommerce_customers.csv"
CONTACT_COLUMNS = {"Email", "Address"}
REQUIRED_NUMERIC_COLUMNS = [
    "Avg. Session Length",
    "Time on App",
    "Time on Website",
    "Length of Membership",
    "Yearly Amount Spent",
]
NAVY = "#101828"
BLUE = "#3B82F6"
CYAN = "#22D3EE"
GRID = "#E8EEF6"
CHART_FONT = "Inter, Aptos, Segoe UI, sans-serif"


st.set_page_config(
    page_title="E-Commerce Customer Insights",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_styles() -> None:
    """Apply the dashboard's clean white and blue visual system."""
    st.markdown(
        """
        <style>
        :root {
            --ink: #101828;
            --muted: #667085;
            --blue: #3B82F6;
            --cyan: #22D3EE;
            --pale-blue: #F3F7FC;
            --line: #E3EAF3;
            --surface: #FFFFFF;
        }
        .stApp {
            background: #FFFFFF;
            color: var(--ink);
        }
        html, body, [class*="st-"] { font-family: Inter, Aptos, "Segoe UI", sans-serif; }
        [data-testid="stHeader"] { background: #FFFFFF; }
        [data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebarContent"] { padding: 1.15rem .9rem; }
        .block-container { padding-top: 1.65rem; padding-bottom: 3rem; max-width: 1440px; }
        h1, h2, h3 { color: var(--ink); letter-spacing: -0.025em; font-weight: 700 !important; }
        h2, h3 { margin-bottom: .45rem !important; }
        [data-testid="stSidebar"] h2 { color: var(--ink); font-size: 1.1rem; }
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            color: var(--muted);
            line-height: 1.5;
        }
        .hero {
            position: relative; overflow: hidden; isolation: isolate;
            background: #FFFFFF;
            border: 1px solid var(--line); border-radius: 20px;
            padding: clamp(1.55rem, 4vw, 2.65rem); margin: .25rem 0 1.4rem;
            box-shadow: 0 8px 26px rgba(16, 24, 40, .06);
        }
        .hero:after {
            content: ""; position: absolute; z-index: -1; width: 270px; height: 270px;
            right: -80px; top: -150px; border-radius: 50%;
            background: rgba(59, 130, 246, .08); filter: blur(2px);
        }
        .hero-eyebrow {
            color: var(--blue); text-transform: uppercase; letter-spacing: .13em;
            font-size: .73rem; font-weight: 750; margin-bottom: .65rem;
        }
        .hero-title {
            color: var(--ink); font-size: clamp(1.8rem, 4.1vw, 2.8rem);
            line-height: 1.12; font-weight: 760; letter-spacing: -.035em;
            margin: 0 0 .7rem;
        }
        .dashboard-subtitle { color: var(--muted); font-size: clamp(.95rem, 1.6vw, 1.08rem); margin: 0; }
        .section-caption { color: var(--muted); margin-top: -.35rem; margin-bottom: 1.1rem; line-height: 1.5; }
        .eyebrow {
            color: var(--blue); text-transform: uppercase; letter-spacing: .11em;
            font-size: .75rem; font-weight: 750; margin-bottom: .35rem;
        }
        [data-testid="stMetric"] {
            position: relative; overflow: hidden;
            background: var(--surface); padding: 1.1rem 1.2rem;
            border: 1px solid var(--line); border-radius: 16px;
            box-shadow: 0 7px 22px rgba(16, 24, 40, .055);
            min-height: 112px;
            transition: box-shadow .16s ease, border-color .16s ease;
        }
        [data-testid="stMetric"]:before {
            content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--blue), var(--cyan));
        }
        [data-testid="stMetric"]:hover {
            border-color: #C8D8EF; box-shadow: 0 10px 26px rgba(16, 24, 40, .09);
        }
        [data-testid="stMetricLabel"] { color: var(--muted); font-weight: 600; font-size: .88rem; }
        [data-testid="stMetricValue"] { color: var(--ink); font-weight: 750; }
        [data-testid="stPlotlyChart"] {
            background: #FFFFFF; border: 1px solid var(--line);
            border-radius: 16px; padding: .35rem;
            box-shadow: 0 6px 20px rgba(16, 24, 40, .04);
        }
        [data-testid="stSidebar"] button {
            border-radius: 10px; border: 1px solid #D6E4F6;
            color: var(--ink); background: #FFFFFF; font-weight: 600;
        }
        [data-testid="stSidebar"] button:hover {
            border-color: var(--blue); color: var(--blue); background: #F5F9FF;
        }
        [data-testid="stSlider"] [role="slider"] { border-color: var(--blue); }
        div[data-testid="stAlert"] { border-radius: 12px; border: 1px solid var(--line); }
        .insight-card {
            background: #FFFFFF; border: 1px solid var(--line); border-left: 4px solid var(--blue);
            border-radius: 14px; padding: 1.05rem 1.15rem; height: 100%;
            box-shadow: 0 5px 16px rgba(16, 24, 40, .035);
        }
        .insight-title { color: var(--ink); font-weight: 700; margin-bottom: .35rem; }
        .insight-text { color: var(--muted); line-height: 1.5; font-size: .94rem; }
        .data-note { color: var(--muted); font-size: .85rem; line-height: 1.5; }
        @media (max-width: 640px) {
            .block-container { padding: 1rem .85rem 2rem; }
            .hero { border-radius: 17px; }
            [data-testid="stMetric"] { min-height: 100px; padding: .9rem; }
            .hero-title { line-height: 1.16; }
            [data-testid="stPlotlyChart"] { padding: .15rem; border-radius: 13px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner="Loading customer data...")
def load_customer_data(file_name: str) -> pd.DataFrame:
    """Read the project CSV and return a safely prepared copy."""
    data_path = Path(__file__).parent / file_name
    data = pd.read_csv(data_path)

    missing_columns = [column for column in REQUIRED_NUMERIC_COLUMNS if column not in data.columns]
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing_columns)}")

    for column in REQUIRED_NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    for column in data.select_dtypes(include="number").columns:
        median_value = data[column].median()
        if pd.notna(median_value):
            data[column] = data[column].fillna(median_value)

    for column in data.select_dtypes(exclude="number").columns:
        if column not in CONTACT_COLUMNS and data[column].isna().any():
            data[column] = data[column].fillna("Unknown")

    data = data.dropna(subset=REQUIRED_NUMERIC_COLUMNS).copy()
    if data.empty:
        raise ValueError("No complete customer rows remain after checking required numeric fields.")
    return data


def format_amount(value: float) -> str:
    return f"${value:,.2f}"


def correlation_description(value: float) -> str:
    if pd.isna(value):
        return "not available for this selection"
    magnitude = abs(value)
    if magnitude < 0.1:
        strength = "little to no"
    elif magnitude < 0.4:
        strength = "weak"
    elif magnitude < 0.7:
        strength = "moderate"
    else:
        strength = "strong"
    direction = "positive" if value > 0 else "negative" if value < 0 else ""
    return f"{strength} {direction} linear association".strip()


def make_histogram(data: pd.DataFrame, column: str, title: str, x_label: str):
    figure = px.histogram(
        data,
        x=column,
        nbins=30,
        title=title,
        labels={column: x_label, "count": "Number of customers"},
        color_discrete_sequence=[BLUE],
        hover_data={column: ":.2f"},
    )
    figure.update_traces(marker_line_color=CYAN, marker_line_width=0.5)
    figure.update_layout(
        template="plotly_white",
        title_x=0.03,
        margin=dict(l=25, r=20, t=65, b=35),
        bargap=0.08,
        showlegend=False,
        font=dict(family=CHART_FONT, color=NAVY, size=12),
        title=dict(font=dict(color=NAVY, size=16)),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        hoverlabel=dict(bgcolor=NAVY, bordercolor=CYAN, font=dict(color="#FFFFFF")),
    )
    figure.update_xaxes(title_text=x_label, gridcolor=GRID, linecolor="#D5DFEC", zerolinecolor=GRID)
    figure.update_yaxes(
        title_text="Number of customers",
        gridcolor=GRID,
        linecolor="#D5DFEC",
        zerolinecolor=GRID,
    )
    return figure


def make_scatter(data: pd.DataFrame, x_column: str, title: str, x_label: str):
    figure = px.scatter(
        data,
        x=x_column,
        y="Yearly Amount Spent",
        title=title,
        labels={x_column: x_label, "Yearly Amount Spent": "Yearly amount spent ($)"},
        color_discrete_sequence=[BLUE],
        opacity=0.78,
        hover_data={
            x_column: ":.2f",
            "Yearly Amount Spent": ":.2f",
        },
    )
    figure.update_traces(marker=dict(line=dict(color=CYAN, width=0.55)))
    figure.update_layout(
        template="plotly_white",
        title_x=0.03,
        margin=dict(l=25, r=20, t=65, b=35),
        showlegend=False,
        font=dict(family=CHART_FONT, color=NAVY, size=12),
        title=dict(font=dict(color=NAVY, size=16)),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        hoverlabel=dict(bgcolor=NAVY, bordercolor=CYAN, font=dict(color="#FFFFFF")),
    )
    figure.update_xaxes(title_text=x_label, gridcolor=GRID, linecolor="#D5DFEC", zerolinecolor=GRID)
    figure.update_yaxes(
        title_text="Yearly amount spent ($)",
        gridcolor=GRID,
        linecolor="#D5DFEC",
        zerolinecolor=GRID,
    )
    return figure


def show_insight(title: str, text: str) -> None:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">{title}</div>
            <div class="insight-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


apply_styles()

st.markdown(
    '<header class="hero">'
    '<div class="hero-eyebrow">Customer analytics · E-commerce</div>'
    '<h1 class="hero-title">E-Commerce Customer Insights Dashboard</h1>'
    '<p class="dashboard-subtitle">Exploring customer behavior, engagement, and yearly spending patterns.</p>'
    '</header>',
    unsafe_allow_html=True,
)

try:
    customers = load_customer_data(DATA_FILE)
except FileNotFoundError:
    st.error(
        f"Could not find **{DATA_FILE}**. Place it in the same project folder as `app.py`, "
        "then refresh the dashboard."
    )
    st.stop()
except (pd.errors.ParserError, UnicodeDecodeError, ValueError) as error:
    st.error(f"Could not prepare the customer data: {error}")
    st.stop()

st.markdown(
    '<div class="data-note">All metrics, charts, and insights below reflect the selected customer subset. '
    "Email and full address fields are never displayed.</div>",
    unsafe_allow_html=True,
)

membership_column = "Length of Membership"
spending_column = "Yearly Amount Spent"
membership_bounds = (
    float(customers[membership_column].min()),
    float(customers[membership_column].max()),
)
spending_bounds = (
    float(customers[spending_column].min()),
    float(customers[spending_column].max()),
)

with st.sidebar:
    st.markdown("## Dashboard controls")
    st.caption("Filter the customer records shown across the dashboard.")
    if st.button("Reset filters", use_container_width=True):
        st.session_state["membership_range"] = membership_bounds
        st.session_state["spending_range"] = spending_bounds

    membership_range = st.slider(
        "Membership Length Range",
        min_value=membership_bounds[0],
        max_value=membership_bounds[1],
        value=membership_bounds,
        key="membership_range",
        help="Select the customer membership duration range.",
    )
    spending_range = st.slider(
        "Yearly Amount Spent Range",
        min_value=spending_bounds[0],
        max_value=spending_bounds[1],
        value=spending_bounds,
        key="spending_range",
        help="Select the yearly spending range.",
    )
    st.markdown("---")
    st.caption(f"Source: `{DATA_FILE}`")
    st.caption(f"Source rows: {len(customers):,}")

filtered = customers.loc[
    customers[membership_column].between(membership_range[0], membership_range[1])
    & customers[spending_column].between(spending_range[0], spending_range[1])
].copy()

st.markdown("### Customer overview")
st.markdown(
    '<div class="section-caption">A high-level summary of the customers currently included by your filters.</div>',
    unsafe_allow_html=True,
)

metric_columns = st.columns(4)
if filtered.empty:
    metric_values = ["0", "—", "—", "—"]
else:
    metric_values = [
        f"{len(filtered):,}",
        format_amount(float(filtered[spending_column].mean())),
        f"{filtered[membership_column].mean():.2f}",
        format_amount(float(filtered[spending_column].max())),
    ]
metric_labels = [
    "Total Customers",
    "Average Yearly Spending",
    "Average Membership Length",
    "Highest Yearly Spending",
]
for column, label, value in zip(metric_columns, metric_labels, metric_values):
    column.metric(label, value)

if filtered.empty:
    st.warning("No customers match both selected ranges. Widen one or both filters to see charts and insights.")
else:
    st.markdown("### Customer spending patterns")
    st.markdown(
        '<div class="section-caption">Explore spending distributions and how customer engagement relates to yearly spending.</div>',
        unsafe_allow_html=True,
    )

    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.plotly_chart(
            make_histogram(
                filtered,
                spending_column,
                "Distribution of Yearly Customer Spending",
                "Yearly amount spent ($)",
            ),
            width="stretch",
            key="spending_histogram",
        )
    with chart_right:
        st.plotly_chart(
            make_histogram(
                filtered,
                membership_column,
                "Distribution of Membership Length",
                "Membership length (dataset units)",
            ),
            width="stretch",
            key="membership_histogram",
        )

    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.plotly_chart(
            make_scatter(
                filtered,
                "Time on App",
                "Mobile App Engagement vs Yearly Spending",
                "Time on App",
            ),
            width="stretch",
            key="app_spending_scatter",
        )
    with chart_right:
        st.plotly_chart(
            make_scatter(
                filtered,
                "Time on Website",
                "Website Engagement vs Yearly Spending",
                "Time on Website",
            ),
            width="stretch",
            key="website_spending_scatter",
        )

    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.plotly_chart(
            make_scatter(
                filtered,
                membership_column,
                "Membership Length vs Yearly Spending",
                "Membership length (dataset units)",
            ),
            width="stretch",
            key="membership_spending_scatter",
        )
    with chart_right:
        correlation_columns = REQUIRED_NUMERIC_COLUMNS
        correlation_matrix = filtered[correlation_columns].corr()
        heatmap = px.imshow(
            correlation_matrix,
            text_auto=".2f",
            color_continuous_scale=[
                [0.0, NAVY],
                [0.25, BLUE],
                [0.5, "#F8FAFC"],
                [1.0, CYAN],
            ],
            range_color=(-1, 1),
            aspect="auto",
            title="Correlation Between Customer Measures",
            labels={"x": "Customer measure", "y": "Customer measure", "color": "Correlation"},
        )
        heatmap.update_layout(
            template="plotly_white",
            title_x=0.03,
            margin=dict(l=25, r=20, t=65, b=45),
            font=dict(family=CHART_FONT, color=NAVY, size=12),
            title=dict(font=dict(color=NAVY, size=16)),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            hoverlabel=dict(bgcolor=NAVY, bordercolor=CYAN, font=dict(color="#FFFFFF")),
            coloraxis_colorbar=dict(
                title=dict(text="Correlation", font=dict(color=NAVY)),
                tickfont=dict(color=NAVY),
                outlinecolor="#D5DFEC",
            ),
        )
        heatmap.update_xaxes(
            title_text="Customer measure",
            tickangle=-35,
            tickfont=dict(color=NAVY, size=10),
            title_font=dict(color=NAVY),
        )
        heatmap.update_yaxes(
            title_text="Customer measure",
            autorange="reversed",
            tickfont=dict(color=NAVY, size=10),
            title_font=dict(color=NAVY),
        )
        st.plotly_chart(
            heatmap,
            width="stretch",
            key="correlation_heatmap",
        )

    st.markdown("### App vs Website comparison")
    st.markdown(
        '<div class="section-caption">Pearson correlation compares the direction and strength of each channel’s linear association with yearly spending.</div>',
        unsafe_allow_html=True,
    )
    app_correlation = filtered["Time on App"].corr(filtered[spending_column])
    website_correlation = filtered["Time on Website"].corr(filtered[spending_column])
    comparison_columns = st.columns(2)
    comparison_columns[0].metric(
        "App time ↔ yearly spending",
        f"{app_correlation:.3f}" if pd.notna(app_correlation) else "—",
        help=correlation_description(app_correlation),
    )
    comparison_columns[1].metric(
        "Website time ↔ yearly spending",
        f"{website_correlation:.3f}" if pd.notna(website_correlation) else "—",
        help=correlation_description(website_correlation),
    )
    if pd.isna(app_correlation) or pd.isna(website_correlation):
        st.info("A channel comparison is unavailable for this selection because at least one correlation is undefined.")
    elif abs(app_correlation) > abs(website_correlation):
        st.info(
            f"Within the filtered customers, app time has the stronger linear relationship "
            f"(r = {app_correlation:.3f}) than website time (r = {website_correlation:.3f}). "
            "Correlation indicates association, not causation."
        )
    elif abs(website_correlation) > abs(app_correlation):
        st.info(
            f"Within the filtered customers, website time has the stronger linear relationship "
            f"(r = {website_correlation:.3f}) than app time (r = {app_correlation:.3f}). "
            "Correlation indicates association, not causation."
        )
    else:
        st.info(
            f"Within the filtered customers, app and website time have equally strong linear "
            f"relationships by absolute correlation (r = {app_correlation:.3f} and {website_correlation:.3f}). "
            "Correlation indicates association, not causation."
        )

    st.markdown("### Key Business Insights")
    median_spending = float(filtered[spending_column].median())
    mean_spending = float(filtered[spending_column].mean())
    spending_skew = float(filtered[spending_column].skew()) if len(filtered) > 2 else float("nan")
    if pd.isna(spending_skew):
        spending_shape = "not enough observations to describe the spending distribution's skew"
    elif spending_skew > 0.5:
        spending_shape = "right-skewed"
    elif spending_skew < -0.5:
        spending_shape = "left-skewed"
    else:
        spending_shape = "approximately symmetric"

    membership_correlation = filtered[membership_column].corr(filtered[spending_column])
    numeric_correlations = filtered[REQUIRED_NUMERIC_COLUMNS].corr()[spending_column].drop(
        spending_column
    ).dropna()
    if numeric_correlations.empty:
        top_feature_insight = "Not enough variation in this selection to calculate feature correlations with yearly spending."
    else:
        strongest_feature = numeric_correlations.abs().idxmax()
        strongest_correlation = float(numeric_correlations[strongest_feature])
        strongest_label = {
            "Avg. Session Length": "Average session length",
            "Time on App": "Time on App",
            "Time on Website": "Time on Website",
            membership_column: "Length of Membership",
        }[strongest_feature]
        top_feature_insight = (
            f"{strongest_label} has the strongest linear association with yearly spending in "
            f"this selection (r = {strongest_correlation:.3f}; "
            f"{correlation_description(strongest_correlation)})."
        )
    if pd.notna(app_correlation) and pd.notna(website_correlation):
        if abs(app_correlation) > abs(website_correlation):
            channel_insight = (
                f"The app has the stronger absolute correlation with spending "
                f"in this filtered selection (|r| = {abs(app_correlation):.3f}). "
                "This is an association, not a causal effect."
            )
        elif abs(website_correlation) > abs(app_correlation):
            channel_insight = (
                f"The website has the stronger absolute correlation with spending "
                f"in this filtered selection (|r| = {abs(website_correlation):.3f}). "
                "This is an association, not a causal effect."
            )
        else:
            channel_insight = (
                "App and website time have equally strong absolute correlations with spending "
                "in this selection. Correlation is not causation."
            )
    else:
        channel_insight = (
            "The channel comparison is unavailable because at least one correlation is undefined "
            "for this selection."
        )

    insight_row_one = st.columns(2)
    with insight_row_one[0]:
        show_insight(
            "Customer spending patterns",
            f"Average yearly spending is {format_amount(mean_spending)} and the median is "
            f"{format_amount(median_spending)}. The filtered distribution is {spending_shape}.",
        )
    with insight_row_one[1]:
        show_insight(
            "Membership and spending",
            f"Membership length has a {correlation_description(membership_correlation)} "
            f"with yearly spending (r = {membership_correlation:.3f}).",
        )
    insight_row_two = st.columns(2)
    with insight_row_two[0]:
        show_insight(
            "App vs website engagement",
            channel_insight,
        )
    with insight_row_two[1]:
        show_insight("Strongest spending relationship", top_feature_insight)

st.markdown("---")
show_raw_data = st.checkbox("Show Raw Customer Data")
if show_raw_data:
    if filtered.empty:
        st.info("There are no customer records to display for the current filters.")
    else:
        display_columns = [column for column in filtered.columns if column not in CONTACT_COLUMNS]
        st.dataframe(
            filtered[display_columns],
            width="stretch",
            hide_index=True,
        )
        st.caption(
            f"Showing {len(filtered):,} filtered rows. Email and Address are excluded for privacy."
        )
