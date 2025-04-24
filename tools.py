####################################################
# Author: Adam Smith-Orlik                         #
# Date: 21-04-2025                                 # 
# Description: Tools for calculating the           #
# Euclidean distance and Cosine similarity metris  #
# email: asorlik@yorku.ca                          #
# status: Complete                                 #
####################################################

import numpy as np

def normalize_user_weigths(x: dict) -> dict:
    '''
    Use: Normalized the subtopic weights
    Take:
        - x: user position-weigth dictionary 
    Returns:
        User dictionary with normalized weights 
    '''
    weights = []
    for topic in x.values():
        for subtopic in topic.values():
            weights.append(subtopic['weight'])

    # sum all weights
    total_weights = sum(weights)

    # normalize all weights 
    for topic in x.values():
        for subtopic in topic.values():
            weight = np.round(subtopic['weight'] / total_weights, 5)
            subtopic['weight'] = weight

    return x

def weighted_euclidean_distance(x: dict, y: dict) -> dict:
    '''
    Use: Calculates the weighted Euclidean distance
    Takes:
        - x: your position dictionary 
        - y: party position dictionary 
    Returns:
        topic dictionary with topic-wise weighted Euclidean distance

    '''
    total_subtopics = sum(len(subtopics) for subtopics in x.values())
    distances = {}
    for topic in x.keys():
        distance = 0.0
        for subtopic in x[topic].keys():
            weight = x[topic][subtopic].get('weight', 1.0 / total_subtopics)
            user = x[topic][subtopic]['position']
            party = y[topic][subtopic]['position']
            distance += weight * (user - party) ** 2
        distance = np.sqrt(distance)
        distances[topic] = distance
        
    return distances

def total_euclidean_distance(x: dict) -> float:
    '''
    Use: Calculates the total Euclidean distance
    Takes:
        - x: The weighted Euclidean topic-wise distance dictionary 
    Returns:
        Total Euclidean distance value across all topics
    '''
    total_distance = 0.0
    for topic in x.keys():
        total_distance += x[topic] ** 2
    return np.sqrt(total_distance) / 2 # maximum distance is 2, so divide so that max distance is 1. 

def weighted_cosine_similarity(x: dict, y: dict) -> dict:
    """
    Use: Calculate the cosine similarity between two positions.
    Takes:
        - x: your position dictionary 
        - y: party position dictionary
    Returns:
        - topic dictionary with topic-wise cosine similarity
    """
    similarities = {}
    for topic in x.keys():
        dot_product = 0.0
        norm1 = 0.0
        norm2 = 0.0
        for subtopic in x[topic].keys():
            weight = x[topic][subtopic].get('weight', 1.0)
            user = x[topic][subtopic]['position']
            party = y[topic][subtopic]['position']
            dot_product += weight**2 * user * party
            norm1 += weight**2 * user ** 2
            norm2 += weight**2 * party ** 2
        if norm1 == 0 or norm2 == 0:
            similarity = 0.0
        else:
            similarity = dot_product / (np.sqrt(norm1) * np.sqrt(norm2))
        similarities[topic] = similarity
        
    return similarities

def flatten_positions(x: dict) -> dict:
    flat = {}
    for topic, subtopics in x.items():
        for subtopic, info in subtopics.items():
            key = f"{topic}:{subtopic}"
            flat[key] = info['position']
    return flat

def flatten_weights(x: dict) -> dict:
    flat = {}
    for topic, subtopics in x.items():
        for subtopic, info in subtopics.items():
            key = f"{topic}:{subtopic}"
            flat[key] = info['weight']
    return flat


def total_cosine_similarity(x: dict, y: dict) -> float:
    '''
    Use: Calculate the total weighted cosine similarity between two positions.
    Takes:
        - x: your position dictionary 
        - y: party position dictionary
    Returns:
        - Total cosine similarity value
    '''
    total_subtopics = sum(len(subtopics) for subtopics in x.values())
    default_weight = 1.0 / total_subtopics

    user_positions = flatten_positions(x)
    try:
        weights = flatten_weights(x)
    except KeyError:
        weights = {k: default_weight for k in user_positions.keys()}
        
    party_positions = flatten_positions(y)
    

    dot_product = 0.0
    norm_user = 0.0
    norm_party = 0.0

    for key in user_positions:
        weight = weights[key]
        user = user_positions[key]
        party = party_positions[key]

        dot_product += weight**2 * user * party
        norm_user += weight**2 * user**2
        norm_party += weight**2 * party**2

    if norm_user == 0 or norm_party == 0:
        return 0.0

    return dot_product / (np.sqrt(norm_user) * np.sqrt(norm_party))