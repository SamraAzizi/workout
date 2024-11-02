import streamlit as st
from profiles import create_profile, get_profile, get_notes, get_profile
from form_submit import update_personal_info, delete_note, add_note

st.title("Personal Fitness Tool")

@st.fragment()
def personal_data_form():
    with st.form("personal_data"):
        st.header("Personal Data")

        profile = st.session_state.profile

        name = st.text_input("Name", value=profile["general"]["name"])
        age = st.number_input("Age", min_value=1, max_value=120, step=1, value=profile["general"]["age"] )
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, step=0.1, value=float(profile["general"]["weight"]))
        height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, step=0.1, value=float(profile["general"]["height"]))
        genders = ["Female", "Male", "Others"]
        gender = st.radio("Gender",genders,genders.index(profile["general"].get("gender", "Female")))
        activities = (
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
            "Super Active",

        )

        activity_level = st.selectbox("Activity Level", activities, index=activities.index(profile["general"].get("activity_level", "sedentary")))

        personal_data_submit = st.form_submit_button("Save")

        if personal_data_submit:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner():
                    st.session_state.profile = update_personal_info(profile, "general", name=name, weight = weight, height=height, gender=gender, age=age, activity_level=activity_level)
                    st.success("Information Saved.")

            else:
                st.warning("Please fill in all of the data!")


@st.fragment()
def goals_form():
    profile = st.session_state.profile
    with st.form("goals_form"):
        st.header("Goals")
        goals = st.multiselect(
            "Select your Goals", ["Muscle Gain", "Fat Loss", "Stay Active"],
            default=profile.get("goals", ["Muscle Gain"])
        )

        goals_submit = st.form_submit_button('Save')
        if goals_submit:
            if goals:
                with st.spinner():
                    st.session_state.profile = update_personal_info(profile, "goals", goals=goals)
                    st.success("Goals Updated")
            else:
                st.warning("Please Select At least One Goal.")



def forms():
    if "profile" not in st.session_state:
        profile_id = 1
        profile = get_profile(profile_id)
        if not profile:
            profile_id, profile = create_profile(profile_id)

        st.session_state.profile = profile
        st.session_state.profile_id = profile_id

    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(st.session_state.profile_id)


    personal_data_form()
    goals_form()

if __name__ == "__main__":
    forms()