### import dependancies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fuzzywuzzy import process
from tqdm import tqdm

### FM skill dictionaries for radar graphs
fm_outfielders_skills_graph_dict = {
    'defending': (('Tackling', 0.50), ('Marking', 0.25), ('Positioning', 0.25)),
    'physical': (('Strength', 0.25), ('Stamina', 0.25), ('Balance', 0.25), ('Agility', 0.25)),
    'speed': (('Acceleration', 0.50), ('Pace', 0.50)),
    'vision': (('Vision', 0.33), ('Flair', 0.33), ('Passing', 0.34)),
    'attacking': (('Finishing', 0.34), ('Off The Ball', 0.33), ('Composure', 0.33)),
    'technique': (('Technique', 0.34), ('First Touch', 0.33), ('Dribbling', 0.33)),
    'aerial': (('Heading', 0.50), ('Jumping Reach', 0.50)),
    'mental': (('Determination', 0.166), ('Decision', 0.166), ('Anticipation', 0.166),
               ('Teamwork', 0.166), ('Bravery', 0.166), ('Concentration', 0.166)),
}

fm_gks_skills_graph_dict = {
    'shotstopping': (('Reflexes', 0.50), ('One On Ones', 0.50)),
    'physical': (('Balance', 0.25), ('Agility', 0.25), ('Strength', 0.25), ('Stamina', 0.25)),
    'speed': (('Acceleration', 0.5), ('Pace', 0.5)),
    'mental': (('Determination', 0.166), ('Decision', 0.166), ('Anticipation', 0.166),
               ('Teamwork', 0.166), ('Bravery', 0.166), ('Concentration', 0.166)),
    'communication': (('Communication', 0.50), ('Command Of Area', 0.50)),
    'eccentricity': (('Eccentricity', 0.50), ('Eccentricity', 0.50)),
    'aerial': (('Handling', 0.50), ('Aerial Reach', 0.50)),
    'distribution': (('Throwing', 0.50), ('Kicking', 0.50)),
}

### Select important columns
FM_columns = ['Corners', 'Crossing', 'Dribbling', 'Finishing', 'First Touch', 'Free Kick Taking',
              'Heading', 'Long Shots', 'Long Throws', 'Marking', 'Passing', 'Penalty Taking',
              'Tackling', 'Technique', 'Aggressiion', 'Anticipation', 'Bravery', 'Composure',
              'Concentration', 'Vision', 'Decision', 'Determination', 'Flair', 'Leadership',
              'Off The Ball', 'Teamwork', 'Work Rate', 'Positioning', 'Acceleration', 'Agility',
              'Balance', 'Jumping Reach', 'Natural Fitness', 'Pace', 'Stamina', 'Strength']
FC_columns = ['attacking_crossing', 'attacking_finishing', 'attacking_heading_accuracy',
              'attacking_short_passing', 'attacking_volleys', 'skill_dribbling', 'skill_curve',
              'skill_fk_accuracy', 'skill_long_passing', 'skill_ball_control', 'movement_acceleration',
              'movement_sprint_speed', 'movement_agility','movement_reactions', 'movement_balance',
              'power_shot_power', 'power_jumping', 'power_stamina', 'power_strength', 'power_long_shots',
              'mentality_aggression', 'mentality_interceptions', 'mentality_positioning', 'mentality_vision',
              'mentality_penalties', 'mentality_composure', 'defending_marking_awareness',
              'defending_standing_tackle', 'defending_sliding_tackle']
defense_columns = ['defense_Blocks_Blocks', 'defense_Tackles_Tkl', 'defense_Tackles_TklW',
                   'defense_Tackles_Def 3rd', 'defense_Tackles_Mid 3rd', 'defense_Tackles_Att 3rd',
                   'defense__Int', 'defense__Clr']
touches_columns = ['possession_Touches_Def Pen', 'possession_Touches_Def 3rd', 'possession_Touches_Mid 3rd',
                   'possession_Touches_Att 3rd', 'possession_Touches_Att Pen', 'possession_Touches_Touches']
passing_columns = ['passing_Total_Att', 'passing_Short_Att', 'passing_Medium_Att', 'passing_Long_Att',
                   'passing__KP', 'passing__CrsPA', 'passing__PrgP']
progres_columns = ['possession_Carries_PrgDist', 'possession_Carries_TotDist', 'possession_Receiving_Rec',
                   'possession_Receiving_PrgR', 'possession_Take-Ons_Att', 'possession_Take-Ons_Succ']
attack_columns = ['gca_SCATypes_TO', 'gca_SCATypes_Sh', 'gca_SCATypes_Fld', 'gca_SCATypes_Def',
                  'gca_SCATypes_PassLive', 'gca_SCATypes_PassDead', 'shooting_Standard_Dist',
                  'shooting_Expected_npxG']
misc_columns = ['playingtime_PlayingTime_Min', 'misc_Performance_Fls', 'misc_Performance_Fld',
                'misc_Performance_Off', 'misc_AerialDuels_Won', 'misc_AerialDuels_Lost']
all_stats_columns = (defense_columns + touches_columns + passing_columns +
                     progres_columns + attack_columns + misc_columns)

### Calculate skill nodes for radar graphs
def calculate_skill_nodes(data: pd.Series, gk: bool = False) -> dict:
    """Calculates node values for a radar plot of FM skills.

    Parameters
    ----------
    data : pd.Series
        Source of data with skills.
    gk : bool, optional
        If True, will treat player as GK, by default False.

    Returns
    -------
    dict
        Dictionary of node values.
    """
    # Check if GK and load corresponding skill dictionary
    skill_dict = fm_gks_skills_graph_dict if gk else fm_outfielders_skills_graph_dict

    # Make a dictionary of nodes
    node_values = {'name': data['Name']}
    for node_name, skills in skill_dict.items():
        node_value = sum(data[skill_name] * weight for skill_name, weight in skills)
        node_values[node_name] = node_value
    return node_values

### Plot radar graph
def plot_fm_radar(data: dict, gk: bool = False) -> None:
    """Plots a stylish radar graph for FM skills.

    Parameters
    ----------
    data : dict
        Dictionary of data with skill nodes.
    gk : bool, optional
        If True, indicates that the player is a goalkeeper.
    """
    # Set colors based on player type
    line_color = '#FF5733' if not gk else '#3333FF'  # Orange for outfielders, Blue for goalkeepers
    fill_color = '#FF5733' if not gk else '#3333FF'
    title_suffix = '' if not gk else ' (GK)'

    # Each attribute we'll plot in the radar chart.
    labels = list(data.keys())[1:]
    values = list(data.values())[1:]
    num_vars = len(labels)

    # Split the circle into even parts and save the angles
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Complete the loop and append the start value to the end.
    values += values[:1]
    labels += labels[:1]
    angles += angles[:1]

    # Create the figure and polar subplot
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))

    # Draw the outline of our data
    ax.plot(angles, values, color=line_color, linewidth=2, linestyle='solid')
    # Fill it in
    ax.fill(angles, values, color=fill_color, alpha=0.4)

    # Fix axis to go in the right order and start at 12 o'clock
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw axis lines for each angle and label
    ax.set_thetagrids(np.degrees(angles), labels, fontsize=12, color='#4B0082')

    # Adjust alignment of labels
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    # Ensure radar goes from 0 to 20
    ax.set_ylim(0, 20)
    ax.set_rgrids([5, 10, 15, 20], color='#AAAAAA', alpha=0.5)

    # Set position of y-labels
    ax.set_rlabel_position(180 / num_vars)

    # Customize appearance
    ax.tick_params(colors='#4B0082')
    ax.tick_params(axis='y', labelsize=10)
    ax.grid(color='#DDDDDD', linestyle='--')
    ax.spines['polar'].set_color('#4B0082')
    ax.set_facecolor('#FAFAFA')

    # Set title with a stylish font
    ax.set_title(data['name'] + title_suffix, y=1.1, fontsize=20, color='#4B0082', fontweight='bold')
    plt.show()

# Get the best match between names given exact DOB
def get_best_match(name, yob, grouped_df, player_col, threshold=80):
    """
    Find the best matching player name from a dataset based on name similarity and year of birth.

    This function attempts to find the closest match for a given player name within a subset of players
    born in the same year. It uses fuzzy string matching to compare names and returns the best match
    if it meets or exceeds the specified similarity threshold.

    Parameters:
    name (str): The name of the player to match.
    yob (int or str): The year of birth of the player.
    grouped_df (pandas.core.groupby.DataFrameGroupBy): A GroupBy object of the DataFrame containing player data,
                                                       grouped by year of birth.
    player_col (str): The name of the column containing player names.
    threshold (int, optional): The minimum similarity score required for a match. Defaults to 80.

    Returns:
    str or None: The name of the best matching player if a match is found and meets the threshold,
                 otherwise None.

    Note:
    - The function uses the fuzzywuzzy library's process.extractOne for string matching.
    - If no players are found for the given year of birth, the function returns None.
    - The grouped_df should be a pandas GroupBy object, grouped by year of birth.

    Example:
    >>> df = pd.DataFrame({'_Player_': ['John Doe', 'Jane Smith'], 'YOB': [1990, 1991]})
    >>> grouped_df = df.groupby('YOB')
    >>> get_best_match('Jon Doe', 1990, grouped_df)
    'John Doe'
    """
    try:
        choices = grouped_df.get_group(yob)[player_col]
    except KeyError:
        return None
    
    if choices.empty:
        return None
    
    match, score = process.extractOne(name, choices.values)
    return match if score >= threshold else None

# Smith-Waterman function
def smith_waterman(s1, s2, match_score=2, gap_cost=1):
    """
    Compute the Smith-Waterman score between two strings.
    
    :param s1: First string.
    :param s2: Second string.
    :param match_score: Score for character match.
    :param gap_cost: Cost for gap (insertion/deletion).
    :return: The Smith-Waterman score for the best local alignment.
    """
    m, n = len(s1), len(s2)
    score_matrix = [[0] * (n + 1) for _ in range(m + 1)]
    max_score = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = score_matrix[i - 1][j - 1] + (match_score if s1[i - 1] == s2[j - 1] else -match_score)
            delete = score_matrix[i - 1][j] - gap_cost
            insert = score_matrix[i][j - 1] - gap_cost
            score_matrix[i][j] = max(0, match, delete, insert)
            max_score = max(max_score, score_matrix[i][j])

    return max_score

# Use Smith-Waterman to find similar strings
def find_most_similar_strings(target, strings, n=5):
    """
    Find the n most similar strings to the target string from a list of strings using Smith-Waterman score.
    
    :param target: The target string to compare against.
    :param strings: A list of strings to search within.
    :param n: The number of most similar strings to return. Default is 5.
    :return: A list of the n most similar strings.
    """
    # Compute the Smith-Waterman score for each string in the list
    scores = [(string, smith_waterman(target, string)) for string in strings]
    
    # Find the n strings with the highest scores
    most_similar = sorted(scores, key=lambda x: x[1], reverse=True)[:n]
    
    # Extract and return only the strings (not the scores)
    return [string for string, score in most_similar]