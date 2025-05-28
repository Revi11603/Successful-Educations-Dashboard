import plotly.express as px
from preswald import connect, get_df, plotly, query, table, text

connect()
df = get_df("successful_educations")

text("# Successful Educations Analysis")

total       = len(df)
unique_p    = df.profession.nunique()
schol_pct   = (
    df[df.award.notnull() & (df.award != "")]
      .shape[0]
    / total
    * 100
)
text("## Key Metrics")
text(f"- **Total records:** {total}")
text(f"- **Unique professions:** {unique_p}")
text(f"- **Scholarship/Award recipients:** {schol_pct:.1f}%")

sql = """
SELECT
  profession,
  COUNT(*) AS record_count
FROM successful_educations
GROUP BY profession
ORDER BY record_count DESC
"""
prof_counts = query(sql, "successful_educations")

text("## Successful Educations Overview")
table(df.head(20), title="First 20 Records of the Dataset")
text("## Records by Profession")
table(prof_counts, title="Count by Profession")

prof_counts = (
    df.groupby("profession")
      .size()
      .reset_index(name="count")
      .sort_values("count", ascending=False)
)

text("## Profession Distribution")
fig1 = px.bar(
    prof_counts,
    x="profession",
    y="count",
    labels={"profession":"Profession","count":"Count"}
)
plotly(fig1)

text("## GPA Distribution")
fig2 = px.histogram(
    df,
    x="gpa",
    nbins=20,
    labels={"gpa":"GPA"}
)
plotly(fig2)

text("## GPA vs University Ranking by Degree")
fig3 = px.scatter(
    df,
    x="university_global_ranking",
    y="gpa",
    color="degree",
    title="",
    labels={
        "university_global_ranking": "University Global Ranking",
        "gpa": "GPA",
        "degree": "Degree"
    }
)
fig3.update_traces(marker=dict(size=8))
plotly(fig3)