####################################################
# Author: Adam Smith-Orlik                         #
# Date: 21-04-2025                                 # 
# Description: Helper functions and constants      #
#   for the political compass app                  #
# email: asorlik@yorku.ca                          #
# status: Completed                                #
####################################################

import streamlit as st
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

## Dictionaries 
party_colors = {
    "Liberal": "red",
    "Conservative": "blue",
    "NDP": "orange"
}

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
            "Strongly protects freedom of religion in all domains; faith-based institutions and expression should be fully accommodated",
            "Supports strict secularism; limits religious expression in public institutions (e.g. bans on symbols, prayer)"
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

## Functions
def render_subtopic_input(topic_name, subtopic_name, desc_neg1, desc_pos1):
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {topic_name} — {subtopic_name}")
        st.markdown(f"-1: *{desc_neg1}*")
        st.markdown(f"+1: *{desc_pos1}*")

    with col2:
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

def reorder_positions(reference_dict, target_dict):
    reordered = {}
    for topic in reference_dict:
        reordered[topic] = {}
        for subtopic in reference_dict[topic]:
            if topic in target_dict and subtopic in target_dict[topic]:
                reordered[topic][subtopic] = target_dict[topic][subtopic]
            else:
                raise KeyError(f"Missing {topic}:{subtopic} in target_dict")
    return reordered