import streamlit as st
import pandas as pd
import re
import time 

# Load dataset
df = pd.read_csv('merged_diseases_final.csv')
df['Symptoms'] = df['Symptoms'].astype(str).str.lower()

# Initialize session state for chat history and last predicted disease
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_disease" not in st.session_state:
    st.session_state.last_disease = None

# Create a placeholder for the title
title_placeholder = st.empty()

# Full title text
full_text = "🩺 Hi, I am Medtech Chatbot"

# Typewriter effect
display_text = ""
for char in full_text:
    display_text += char  # Add one letter at a time
    title_placeholder.title(display_text)
    time.sleep(0.05)  # Adjust speed

# Final static title after animation
title_placeholder.title(full_text)
# Display chat history (User & Bot messages)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_input = st.chat_input("Enter symptoms or ask about precautions/symptoms/effects...")

if user_input:
    # Display user input message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Store user input in chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = ""  # Store chatbot response

    # Keywords for different queries
    precaution_keywords = ["precaution", "how to prevent", "prevent", "safety","what i do"]
    symptom_keywords = ["what are the symptoms", "symptoms of"]

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
                response = f"**🛡️ Precautions for {row['Disease']}:**\n" + "\n".join([f"✅ {p.strip()}" for p in precautions])
                break
        
        if not found:
            response = "⚠️ Disease not found in database. Please check the name and try again."

    # Check if user asks for **symptoms**
    elif any(keyword in user_input.lower() for keyword in symptom_keywords):
        disease_asked = re.sub(r'[^a-zA-Z ]', '', user_input).strip().lower()

        found = False
        for _, row in df.iterrows():
            disease = row['Disease'].lower()
            if disease in disease_asked:
                found = True
                symptoms = row.get('Symptoms', 'No symptoms found').split(',')
                response = f"**🤒 Symptoms of {row['Disease']}:**\n" + "\n".join([f"🔹 {s.strip()}" for s in symptoms])
                break
        
        if not found:
            response = "⚠️ Disease not found in database. Please check the name and try again."


    else:
        # Extract user symptoms
        user_symptoms = set(re.findall(r'\w+', user_input.lower()))

        # Store disease matches
        disease_match = {}

        # Check user symptoms against dataset
        for _, row in df.iterrows():
            disease = row['Disease']
            symptoms = set(re.findall(r'\w+', row['Symptoms']))
            matched_symptoms = user_symptoms.intersection(symptoms)
            match_count = len(matched_symptoms)

            if match_count > 0:
                disease_match[disease] = (match_count, matched_symptoms)

        # Sort by most matched symptoms
        sorted_diseases = sorted(disease_match.items(), key=lambda x: x[1][0], reverse=True)

        if sorted_diseases:
            response = f"✅ **Matched Symptoms:** {', '.join(user_symptoms)}\n\n"
            response += "🦠 **Possible Diseases:**\n"
            top_diseases = sorted_diseases[:3]

            for disease, (match_count, matched_symptoms) in top_diseases:
                response += f"🔹 **{disease}** (Matched Symptoms: {match_count})\n"
                response += f"   ➤ Symptoms Matched: {', '.join(matched_symptoms)}\n\n"

            # Store last predicted disease for future queries
            st.session_state.last_disease = top_diseases[0][0]

    # Display chatbot response with loading effect
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):  # Show loading animation
            time.sleep(2)  # Simulate processing delay
            placeholder = st.empty()  
            typed_text = ""  

            for word in response.split():
                typed_text += word + " "
                placeholder.markdown(typed_text)  
                time.sleep(0.09)  # Adjust speed of typing effect

    # Store chatbot response
    st.session_state.messages.append({"role": "assistant", "content": response})
