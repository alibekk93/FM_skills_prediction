# The Soccer Stats Spectacular

## Table of Contents
1. [Project Overview](#project-overview)
2. [Notebooks](#notebooks)
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

## Notebooks

### 1. Data Preparation [📓](notebooks/01_data_preparation.ipynb)
- Merge separate files for each league and statistic type.
- Calculate percentage above/below team average for each player statistic.
    - The assumption here is that each player has a role within their team's tactic and their statistics will largely depend on the role.
    - Team style also has an affect on statistics and would distort results if not taken into account.
    - Using percentage above/below team mean statistic instead of raw statistics would be a better representation of players' roles within their teams as well as normalize data for us.
- Aggregate original pre-transformation data per team for team-level statistics.
- Apply Principal Component Analysis (PCA) to reduce the dimensionality of player statistics separately for each statistic group:
    - defense
    - touches
    - passing
    - progression
    - attack
    - miscelaneous
- Apply PCA to reduce the dimensionality of team statistics.
- Create tags to combine FBRef statistics with Football Manager and FC24 ratings.

### 2. Team similarity [📓](notebooks/02_team_similarity.ipynb)
- Use aggregated team statistics (pre- or after PCA) to find similar teams using:
    - cosine similarity
    - Euclidean distance

### 3. Data Validation and Exploratory Analysis
- Perform exploratory data analysis (EDA) after each preprocessing step.
- Visualize PCA results to understand player and team distributions.
- Validate the effectiveness of the preprocessing steps.

### 4. Similarity
- Implement functions to identify similar items based on cosine similarity or eucledian distance.
- Identify similar teams and players.

### 5. Modelling
- Create models to predict FM skills
- Create models to predict FC skills

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