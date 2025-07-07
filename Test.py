import streamlit as st

# Main tabs
tab1, tab2 = st.tabs(["Main Tab 1", "Main Tab 2"])

with tab1:
    st.header("Main Tab 1 Content")
    
    # Subtabs using radio buttons
    subtab = st.selectbox("Choose a subtab:", ["Subtab A", "Subtab B", "Subtab C"])
    
    if subtab == "Subtab A":
        st.write("You selected Subtab A content.")
    elif subtab == "Subtab B":
        st.write("You selected Subtab B content.")
    elif subtab == "Subtab C":
        st.write("You selected Subtab C content.")

with tab2:
    st.header("Main Tab 2 Content")
    st.write("This is just another main tab.")
