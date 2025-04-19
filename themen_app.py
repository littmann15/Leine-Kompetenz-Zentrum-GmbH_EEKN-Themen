import streamlit as st
import json
import os
import uuid
from datetime import datetime

DB_FILE = "themen_db.json"

# Datenbank laden oder initialisieren
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

db = load_db()

# Streamlit UI
st.set_page_config(page_title="Themenplattform", layout="centered")

st.title("📝 Themenplattform für Klimaschutz-Netzwerke")

query_params = st.query_params
session_id = query_params.get("session", [None])[0]

# Wenn keine Session-ID, dann Admin-Ansicht
if session_id is None:
    st.subheader("🔐 Admin-Bereich")

    if st.button("Neue Session erstellen"):
        new_id = uuid.uuid4().hex[:6].upper()
        db[new_id] = []
        save_db(db)
        st.success(f"Neue Session erstellt: `{new_id}`")
        st.markdown(f"📎 **Teilnehmer-Link:** `?session={new_id}`")
        st.code(f"http://localhost:8501/?session={new_id}", language="markdown")

    st.markdown("---")
    st.subheader("📊 Themen anzeigen")

    selected_id = st.text_input("Session-ID eingeben")

    if selected_id:
        if selected_id in db:
            st.success(f"Themen für Session {selected_id}")
            for idx, entry in enumerate(db[selected_id], 1):
                st.markdown(f"**{idx}.** {entry['text']}  \n*eingereicht am {entry['timestamp']}*")
        else:
            st.warning("Diese Session existiert nicht.")
else:
    st.subheader(f"💡 Themen einreichen – Session {session_id}")
    if session_id not in db:
        st.error("Ungültige Session-ID.")
    else:
        text = st.text_area("Was möchtest du einbringen?", max_chars=300)
        if st.button("Absenden"):
            if text.strip():
                db[session_id].append({
                    "text": text.strip(),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                save_db(db)
                st.success("✅ Vielen Dank für deinen Vorschlag!")
            else:
                st.warning("Bitte gib ein Thema ein.")
