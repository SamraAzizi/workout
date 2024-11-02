import streamlit as st


st.title("Personal Fitness Tool")

@st.fragment()
def personal_data_form():
    with st.form("personal_data"):
        st.header("Personal Data")

        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, step=0.1)
        gender = st.radio("Gender",["Female", "Male", "Others"])
        activities = (
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
            "Super Active",

        )

        activity_level = st.selectbox("Activity Level", activities)

        personal_data_submit = st.form_submit_button("Save")

        if personal_data_submit:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner():
                    #save the data
                    st.success("Information Saved.")

            else:
                st.warning("Please fill in all of the data!")


def forms():
    personal_data_form()

if __name__ == "__main__":
    forms()