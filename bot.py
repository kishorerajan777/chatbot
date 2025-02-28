import streamlit as st
import pandas as pd
import re
import time
import plotly.express as px  

# Load dataset
file_path ="Diseases.csv"
df = pd.read_csv(file_path)

# Ensure required columns exist
required_columns = {"Disease", "Symptoms", "Precautions", "Description", "Symptom_Severity"}
if not required_columns.issubset(df.columns):
    st.error(f"⚠️ Missing required columns: {required_columns - set(df.columns)}")
    st.stop()

# Standardize disease names and symptoms
df["Disease"] = df["Disease"].astype(str).str.strip().str.lower()
df["Symptoms"] = df["Symptoms"].astype(str).str.strip().str.lower()

# Process Symptoms for Severity Chart
df_exploded = df.copy()
df_exploded["Symptoms"] = df_exploded["Symptoms"].str.split(",")
df_exploded = df_exploded.explode("Symptoms")
df_exploded["Symptoms"] = df_exploded["Symptoms"].str.strip().str.lower()

# Convert Severity Level
df_exploded["Symptom_Severity"] = df_exploded["Symptom_Severity"].astype(str)
df_exploded["Severity_Level"] = pd.to_numeric(df_exploded["Symptom_Severity"].str.extract(r'(\d+)')[0], errors="coerce")

# Initialize session state variables
session_keys = ["messages", "last_disease", "show_chart", "disease_names", "match_counts", "user_symptoms"]
for key in session_keys:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["messages", "disease_names", "match_counts", "user_symptoms"] else None

# Chatbot Title with Typewriter Effect
title_placeholder = st.empty()
title_text = "🩺 Hi, I am Medtech Chatbot"
display_text = ""

for char in title_text:
    display_text += char  
    title_placeholder.markdown(f"<h1 style='color: #FFD700;'>{display_text}</h1>", unsafe_allow_html=True)
    time.sleep(0.05)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown("<h1 style='color: orange;'>🩺 Hi, I am Medtech Chatbot</h1>", unsafe_allow_html=True)

# User Input
user_input = st.chat_input("Enter symptoms or ask about precautions/symptoms/effects...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = ""  

    # Keywords for different queries
    precaution_keywords = ["precaution", "how to prevent", "prevent", "safety", "what should i do"]
    symptom_keywords = ["what are the symptoms", "symptoms of", "i have"]

    # Process user input
    user_input_cleaned = re.sub(r'[^a-zA-Z ]', '', user_input).strip().lower()
    if "this disease" in user_input.lower() or "this" in user_input.lower():
        user_input_cleaned = st.session_state.last_disease or ""

    # Check if user asks for **precautions**
    if any(keyword in user_input.lower() for keyword in precaution_keywords):
        disease_asked = re.sub(r'[^a-zA-Z ]', '', user_input).strip().lower()

        # Handle "How to prevent this disease?" by using last predicted disease
        if "this disease" in user_input.lower() or "this" in user_input.lower():
            disease_asked = st.session_state.last_disease.lower() if st.session_state.last_disease else ""

        found = False
        for _, row in df.iterrows():
            disease = row['Disease'].lower()
            if disease in disease_asked:
                found = True
                precautions = row.get('Precautions', 'No precautions found').split(';')  
                response = f"**🛡️ Precautions for {row['Disease'].capitalize()}:**\n" + "\n".join([f"✅ {p.strip()}" for p in precautions])
                break
        
        if not found:
            response = "⚠️ Disease not found in database. Please check the name and try again."

    # Check if user asks for **symptoms**
    elif any(keyword in user_input.lower() for keyword in symptom_keywords):
        disease_asked = user_input_cleaned.lower()

        found = False
        for _, row in df.iterrows():
            disease = row['Disease'].lower()
            if disease in disease_asked:
                found = True
                symptoms = row.get('Symptoms', 'No symptoms found').split(',')
                response = f"**🤒 Symptoms of {row['Disease'].capitalize()}:**\n" + "\n".join([f"🔹 {s.strip()}" for s in symptoms])

                # Store symptoms for severity chart
                st.session_state.user_symptoms = [s.strip().lower() for s in symptoms]
                st.session_state.show_severity_chart = True  # Enable severity chart automatically
                break

        if not found:
            response = "⚠️ Disease not found in database. Please check the name and try again."
        
    # **If user enters symptoms, find matching diseases**



    # **If user enters symptoms, find matching diseases**w
    else:
        user_symptoms = set(re.findall(r'\w+', user_input.lower()))
        df["MatchCount"] = df["Symptoms"].apply(lambda x: len(set(re.findall(r'\w+', x)).intersection(user_symptoms)))
        disease_matches = df[df["MatchCount"] > 0].nlargest(3, "MatchCount")

        if not disease_matches.empty:
            response += "🦠 **Top 3 Possible Diseases:**\n\n"
            st.session_state.user_symptoms = list(user_symptoms)  # Store for severity chart
            st.session_state.disease_matches = disease_matches.to_dict("records")  # Store matches for chart

            for _, row in disease_matches.iterrows():
                response += f"\n🔹 **{row['Disease'].capitalize()}**\n\n"
                response += f"\n📖 **Description:** {row.get('Description', 'No description available')}\n\n"
                response += "\n🤒 **Symptoms:**\n\n"
                # Display each symptom on a new line
                for symptom in row["Symptoms"].split(","):
                    response += f"🔹 {symptom.strip()}\n\n"
                # Display matched symptoms count on a new line
                response += f"\n\n🔹 **Matched Symptoms Count:**\n{row['MatchCount']}\n"
                response += "\n\n"  # Add a new line for spacing

            st.session_state.show_chart = True  
        else:
            response = "⚠️ No matching disease found. Please check the symptoms or try rephrasing."

    
        # Display chatbot response with typing effect
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            time.sleep(2)
            placeholder = st.empty()
            typed_text = ""
            for word in response.split():
                typed_text += word + " "
                placeholder.markdown(typed_text)
                time.sleep(0.05)

    st.session_state.messages.append({"role": "assistant", "content": response})

#-----------------------------------------------   BARCHART VISUALS  -----------------------------------------------------------------#

# Show buttons only if symptoms have been processed
if "user_symptoms" in st.session_state and st.session_state.user_symptoms:
    
    #📊 Button to Show Symptom Severity Chartss
    if st.button("📊 See Symptom Severity Chart"):
        st.session_state.show_severity_chart = not st.session_state.get("show_severity_chart", False)

    # 📊 Button to Show Matched Symptoms Count for Top 3 Diseases
    if st.button("📊 See Matched Symptom Counts for Top 3 Diseases"):
        st.session_state.show_matched_chart = not st.session_state.get("show_matched_chart", False)
       
    # 📊 Symptom Severity Chart Display
    if st.session_state.get("show_severity_chart", False) and "user_symptoms" in st.session_state:
        st.markdown("### **📊 Symptom Severity Visualization**")

        matched_symptoms = [s.lower().strip() for s in st.session_state.user_symptoms]
        filtered_df = df_exploded[df_exploded["Symptoms"].isin(matched_symptoms)]

        severity_df = filtered_df.groupby("Symptoms", as_index=False)["Severity_Level"].max()

        if not severity_df.empty:
            fig2 = px.bar(
                severity_df, x="Symptoms", y="Severity_Level",
                title="🔍 Severity Levels of Your Symptoms",
                labels={"Symptoms": "Symptoms", "Severity_Level": "Severity Level"},
                color="Severity_Level",
                color_continuous_scale="viridis"
            )
            fig2.update_traces(textposition="outside")
            fig2.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("⚠️ No severity data found for the entered symptoms.")

    # 📊 Matched Symptoms Count Bar Chart Displays
    if st.session_state.get("show_matched_chart", False):  
        st.markdown("### **📊 Matched Symptom Counts for Top 3 Predicted Diseases**")

        if "disease_matches" in st.session_state:
            disease_matches_df = pd.DataFrame(st.session_state.disease_matches)

            # Extract data for chart
            disease_names = disease_matches_df["Disease"].str.capitalize().tolist()
            match_counts = disease_matches_df["MatchCount"].tolist()

            if disease_names:
                fig3 = px.bar(
                    x=disease_names,
                    y=match_counts,
                    text=match_counts,
                    labels={"x": "Disease", "y": "Matched Symptom Count"},
                    title="🔍 Matched Symptoms for Top 3 Predicted Diseases",
                    color=match_counts,
                    color_continuous_scale="portland",
                )
                fig3.update_traces(textposition="outside")
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.warning("⚠️ No matched symptoms found.")
        else:
            st.warning("⚠️ No stored data for matched symptoms. Please enter symptoms first.")


#-------------------------------------------------------------------------------------------------------------------------------------#
