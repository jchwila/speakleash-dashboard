import pandas as pd
import plotly.express as px
import streamlit as st
from pandas import json_normalize
from streamlit_extras.add_vertical_space import add_vertical_space
from speakleash import Speakleash
import os
import random


base_dir = os.path.join(os.path.dirname(__file__))
replicate_to = os.path.join(base_dir, "datasets")
sl = Speakleash(replicate_to)

st.set_page_config(page_title="Goodreads Analysis App", layout="wide")


row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

row0_1.title("Speakleash a.k.a. Spichlerz Dashboard")


with row0_2:
    add_vertical_space()

row0_2.subheader(
    "[WWW](https://speakleash.org/) | [GitHub](https://github.com/speakleash) | [Twitter](https://twitter.com/Speak_Leash)"
)

datasets = []
size = []
name = []
category = []

total_size_mb = 0
for d in sl.datasets:
    size_mb = round(d.characters/1024/1024)
    datasets.append("Dataset: {0}, size: {1} MB, characters: {2}, documents: {3}".format(d.name, size_mb, d.characters, d.documents))
    size.append(size_mb)
    name.append(d.name)
    category.append(d.category)
    total_size_mb += size_mb

data = {
  "name": name,
  "category": category,
  "size": size,
}

df = pd.DataFrame(data)

fig1a_1 = px.pie(df, values='size', names='name')
fig1a_2 = px.pie(df, values='size', names='category')

row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))

with row1_1:
    st.markdown(
        "An open collaboration project to build a data set for Language Modeling with a capacity of at least 1TB comprised of diverse texts in Polish. Our aim is to enable machine learning research and to train a Generative Pre-trained Transformer Model from collected data"
    )

    st.header('Total size: {} GB'.format(total_size_mb/1024))

st.write("")
row1a_space1, row1a_1, row1a_space2, row1a_2, row1a_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row1a_1:
    st.plotly_chart(fig1a_1, theme="streamlit", use_container_width=True)

with row1a_2:
    st.plotly_chart(fig1a_2, theme="streamlit", use_container_width=True)

def submit_show(choice):
    #Wiem brzydkie ;-) ale działa
    selected = choice.split(",")[0].split(":")[1].strip()
    st.session_state['selected'] = selected
    print(selected)


choice = None

row2_spacer1, row2_1, row2_spacer2 = st.columns((0.1, 3.2, 0.1))
with row2_1:
    choice = st.selectbox(
        "Select one of our datasets",
        datasets,
    )

    st.button('Details and stats', key='button_show',
          on_click=submit_show, args=(choice, ))


line1_spacer1, line1_1, line1_spacer2, line1_2, line1_spacer2= st.columns((0.1, 1, 0.1, 1, 0.1))

with line1_1:
    if 'selected' in st.session_state:
        st.header("Dataset: {}".format(st.session_state['selected']))
        st.write(sl.get(st.session_state['selected']).manifest)


with line1_2:
    if 'selected' in st.session_state:

        counter = 0
        random_step = random.randrange(1, 1000)
        print(random_step)
        txt = ""
        meta = {}

        ds = sl.get(st.session_state['selected']).ext_data
        for doc in ds:
            txt, meta = doc
            counter += 1
            print(txt[:10])
            if counter == random_step:
                break

        st.subheader("Random document (max 100 chars))")
        st.text_area(txt[:100])
        st.write(meta)


st.write("")
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row3_1:
    if 'selected' in st.session_state:
        st.subheader("Wykres 1")


with row3_2:
    if 'selected' in st.session_state:
        st.subheader("Wykres 1")

add_vertical_space()
row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row4_1:
    st.subheader("TODO")

with row4_2:
    st.subheader("TODO")

add_vertical_space()
