
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Goethe B1 Lesen Trainer", layout="wide")

# Load Excel
@st.cache_data
def load_questions(path="questions.xlsx"):
    df = pd.read_excel(path)
    return df

df = load_questions()

# Sidebar selections
einheiten = sorted(df['einheit'].dropna().unique())
einheit = st.sidebar.selectbox("Wähle eine Einheit", einheiten)
teile = sorted(df[df['einheit'] == einheit]['teil'].dropna().unique())
teil = st.sidebar.selectbox("Wähle einen Teil", teile)

filtered = df[(df['einheit'] == einheit) & (df['teil'] == teil)]

st.title(f"📘 Goethe B1 Lesen - Einheit {einheit} Teil {teil}")

user_answers = {}
score = 0

with st.form(key="quiz_form"):
    for i, row in filtered.iterrows():
        st.markdown(f"**{i+1}. {row['frage']}**")
        options = [row[col] for col in ['option_a', 'option_b', 'option_c', 'option_d'] if pd.notna(row[col])]
        user_answers[i] = st.radio("", options, key=f"q{i}")

    submitted = st.form_submit_button("Antworten überprüfen")

if submitted:
    st.subheader("Ergebnisse")
    for i, row in filtered.iterrows():
        correct = row["korrekt"]
        user_input = user_answers.get(i)
        if user_input == correct:
            st.success(f"✅ Frage {i+1}: Richtig")
            score += 1
        else:
            st.error(f"❌ Frage {i+1}: Falsch (Richtig: {correct})")
    st.info(f"🔢 Gesamtpunktzahl: {score} von {len(filtered)}")
