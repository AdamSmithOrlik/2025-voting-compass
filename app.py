import streamlit as st
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tools import *
import pickle 
import os

# load the party positions into the app 
data_path = os.path.join(os.path.dirname(__file__), 'data')
with open(data_path + '/aggregate_liberal_positions.pkl', 'rb') as f:
    liberal_positions = pickle.load(f)

with open(data_path + '/aggregate_conservative_positions.pkl', 'rb') as f:
    conservative_positions = pickle.load(f)

with open(data_path + '/aggregate_ndp_positions.pkl', 'rb') as f:
    ndp_positions = pickle.load(f)

## Helper functions
def render_subtopic_input(topic_name, subtopic_name, desc_neg1, desc_pos1):
    st.markdown(f"### {topic_name} — {subtopic_name}")
    st.markdown(f"-1: *{desc_neg1}*")
    st.markdown(f"+1: *{desc_pos1}*")

    position = st.slider(
        f"Select your stance on {subtopic_name}",
        min_value=-1.0,
        max_value=1.0,
        value=0.0,
        step=0.05,
        key=f"{topic_name}_{subtopic_name}_position"
    )

    weight = st.slider(
        f"How important is {subtopic_name} to you?",
        min_value=0.0,
        max_value=1.0,
        value=1.0,
        step=0.05,
        key=f"{topic_name}_{subtopic_name}_weight"
    )

    return {
        'position': position,
        'weight': weight
    }

# Dictionary of topics and subtopics
topic_definitions = {
    "Economic": {
        "Taxation": (
            "Flat taxes, minimal redistribution, low corporate tax rates",
            "Progressive taxation, wealth taxes, high redistribution"
        ),
        "Spending": (
            "Austerity, reduce government spending, privatization",
            "Expansive public investment, social programs, stimulus spending"
        ),
        "MinimumWage": (
            "Abolish or minimize minimum wage; let markets decide",
            "Substantially increase minimum wage; living wage guarantees"
        ),
        "FiscalDiscipline": (
            "Low debt tolerance, strict balanced budgets, cut deficits",
            "Flexible deficits to support social or environmental goals"
        ),
        "LabourPolicy": (
            "Limit union power; flexible labor markets",
            "Strengthen unions, protections for gig economy and low-wage workers"
        ),
    },
    "Social": {
        "Healthcare": (
            "Privatized healthcare system, minimal public provision",
            "Fully public healthcare with universal access"
        ),
        "Education": (
            "Privatized schools, school choice, reduced state role",
            "Public education as a right, tuition-free post-secondary"
        ),
        "CurriculumControl": (
            "Parents should have strong oversight; restrict identity/sexuality content in K-12",
            "Support inclusive curriculum reflecting social diversity; trust educators"
        ),
        "Housing": (
            "Let the market solve housing; deregulation, tax credits",
            "Aggressive public housing, rent control, zoning reform"
        ),
        "Indigenous": (
            "Equal treatment under Canadian law, no special recognition",
            "Nation-to-nation status, land restitution, UNDRIP adoption"
        ),
        "Immigration": (
            "Tightly restricted immigration, values screening",
            "High skilled and humanitarian immigration, multiculturalism"
        ),
        "LGBTQ": (
            "Limit government support; oppose education/mandates",
            "Strong legal protections, cultural support, inclusive policy"
        ),
        "Drugs": (
            "Criminalize drug use, tough on crime, no harm reduction",
            "View addiction as public health issue, harm reduction"
        ),
        "DEI": (
            "Opposes DEI mandates; prefers individual merit, colorblind approaches",
            "Strongly supports DEI programs; believes systemic disparities require proactive correction"
        ),
    },
    "Environment": {
        "Emissions": (
            "Avoid emissions caps; prioritize economic growth",
            "Aggressively reduce emissions, international targets"
        ),
        "CarbonTax": (
            "No carbon tax; burdens citizens and business",
            "Carbon tax is essential market solution to climate change"
        ),
        "FossilFuels": (
            "Support oil/gas industry, reduce regulation, pipelines",
            "Phase out fossil fuels, divestment, end subsidies"
        ),
        "GreenInvestment": (
            "Let market innovate green tech on its own",
            "Government should invest heavily in green transition"
        ),
    },
    "Foreign": {
        "SpendingM": (
            "Cut military spending, avoid foreign entanglements",
            "Increase defense funding, strong global presence"
        ),
        "RefugeePolicy": (
            "Tight border controls; reduce intake to preserve resources and safety",
            "Expand humanitarian response; Canada has global responsibility"
        ),
        "Aid": (
            "Reduce foreign aid, focus on domestic issues",
            "Expand international aid, climate and human rights"
        ),
        "Trade": (
            "Protect domestic industry, skeptical of globalization",
            "Pro free trade, liberalize markets, global partnerships"
        ),
        "IsraelPalestine": (
            "Unconditional support for Israel, skeptical of Palestine",
            "Strong defense of Palestinian rights, cease occupation"
        ),
        "UkraineRussia": (
            "Stay neutral or reduce involvement",
            "Strong support for Ukraine against Russian aggression"
        ),
    },
    "Justice": {
        "CriminalJustice": (
            "Tough on crime, longer sentences, more policing",
            "Restorative justice, address systemic causes"
        ),
        "FreeSpeech": (
            "Minimal regulation; platform and individual freedom paramount",
            "Government oversight of speech to reduce harm/misinformation"
        ),
        "PoliceReform": (
            "Expand funding and tools for policing; prioritize enforcement and public order",
            "Reform or reduce police funding; invest in alternatives like mental health and community response"
        ),
        "ReligiousLiberty": (
            "Supports strict secularism; limits religious expression in public institutions (e.g. bans on symbols, prayer)",
            "Strongly protects freedom of religion in all domains; faith-based institutions and expression should be fully accommodated"
        ),
    },
    "Science": {
        "Research": (
            "Private sector should fund most research",
            "Publicly funded science is essential to progress"
        ),
        "AI": (
            "Let industry regulate itself; avoid overregulation",
            "Proactive government regulation and AI investment"
        ),
        "Internet": (
            "Market-driven infrastructure; minimal subsidies",
            "Universal internet access as a public good"
        ),
        "Privacy": (
            "Minimal regulation of corporate or state data collection; prioritize security and innovation",
            "Strict data protection laws; transparency and user consent are fundamental rights"
        ),
    },
    "Governance": {
        "Electoral": (
            "Status quo (FPTP); no need for reform",
            "Proportional representation, electoral modernization"
        ),
        "Transparency": (
            "Minimal public reporting; prioritize security",
            "Government must be transparent and accountable"
        ),
        "Federalism": (
            "Strong centralized federal government",
            "More power and autonomy to provinces"
        ),
    },
}

subtopic_display_names = {
    "Healthcare": "Healthcare System",
    "Education": "Education Policy",
    "Housing": "Affordable Housing",
    "Indigenous": "Indigenous Rights",
    "Immigration": "Immigration Policy",
    "DEI": "Diversity, Equity, and Inclusion",
    "LGBTQ": "LGBTQ Rights and Freedoms",
    "Drugs": "Drug Abuse and Addiction",
    "Taxation": "Tax Policy",
    "LabourPolicy": "Labour Policy and Unions",
    "CurriculumControl": "Curriculum Control and Parental Rights",
    "RefugeePolicy": "Refugee Policy and Border Control",
    "Spending": "Government Spending",
    "MinimumWage": "Minimum Wage",
    "FiscalDiscipline": "Fiscal Responsibility",
    "Emissions": "Carbon Emissions",
    "CarbonTax": "Carbon Tax",
    "FossilFuels": "Fossil Fuels",
    "GreenInvestment": "Green Investment",
    "Research": "Research Funding",
    "AI": "AI Investment & Regulation",
    "Internet": "Internet Access",
    "SpendingM": "Military Spending",
    "Aid": "International Aid",
    "Trade": "Trade Policy",
    "IsraelPalestine": "Israel / Palestine Conflict",
    "UkraineRussia": "Ukraine / Russia War",
    "CriminalJustice": "Criminal Justice Reform",
    "PoliceReform": "Police Reform",
    "FreeSpeech": "Free Speech",
    "Privacy": "Privacy and Data Protection",
    "DrugPolicy": "Drug Policy Reform",
    "ReligiousLiberty": "Religious Liberty",
    "Electoral": "Electoral Reform",
    "Transparency": "Government Transparency",
    "Federalism": "Federalism (Provincial vs Federal Power)"
}

def print_dict_structure(name, d):
    st.markdown(f"### 📂 Structure of `{name}`")
    for topic, subtopics in d.items():
        st.write(f"- **{topic}**: {len(subtopics)} subtopics")
        for subtopic, value in subtopics.items():
            st.write(f"  - `{subtopic}` → type: `{type(value)}` | content: `{value}`")

def find_missing_keys(source, target):
    for topic in source:
        for subtopic in source[topic]:
            if topic not in target or subtopic not in target[topic]:
                st.warning(f"Missing: {topic}:{subtopic} in party data.")

party_colors = {
    "Liberal": "red",
    "Conservative": "blue",
    "NDP": "orange"
}

# Function to plot the number line
def plot_clean_number_line(topic_key, subtopic_key, user_val, party_vals, subtopic_display_names):
    subtopic_label = subtopic_display_names.get(subtopic_key, subtopic_key)

    fig, ax = plt.subplots(figsize=(6, 0.6))

    ax.axhline(0, color='black', linewidth=1)
  
    ax.plot(user_val, 0, 'o', color='black', markersize=8, alpha=0.6, label='You')

    for party, val in party_vals.items():
        ax.plot(val, 0, 'o', color=party_colors[party], markersize=8, alpha=0.6, label=party)

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.3, 0.3)
    ax.set_yticks([])
    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels(["-1", "0", "1"], fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.tick_params(axis='x', pad=2)

    ax.set_title(f"{subtopic_label}", fontsize=10)
    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=4, frameon=False)
    # plt.tight_layout()
    plt.tight_layout(pad=0.2)

    return fig

 # Utility: compute weighted average per category
def category_weighted_means(position_dict):
    category_means = {}
    for category, subtopics in position_dict.items():
        positions = [sub['position'] for sub in subtopics.values()]
        weights = [sub['weight'] for sub in subtopics.values()]
        category_means[category] = np.average(positions, weights=weights)
    return category_means

# Optional utility to add weights=1.0 to party dicts
def fill_party_weights(party_dict):
    return {
        cat: {sub: {'position': info['position'], 'weight': 1.0} for sub, info in subs.items()}
        for cat, subs in party_dict.items()
    }

def plot_pca_2d(user_positions, party_positions_dict, title="2D PCA: Political Alignment"):
    """
    Plot a 2D PCA with vector arrows from origin to each actor (user + parties),
    applying √weight scaling to each subtopic to match importance.
    """
    def flatten_weighted_positions(d):
        return [
            v['position'] #np.sqrt(v.get('weight', 1.0)) * v['position']
            for cat in d.values()
            for v in cat.values()
        ]
    
    labels = ["You"] + list(party_positions_dict.keys())
    colors = ['black', 'red', 'blue', 'orange']

    data = [flatten_weighted_positions(user_positions)] + [
        flatten_weighted_positions(party_dict) for party_dict in party_positions_dict.values()
    ]
    
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(data)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_title(title)
    ax.set_xlabel("Principal Component A")
    ax.set_ylabel("Principal Component B")
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.5)
    ax.axvline(0, color='grey', linestyle='--', linewidth=0.5)
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

    for (x, y), color in zip(reduced, colors):
        ax.arrow(0, 0, x, y, head_width=0.05, head_length=0.05, fc=color, ec=color, linewidth=2)

    ax.set_aspect('equal', adjustable='datalim')
    return fig

def plot_pca_3d(user_positions, party_positions_dict, title="3D PCA: Political Alignment"):
    """
    Plot a 3D PCA with vector arrows from origin for user and party positions.
    Applies √weight × position to reflect topic importance.
    """
    def flatten_weighted_positions(d):
        return [
            v['position']
            for cat in d.values()
            for v in cat.values()
        ]

    labels = ["You"] + list(party_positions_dict.keys())
    colors = ['black', 'red', 'blue', 'orange']
    
    data = [flatten_weighted_positions(user_positions)] + [
        flatten_weighted_positions(party_dict) for party_dict in party_positions_dict.values()
    ]

    pca = PCA(n_components=3)
    reduced = pca.fit_transform(data)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title)

    for (x, y, z), color in zip(reduced, colors):
        ax.quiver(0, 0, 0, x, y, z, color=color, arrow_length_ratio=0.1, linewidth=2)

    ax.set_xlabel("Principal Component A")
    ax.set_ylabel("Principal Component B")
    ax.set_zlabel("Principal Component C")

    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])
    ax.set_zlim([-4, 4])

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax.view_init(elev=20, azim=135)
    ax.grid(False)
    ax.set_box_aspect([1,1,1])
    plt.tight_layout()
    return fig

########################################################################
########################################################################
# APP STARTS HERE
# Set page title and layout
st.set_page_config(page_title="2025 Elections Compass", layout="wide")

st.title("2025 Canadian Federal Elections Compass")
st.markdown("""### by Adam Smith-Orlik""")

# Introduction
st.markdown(
    """
    ### Introduction
    Welcome to the 2025 Canadian Federal Elections Compass—a data-driven and bias-mitigating tool to help quantify your political prefereneces and compare with the positions of the major parties in the upcoming elections. The party positions are based on AI-generated estimates from multiple models, and the compass allows you to assign weights to the topics that matter most to you. For detailed infromation on how the compass was designed see my blog post [here](<insert blog link>).
    """
)

st.markdown("☕  **If you find this app useful please consider supporting me:** [Buy me a coffee](https://buymeacoffee.com/adamsmithorlik)")

# drop down menus
with st.expander("How to Use this Compass", expanded=False):
    st.markdown(
        """
        1. **Survey**: Read the extreme positions on each subtopic and select your position on a scale from -1 to 1, where 0 is the status quo.
        2. **Weighting**: Rate the importance of each subtopic to your overall political position on a scale from 0 to 1. 0 being not important and 1 being very important.
        3. **Results**: After submitting your responses, the compass will compute the distance metrics and display your results. To understand the distance metrics, please see the "Methods" section.
        """
    )
with st.expander("Motivation", expanded=False):
    st.markdown(
        """
        Using other online compasses I noticed that the questions posed were leading, too specific for someone who is not a politics wonk, overly focused on hot-button issues, or simply not representative of most peoples politcal values. What is more, there was no clear way to quantify the importnace of some topics over others. I wanted to create a compass that better captures the full spectrum of politcal values and allows the user to assign weights to topics that matter the most to them.
        """
    )

with st.expander("Methods", expanded=False):
    st.markdown(
        """
        In the interest of transparency I will describe exactly how the compass operates, and for those interested the full code with be availble publically at <Github Link Here>. 

        ## Topic Selection 
        - The compass is based on a set of 7 topics with subtopics that are relevant to the Canadian political landscape:
            1. Economic Policy
                - Fiscal Policy
                - Taxation
                - Minmum Wage
                - Spending 
                - Labour Policy
            2. Social Policy
                - Healthcare
                - Education
                - Curriculum Control
                - Housing
                - Immigration
                - Indigenous Rights
                - LGBTQ+ Rights
                - Homleessness and Drug Addiction
                - Diversity, Equity, and Inclusion
            3. Foreign Policy
                - Military Spending
                - Foreign Aid
                - Trade Policy
                - Israel/Palestine
                - Ukraine/Russia
                - Refugees and Border Control
            4. Environment
                - Emissions
                - Carbon Tax
                - Fossil Feuls 
                - Green Investment
            5. Justice and Civil Liberty
                - Crinimal Justice 
                - Civil Liberties 
                - Free Speech 
                - Police Reform
            6. Science and Technology
                - Research Funding
                - AI Regulation
                - Internet Access
                - Privacy and Data Protection
            7. Governance 
                - Electoral Reform
                - Government Transparency
                - Federalism 

        ## User Input
        The compass asks the use to rate their position on each of the abovementioned subtopics on a scale from -1 to 1 representing the extreme positions (as articualted below) and where 0 is the status quo.

        The use will also be asked to rate the subtopic from 0 to 1 representing the importance of that subtopic to their overall political position. E.g. a single issue voter is free to set one subtopic to 1 and the rest to 0. 

        ## Party Positions
        In an effort to be as unbiased as possible I have used AI to estimate the current party positions from online sources. Further, I have used 3 different AI models--ChatGPT, Claude, and Perplexity--and aggreagated the results to get a more accurate picture of the party positions.

        ## Distance Metrics 
        I elect to use two different metrics the measure the distance between the users responses and the party positions. 1) Weighted Euclidean distance and 2) weighted Cosine Similarity. For more detial please see my blog post <link here>. 

        - The weighted Euclidean distance returns a result ranging from 0 (perflectly overlapping values) to 1 (maximally distant values).
        - The weighted Cosine Similarity returns a result ranging from -1 (anti-aligned) to 1 (perfectly aligned).

        # Comparison
        The compass will compute the weighted distances for each subtopic separately and then a total distance across all topics. These numbers will tell the user how closely aligned they are with each party.

        The compass will also display a number of plots calculated from the data, but these need to be interpreted carefully; the visual results do not always retain the weightings, and where relevant a cautionary note will be made. 
        """
    )
with st.expander("Cautionary Notes", expanded=False):
    st.markdown(
        """
        - I am not a political scientist, and this compass is not intended to be a definitive measure of your political beliefs or values. It is simply a tool to help you better understand your own views and how they compare to those of the major parties in Canada.
        - The compass is not a substitute for actual political engagement and should not be used as the sole basis for making voting decisions.
        - This compass uses AI to estimate party positions, which may not be accurate or up-to-date. The compass is not affiliated with any political party and does not endorse any specific candidate or platform.
        - The compass is based on a limited set of topics and subtopics, which may not capture the full spectrum and complexity of political beliefs and values.
        - Despite intending to be as unbiased as possible, the compass may still reflect the biases of the data sources used to estimate party positions.
        - Many things go into making an informed political decision. I made this out of an effort to do my civil duty of making the best decision I can, and I hope you will too.
        """

    )

# USER INPUT
st.header("Your Political Compass")

user_inputs = {}

with st.form("survey"):
    st.header("Survey")

    st.markdown(
        """
        Please rate your position on the following topics. When done hit the "Submit my Positions" button at the bottom.

        Remember:
        -1 and 1 represent the extreme positions on either side of the spectrum.
        0 represents the status quo, i.e. the current position of the government.
        """
    )

    # For each topic
    for topic_name, subtopics in topic_definitions.items():
        user_inputs[topic_name] = {}
        for subtopic_name, (desc_neg1, desc_pos1) in subtopics.items():
            display_name = subtopic_display_names.get(subtopic_name, subtopic_name)  # fallback to key if not found
            user_inputs[topic_name][subtopic_name] = render_subtopic_input(
                topic_name,
                display_name,  # shown to user
                desc_neg1,
                desc_pos1
            )


    submitted = st.form_submit_button("Submit my Positions")
    ################################################################
    ################################################################
    # START OF RESULTS
    st.divider()
    if submitted:
        st.header("Distance Metrics Main Results")
        # normalize the users weights 
        normalized_inputs = normalize_user_weigths(user_inputs)
        # COMPUTE THE DISTANCE METRICS
        # calculate the total distances 
        euclidean_distance_liberal = weighted_euclidean_distance(normalized_inputs, liberal_positions)
        euclidean_distance_conservative = weighted_euclidean_distance(normalized_inputs, conservative_positions)
        euclidean_distance_ndp = weighted_euclidean_distance(normalized_inputs, ndp_positions)
        # calcualte the total euclidean distances 
        total_euclidean_distance_liberal = total_euclidean_distance(euclidean_distance_liberal)
        total_euclidean_distance_conservative = total_euclidean_distance(euclidean_distance_conservative)
        total_euclidean_distance_ndp = total_euclidean_distance(euclidean_distance_ndp)
        # write the results to the screen

        # cosine similarities 
        cosine_similarity_liberal = weighted_cosine_similarity(normalized_inputs, liberal_positions)
        cosine_similarity_conservative = weighted_cosine_similarity(normalized_inputs, conservative_positions)
        cosine_similarity_ndp = weighted_cosine_similarity(normalized_inputs, ndp_positions)

        # calcualte the total cosine similarities
        total_cosine_similarity_liberal = total_cosine_similarity(normalized_inputs, liberal_positions)
        total_cosine_similarity_conservative = total_cosine_similarity(normalized_inputs, conservative_positions)
        total_cosine_similarity_ndp = total_cosine_similarity(normalized_inputs, ndp_positions)
        
        st.markdown("## Weighted Euclidean Distance")
        st.metric("Liberal Party", round(total_euclidean_distance_liberal, 3))
        st.metric("Conservative Party", round(total_euclidean_distance_conservative, 3))
        st.metric("NDP", round(total_euclidean_distance_ndp, 3))

        euclidean_scores = {
            'Liberal Party':  total_euclidean_distance_liberal,
            'Conservative Party': total_euclidean_distance_conservative,
            'NDP': total_euclidean_distance_ndp
        }

        euclidean_furthest, euclidean_furthest_value = max(euclidean_scores.items(), key=lambda item: item[1])
        euclidean_closest, euclidean_closest_value = min(euclidean_scores.items(), key=lambda item: item[1])
        # Euclidean Results Summary Box
        st.markdown("### Euclidean Distance Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.success(f"**Closest Party:** {euclidean_closest}")

        with col2:
            st.error(f"**Furthest Party:** {euclidean_furthest}")

        st.markdown(
            f"""
            Your views are **closest** to the *{euclidean_closest}* based on the weighted Euclidean distance.
            A lower score means you're **closer** in position to that party across all topics .
            """
        )


        st.markdown("## Weighted Cosine Similarity")
        st.metric("Liberal Party", round(total_cosine_similarity_liberal, 3))
        st.metric("Conservative Party", round(total_cosine_similarity_conservative, 3))
        st.metric("NDP", round(total_cosine_similarity_ndp, 3))

        cosine_scores = {
            'Liberal Party':  total_cosine_similarity_liberal,
            'Conservative Party': total_cosine_similarity_conservative,
            'NDP': total_cosine_similarity_ndp
        }

        cosine_closest, cosine_closest_value = max(cosine_scores.items(), key=lambda item: item[1])
        cosine_furthest, cosine_furthest_value = min(cosine_scores.items(), key=lambda item: item[1])


        # Cosine Similarity Results Summary Box
        st.markdown("### Cosine Similarity Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.success(f"**Closest Party:** {cosine_closest}")

        with col2:
            st.error(f"**Furthest Party:** {cosine_furthest}")

        st.markdown(
            f"""
            Based on directional similarity, your views are **most aligned** with *{cosine_closest}*.
            A score closer to **1.0** means your weighted **policy vector points in a similar direction**.
            """
        )

        st.markdown("## Per Topic Comparison")

        st.markdown(
            """
            The following table shows the Euclidean distance and Cosine Similarity for topic for each party. This captures the per-topic differences between your views and the party positions given the weights you assigned to each subtopic.
            """
        )
        # Euclidean distance per topic
        topics = euclidean_distance_liberal.keys()
        table_data = []

        with st.expander(" View Per-Topic Distance and Similarity Table"):
            topics = euclidean_distance_liberal.keys()
            table_data = []

            for topic in topics:
                ed_scores = {
                    'Liberal': euclidean_distance_liberal[topic],
                    'Conservative': euclidean_distance_conservative[topic],
                    'NDP': euclidean_distance_ndp[topic]
                }
                cs_scores = {
                    'Liberal': cosine_similarity_liberal[topic],
                    'Conservative': cosine_similarity_conservative[topic],
                    'NDP': cosine_similarity_ndp[topic]
                }

                closest_ed = min(ed_scores, key=ed_scores.get)
                closest_cs = max(cs_scores, key=cs_scores.get)

                table_data.append({
                    'Topic': topic,
                    'LP (ED)': f"{ed_scores['Liberal']:.2f}",
                    'CP (ED)': f"{ed_scores['Conservative']:.2f}",
                    'NDP (ED)': f"{ed_scores['NDP']:.2f}",
                    'Closest (ED)': closest_ed,
                    'LP (CS)': f"{cs_scores['Liberal']:.2f}",
                    'CP (CS)': f"{cs_scores['Conservative']:.2f}",
                    'NDP (CS)': f"{cs_scores['NDP']:.2f}",
                    'Closest (CS)': closest_cs
                })


            df_results = pd.DataFrame(table_data)
            df_results.reset_index(drop=True, inplace=True)
            # st.dataframe(df_results.style.hide(axis="index"), use_container_width=True)
            st.table(df_results.style.hide(axis="index"))


        # note on results 
        st.markdown(
            """
            **Note:** The Euclidean distance and the Cosine Similarity can disagree on which party you are "closest" to. This is because the Euclidean distance is a measure of absolute distance, while the Cosine Similarity is a measure of directional similarity. In other words, the Euclidean distance tells you how far apart two points are in space, while the Cosine Similarity tells you how similar the angles between two vectors are in a multi-dimensional space.
            """
        )
        ################################################################
        ################################################################
        # START OF VISUALIZATION
        st.divider()
        st.header("Visualizing the Data")

        st.markdown("### Subtopic Numberline Plots")

        st.markdown(
            """
            The following plots show your position compared to the party positions on each subtopic. The party positions are the aggregated AI-generated estimates of their positions. 
            """
        )

        for topic in normalized_inputs.keys():
            with st.expander(topic): 
                for subtopic in normalized_inputs[topic].keys():
                    user_val = normalized_inputs[topic][subtopic]['position']
                    party_vals = {
                        "Liberal": liberal_positions[topic][subtopic]['position'],
                        "Conservative": conservative_positions[topic][subtopic]['position'],
                        "NDP": ndp_positions[topic][subtopic]['position'],
                    }
                    fig = plot_clean_number_line(
                        topic,
                        subtopic,
                        user_val,
                        party_vals,
                        subtopic_display_names
                    )
                    st.pyplot(fig)
                    plt.close(fig)

        st.markdown(
            """
            NOTE: The numberline plots do not include the weights assigned to each subtopic. Interpret accordingly.
            """
        )

        st.markdown("### Radar Plot")

        st.markdown(
            """
            The follow plot shows your mean **unweighted** topic position compared to the party positions. 

            The center of the plot represents the -1 positions and the outer edge represents the +1 positions. 
            """
        )


        # Compute weighted means
        my_avg = category_weighted_means(normalized_inputs)
        lib_avg = category_weighted_means(fill_party_weights(liberal_positions))
        con_avg = category_weighted_means(fill_party_weights(conservative_positions))
        ndp_avg = category_weighted_means(fill_party_weights(ndp_positions))

        # Radar plot setup
        labels = list(my_avg.keys())
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]  # close the loop

        def close(values): return values + values[:1]

        with st.expander("Radar Plot: Alignment by Topic"):
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

            ax.plot(angles, close([my_avg[k] for k in labels]), color='black', label="You")
            ax.plot(angles, close([lib_avg[k] for k in labels]), color='red', label="Liberal")
            ax.plot(angles, close([con_avg[k] for k in labels]), color='blue', label="Conservative")
            ax.plot(angles, close([ndp_avg[k] for k in labels]), color='orange', label="NDP")
            ax.fill(angles, close([my_avg[k] for k in labels]), color='black', alpha=0.1)

            # remove the axis numbers titles 
            ax.set_yticklabels([])

            ax.set_thetagrids(np.degrees(angles[:-1]), labels)
            ax.set_ylim(-1, 1)
            ax.set_title("Political Alignment by Topic", size=12)
            ax.legend(loc='lower left', bbox_to_anchor=(0.9, 0.1))
            ax.grid(color='k', linestyle='-', linewidth=0.5, alpha=0.2)
            st.pyplot(fig)

        st.markdown("### 2D PCA Plot")
        st.markdown(
            """
            The following plot shows the unweighted principle component analysis of your position compared to the party positions. The axes represent the first two principal components of the data that capture the most variance in the data.

            """
        )
        # PCA plot
        with st.expander("PCA Projection of Political Alignment (2D)"):
            pca_fig = plot_pca_2d(
                user_positions=user_inputs,
                party_positions_dict={
                    'Liberal': fill_party_weights(liberal_positions),
                    'Conservative': fill_party_weights(conservative_positions),
                    'NDP': fill_party_weights(ndp_positions)
                }
            )
            st.pyplot(pca_fig)

        st.markdown("### 3D PCA Plot")
        st.markdown("""
            Same as the above but in 3D. The axes represent the first three principal components of the data that capture the most variance in the data.
        """
        )

        with st.expander("3D PCA Projection of Political Alignment"):
            pca_fig_3d = plot_pca_3d(
                user_positions=user_inputs,
                party_positions_dict={
                    'Liberal': fill_party_weights(liberal_positions),
                    'Conservative': fill_party_weights(conservative_positions),
                    'NDP': fill_party_weights(ndp_positions)
                }
            )
            st.pyplot(pca_fig_3d)

        st.markdown(
            """
            **Note:** The PCA plots do not include the weights assigned to each subtopic. Interpret accordingly.
            """
        )
        



