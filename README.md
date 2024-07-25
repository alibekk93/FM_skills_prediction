# The Soccer Stats Spectacular

## Table of Contents
1. [Project Overview](#project-overview)
2. [Data Preprocessing](#data-preprocessing)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contribution](#contribution)
6. [License](#license)
7. [Contact](#contact)

## Project Overview

Welcome to the Soccer Stats Spectacular! This project dives into the world of soccer to analyze player performance and predict their skills. We're combining real-world match statistics with player ratings from Football Manager 2023 and FC24 to create a comprehensive model for player evaluation and comparison.

### What’s the Game Plan?
1. **Predict Player Skills**: Can we use real match data to predict how players are rated in video games? Let's find out!
2. **Find Player and Team Twins**: Ever wondered which players or teams are secretly alike? We'll uncover those hidden similarities.
3. **Bridge the Gap**: Explore the fascinating relationship between on-field performance and virtual ratings.

Get ready for a deep dive into soccer stats, where data science meets the beautiful game!

## Data Preprocessing

### 1. Data Consolidation [📓](notebooks/01_data_consolidation.ipynb)
- Merge separate files for each league and statistic type.
- Combine FBRef statistics with Football Manager and FC24 ratings.
- Ensure consistent player and team naming across all datasets.

### 2. Feature Engineering
- Calculate percentage above/below team average for each player statistic:
    ```python
    def percent_above_below(group):
        return (group - group.mean()) / group.mean()
  
    player_data_transformed = player_data.groupby('team').  transform(percent_above_below)
    ```
- Aggregate original pre-transformation data per team for team-level statistics.

### 3. Dimensionality Reduction for Player Statistics
- Apply Principal Component Analysis (PCA) to reduce the dimensionality of player statistics:
    ```python
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    player_data_scaled = scaler.fit_transform(player_data_transformed)

    pca_player = PCA(n_components=0.95)  # Retain 95% of variance
    player_pca = pca_player.fit_transform(player_data_scaled)
    ```

### 4. Team Style and Strength Encoding
- Apply PCA to reduce the dimensionality of team statistics.
- Append the resulting team PCA components to individual player data:
    ```python
    team_data_scaled = scaler.fit_transform(team_data)
    pca_team = PCA(n_components=5)  # Adjust number of components as needed
    team_pca = pca_team.fit_transform(team_data_scaled)

    player_data_final = pd.concat([
        pd.DataFrame(player_pca),
        pd.DataFrame(team_pca[player_data['team_id']])
        ], axis=1)
    ```

### 5. Data Validation and Exploratory Analysis
- Perform exploratory data analysis (EDA) after each preprocessing step.
- Visualize PCA results to understand player and team distributions.
- Validate the effectiveness of the preprocessing steps.

### 6. Data Versioning
- Implement a versioning system for datasets at each preprocessing stage.
- Ensure reproducibility of results and enable easy backtracking if needed.

## Installation
To get started with the Soccer Stats Spectacular, follow these steps:
1. Clone the repository:
```bash
git clone https://github.com/your-username/soccer-stats-spectacular.git
```
2. Navigate to the project directory:
```bash
cd soccer-stats-spectacular
```
3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage
To run the analysis and start making predictions, execute the following command:
```bash
python main.py --data-source "FBRef" --season "2023-24" --predict-skills
```
This will kick off the data processing and prediction pipeline, producing results that you can analyze further.

## Contribution
We welcome contributions from fellow soccer enthusiasts and data scientists! To contribute:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License. See the LICENSE.md file for details.

## Contact
For questions, support, or just to say hello, reach out to us at:
- Email: datafanatic@soccerstats.com
- Twitter: @SoccerStatSpectacular

We hope you enjoy diving into the world of soccer stats with us!