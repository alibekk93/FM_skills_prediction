### import dependancies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### Skill dictionaries for radar graphs
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
FM_columns = ['Name', 'Position', 'Corners', 'Crossing', 'Dribbling', 'Finishing', 'First Touch',
              'Free Kick Taking', 'Heading', 'Long Shots', 'Long Throws', 'Marking', 'Passing',
              'Penalty Taking', 'Tackling', 'Technique', 'Aggressiion', 'Anticipation', 'Bravery',
              'Composure', 'Concentration', 'Vision', 'Decision', 'Determination', 'Flair', 'Leadership',
              'Off The Ball', 'Teamwork', 'Work Rate', 'Positioning', 'Acceleration', 'Agility', 'Balance',
              'Jumping Reach', 'Natural Fitness', 'Pace', 'Stamina', 'Strength']
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
