import streamlit as st
import json
import requests

base_url = "https://api.sampleapis.com/futurama/"
available_topics = ["info", "characters", "cast", "episodes", "questions", "inventory"]

st.title("Available topics:")
for t in available_topics:
    st.markdown("- " + t.capitalize())

topic_raw = st.text_input("What are you interested in?")
topic = topic_raw.lower()

if topic in available_topics:
    st.title(topic.capitalize() + ":")
    r = requests.get(base_url + topic)
    content = json.loads(r.content)

    if topic == "characters":
        for character in content:
            st.write(character["name"]["first"])
            st.image(character["images"]["main"])
    elif topic == "info":
        local_content = content[0]
        print(local_content)
        st.subheader("Synopsis:")
        st.write(local_content["synopsis"])

        st.subheader("Years aired: " + local_content["yearsAired"])

        st.subheader("Creators:")
        for creator in local_content["creators"]:
            c = creator["name"]
            st.markdown(f"[{c}](%s)" % creator["url"])
    elif topic == "cast":
        st.write(content)
    elif topic == "episodes":
        st.write(content)
    elif topic == "questions":
        st.write(content)
    elif topic == "inventory":
        st.write(content)
