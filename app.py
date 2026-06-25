from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="AI Agent Deployment Dashboard",
    page_icon="🤖",
    layout="wide",
)

DEFAULT_DATA_DIR = Path(r"C:\Users\DELL")


@st.cache_data(show_spinner=False)
def load_csv(path):
    return pd.read_csv(path, encoding="utf-8-sig")


# =========================
# FILTER CS JOBS
# =========================
def filter_cs(df):
    keywords = [
        "Computer","Software","Web","Database","Data",
        "Information Security","Network","Programmer",
        "Developer","Statistician"
    ]
    pattern = "|".join(keywords)
    return df[df["Occupation (O*NET-SOC Title)"].astype(str)
              .str.contains(pattern, case=False, na=False)].copy()


# =========================
# PREPARE DATA
# =========================
def prepare_data(tasks, expert, metadata, desires):

    for df in [tasks, expert, desires]:
        df["Task ID"] = pd.to_numeric(df["Task ID"], errors="coerce")

    cs_tasks = filter_cs(tasks)
    cs_expert = filter_cs(expert)
    cs_metadata = filter_cs(metadata)
    cs_desires = filter_cs(desires)

    # ---------- AGG ----------
    desire_agg = cs_desires.groupby(
        ["Task ID","Occupation (O*NET-SOC Title)","Task"]
    ).agg(
        desire_mean=("Automation Desire Rating","mean"),
        time_mean=("Time","mean"),
        core_skill_mean=("Core Skill Rating","mean"),
        job_security_mean=("Job Security Rating","mean"),
        worker_human_agency_mean=("Human Agency Scale Rating","mean"),
    ).reset_index()

    expert_agg = cs_expert.groupby("Task ID").agg(
        capacity_mean=("Automation Capacity Rating","mean")
    ).reset_index()

    meta = cs_tasks[[
        "Task ID",
        "Occupation Employment",
        "Occupation Mean Annual Wage"
    ]].drop_duplicates("Task ID")

    rec = desire_agg.merge(expert_agg, on="Task ID", how="left") \
                    .merge(meta, on="Task ID", how="left")

    # ---------- CLEAN ----------
    rec["capacity_filled"] = rec["capacity_mean"].fillna(3)

    rec["Occupation Employment"] = pd.to_numeric(
        rec["Occupation Employment"], errors="coerce"
    )
    rec["Occupation Employment"] = rec["Occupation Employment"].fillna(
        rec["Occupation Employment"].median()
    )
    rec["Occupation Employment"] = rec["Occupation Employment"].replace(0, 1)

    rec["wage"] = pd.to_numeric(
        rec["Occupation Mean Annual Wage"], errors="coerce"
    ).fillna(rec["Occupation Mean Annual Wage"].median())

    # ---------- METRICS ----------
    rec["trust_gap"] = rec["capacity_filled"] - rec["desire_mean"]

    rec["agent_fit_score"] = (
        0.35 * rec["capacity_filled"]
        + 0.25 * rec["desire_mean"]
        + 0.15 * rec["time_mean"]
        + 0.15 * (6 - rec["worker_human_agency_mean"])
        + 0.10 * (6 - rec["job_security_mean"])
    )

    # IMPACT SCORE (NEW 🔥)
    rec["impact_score"] = (
        rec["agent_fit_score"]
        * rec["Occupation Employment"]
        * rec["wage"]
    )

    # ---------- CATEGORY ----------
    def quadrant(row):
        if row["capacity_filled"] >= 3.5 and row["desire_mean"] >= 3.5:
            return "High-High"
        if row["capacity_filled"] >= 3.5:
            return "High Cap - Low Desire"
        if row["desire_mean"] >= 3.5:
            return "Low Cap - High Desire"
        return "Low-Low"

    rec["quadrant"] = rec.apply(quadrant, axis=1)

    return rec


# =========================
# LOAD DATA
# =========================
tasks = load_csv(DEFAULT_DATA_DIR / "task_statement_with_metadata.csv")
expert = load_csv(DEFAULT_DATA_DIR / "expert_rated_technological_capability.csv")
metadata = load_csv(DEFAULT_DATA_DIR / "domain_worker_metadata.csv")
desires = load_csv(DEFAULT_DATA_DIR / "domain_worker_desires.csv")

rec = prepare_data(tasks, expert, metadata, desires)


# =========================
# SIDEBAR FILTER
# =========================
with st.sidebar:
    occs = sorted(rec["Occupation (O*NET-SOC Title)"].dropna().unique())
    selected = st.multiselect("Occupation", occs, default=occs)

rec = rec[rec["Occupation (O*NET-SOC Title)"].isin(selected)]


# =========================
# TITLE
# =========================
st.title("🤖 From Automation Potential to Responsible AI Agent Deployment")


# =========================
# EXECUTIVE SUMMARY
# =========================
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Tasks", rec["Task ID"].nunique())
c2.metric("Occupations", rec["Occupation (O*NET-SOC Title)"].nunique())
c3.metric("Avg Desire", round(rec["desire_mean"].mean(),2))
c4.metric("Avg Capacity", round(rec["capacity_filled"].mean(),2))
c5.metric("Quick Wins", (rec["agent_fit_score"]>3.5).sum())
# ===== AUTO INSIGHT =====
top_occ = rec.groupby("Occupation (O*NET-SOC Title)")["agent_fit_score"].mean().idxmax()
top_gap = rec.groupby("Occupation (O*NET-SOC Title)")["trust_gap"].mean().idxmax()

st.markdown("### 🔎 Key Insights")

st.info(f"""
- Occupation with highest AI Agent Fit: **{top_occ}**
- Occupation with largest Trust Gap: **{top_gap}**
- High potential tasks are concentrated in **high capacity + high desire quadrant**
- Risk mainly comes from **high human agency & job security concern**
""")

# =========================
# TABS
# =========================
tabs = st.tabs([
    "1. Foundation",
    "2. Tension",
    "3. Trust & Gap",
    "4. Autonomy",
    "5. Risk",
    "6. Recommendations"
])


# =========================
# TAB 1 - FOUNDATION
# =========================
with tabs[0]:

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(px.histogram(
            rec, x="agent_fit_score",
            range_x=[1, 5],
            title="Distribution of Agent Fit Score"
        ), use_container_width=True)

    with col2:
        st.plotly_chart(px.scatter(
            rec,
            x="capacity_filled",
            y="desire_mean",
            color="agent_fit_score",
            hover_name="Task",
            title="Desire vs Capacity"
        ), use_container_width=True)
    corr_cols = [
    "desire_mean",
    "capacity_filled",
    "agent_fit_score",
    "worker_human_agency_mean",
    "job_security_mean",
        "time_mean"
    ]
    
    fig_corr = px.imshow(
        rec[corr_cols].corr(),
        text_auto=True,
        title="Feature Correlation Heatmap"
    )
    
    st.plotly_chart(fig_corr, use_container_width=True, key="foundation_corr")

# =========================
# TAB 2 - TENSION
# =========================
with tabs[1]:

    fig_tension = px.scatter(
        rec,
        x="capacity_filled",
        y="desire_mean",
        size="Occupation Employment",
        color="worker_human_agency_mean",
        hover_name="Task",
        title="AI Deployment Tension Map"
    )

    fig_tension.add_vline(x=3.5, line_dash="dash")
    fig_tension.add_hline(y=3.5, line_dash="dash")

    st.plotly_chart(fig_tension, use_container_width=True, key="tension_scatter")

    quad = rec["quadrant"].value_counts().reset_index()
    quad.columns = ["quadrant", "count"]

    fig_quad = px.pie(
        quad,
        names="quadrant",
        values="count",
        title="Opportunity Quadrant"
    )

    st.plotly_chart(fig_quad, use_container_width=True, key="tension_pie")
# =========================
# TAB 3 - TRUST
# =========================
with tabs[2]:

    fig_trust_hist = px.histogram(
    rec,
    x="trust_gap",
    title="Trust Gap Distribution"
    )

    st.plotly_chart(fig_trust_hist, use_container_width=True, key="trust_hist")

    fig_trust_scatter = px.scatter(
    rec,
    x="trust_gap",
    y="agent_fit_score",
    range_y=[2, 4],
    hover_name="Task",
    title="Trust Gap vs Opportunity"
    )

    st.plotly_chart(fig_trust_scatter, use_container_width=True, key="trust_scatter")
    trust_occ = rec.groupby("Occupation (O*NET-SOC Title)")["trust_gap"].mean().reset_index()

    fig_trust_bar = px.bar(
        trust_occ.sort_values("trust_gap"),
        x="trust_gap",
        y="Occupation (O*NET-SOC Title)",
        orientation="h",
        title="Average Trust Gap by Occupation"
    )
    
    st.plotly_chart(fig_trust_bar, use_container_width=True, key="trust_bar")
    fig_quad_bar = px.bar(
    quad,
    x="quadrant",
    y="count",
    title="Task Distribution by Opportunity Quadrant"
    )
    
    st.plotly_chart(fig_quad_bar, use_container_width=True, key="tension_bar")


# =========================
# TAB 4 - AUTONOMY
# =========================
with tabs[3]:

    fig_core = px.scatter(
        rec,
        x="core_skill_mean",
        y="capacity_filled",
        size="desire_mean",
        hover_name="Task",
        title="Core vs Automation"
    )
    
    st.plotly_chart(fig_core, use_container_width=True, key="autonomy_core")
    trust_quad = rec.groupby("quadrant")["trust_gap"].mean().reset_index()

    fig_trust_quad = px.bar(
        trust_quad,
        x="quadrant",
        y="trust_gap",
        title="Average Trust Gap by Quadrant"
    )
    
    st.plotly_chart(fig_trust_quad, use_container_width=True, key="trust_quad")
    def autonomy_proxy(row):
        if row["capacity_filled"] >= 4 and row["worker_human_agency_mean"] <= 2.5:
            return "Autonomous"
        if row["capacity_filled"] >= 3.5:
            return "Semi-Autonomous"
        if row["capacity_filled"] >= 3:
            return "Human-in-loop"
        return "Assistant"

    rec["autonomy_type"] = rec.apply(autonomy_proxy, axis=1)
    
    auto_df = rec["autonomy_type"].value_counts().reset_index()
    auto_df.columns = ["autonomy_type", "count"]
    
    fig_auto = px.bar(
        auto_df,
        x="count",
        y="autonomy_type",
        orientation="h",
        title="Distribution of AI Agent Autonomy Levels"
    )
    
    st.plotly_chart(fig_auto, use_container_width=True, key="autonomy_bar")
    fig_auto_fit = px.box(
    rec,
    x="autonomy_type",
    y="agent_fit_score",
    title="Agent Fit Score by Autonomy Level"
    )
    
    st.plotly_chart(fig_auto_fit, use_container_width=True, key="autonomy_fit")


# =========================
# TAB 5 - RISK
# =========================
with tabs[4]:

    fig_risk1 = px.scatter(
    rec,
    x="capacity_filled",
    y="worker_human_agency_mean",
    size="desire_mean",
    hover_name="Task",
    title="Human Control Risk"
    )
    
    st.plotly_chart(fig_risk1, use_container_width=True, key="risk_human")
    fig_risk2 = px.scatter(
    rec,
    x="agent_fit_score",
    y="job_security_mean",
    size="desire_mean",
    hover_name="Task",
    title="Job Security Risk"
    )
    
    st.plotly_chart(fig_risk2, use_container_width=True, key="risk_job")
    fig_risk3 = px.scatter(
    rec,
    x="agent_fit_score",
    y="worker_human_agency_mean",
    size="desire_mean",
    color="job_security_mean",
    title="Risk vs Opportunity Matrix"
    )
    
    st.plotly_chart(fig_risk3, use_container_width=True, key="risk_matrix")
    rec["risk_level"] = pd.cut(
    rec["worker_human_agency_mean"],
    bins=[0,2.5,3.5,5],
    labels=["Low Risk","Medium Risk","High Risk"]
    )
    
    risk_dist = rec["risk_level"].value_counts().reset_index()
    risk_dist.columns = ["risk_level","count"]
    
    fig_risk_bar = px.bar(
        risk_dist,
        x="risk_level",
        y="count",
        title="Distribution of Risk Levels"
    )
    
    st.plotly_chart(fig_risk_bar, use_container_width=True, key="risk_dist")
    

# =========================
# TAB 6 - RECOMMENDATION
# =========================
with tabs[5]:

    top = rec.sort_values("impact_score", ascending=False).head(20)
    sweet = rec[
    (rec["capacity_filled"] >= 3.5) &
    (rec["desire_mean"] >= 3.5) &
    (rec["worker_human_agency_mean"] <= 3)
    ]
    
    fig_sweet = px.scatter(
        sweet,
        x="capacity_filled",
        y="desire_mean",
        size="impact_score",
        hover_name="Task",
        title="Automation Sweet Spot"
    )
    
    st.plotly_chart(fig_sweet, use_container_width=True, key="rec_sweet")
    fig_top = px.bar(
        top.sort_values("impact_score"),
        x="impact_score",
        y="Task",
        orientation="h",
        title="Top 20 High Impact Tasks"
    )
    
    st.plotly_chart(fig_top, use_container_width=True, key="rec_top")
    # Pareto
    pareto = rec.sort_values("impact_score", ascending=False)
    pareto["cum_pct"] = pareto["impact_score"].cumsum() / pareto["impact_score"].sum()
    
    fig_pareto = px.line(
        pareto.head(50),
        y="cum_pct",
        title="Pareto Curve (Impact Concentration)"
    )
    
    st.plotly_chart(fig_pareto, use_container_width=True, key="rec_pareto")
    fig_if = px.scatter(
        rec,
        x="agent_fit_score",
        y="impact_score",
        size="Occupation Employment",
        title="Impact vs Feasibility"
    )
    
    st.plotly_chart(fig_if, use_container_width=True, key="rec_if")
    # Impact vs Feasibility
    fig_if = px.scatter(
    rec,
    x="agent_fit_score",
    y="impact_score",
    size="Occupation Employment",
    title="Impact vs Feasibility"
    )
    