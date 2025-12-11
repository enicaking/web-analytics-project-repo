
-----

# UC3M Web Analytics Final Project
# California Engineering Salary Predictor

## Overview

This is a data science project carried out by students in their final year of Data Science and Engineering. The final model is a predictor of engineering salaries in California, but the code can be adapted for any industry, in any place. The project involves a complete pipeline from web scraping, to data parsing, cleaning, feature engineering (including advanced natural language processing), to model training using **XGBoost Regression**. Many approaches were tested along the way, all of which are preserved within the filing system.

## Features

  * **LinkedIn Data Scraper:** Acquires updated job postings by searching combinations of job and location and scraping results of first page.
  * **Data Processing Pipeline:** Handles data parsing, cleaning, and standardization (outlier removal).
  * **Salary Standardization:** Converts various salary formats (hourly, monthly, yearly) to a consistent hourly unit.
  * **NLP Feature Engineering:** Uses **FastText** embeddings on job description field to vectorize semantic information.
  * **Machine Learning Model:** Optimized **XGBoost Regressor** for salary prediction.

## Project Structure

The repository is organized to follow the data science workflow.

| Directory/File | Description | Key Contents |
| :--- | :--- | :--- |
| `Scraper scripts/` | Scripts for data acquisition from LinkedIn. | Scraper logic. |
| `Disarded paths/` | Paths that were not pursued in the final analysis. | Unused data/notebooks. |
| `Intermediary notebooks/` | Temporary/development notebooks. | Scratchpad for feature development. |
| `Linkedin data/` | Raw data scraped directly from LinkedIn. | JSON files/initial CSV. |
| `Processed data/` | Cleaned and feature-engineered data ready for modeling. | Final training CSV. |
| `models/` | Saved trained models, checkpoint, and model configuration files. | Neural network models, pipeline objects. |
| `wandb/` | Weights & Biases (W\&B) logging and experiment tracking files. | Hyperparameter sweeps for model. |
| `0_utilities.py` | Utility functions used across multiple notebooks/scripts. | Helper functions for data processing. |
| `1_linkedin_scraper_per_engineer.py` | The main script used to run the data scraper. | Script for data acquisition. |
| `2_deduplicate_and_parsing_linkedin_json_fasttext.py` | Data cleaning, deduplication, JSON parsing, and initial FastText embedding generation. | Data prep script. |
| `3_salary_conversion_dataset_fasttext_30.ipynb` | Notebook for salary standardization and final dataset preparation. | Salary cleaning/standardization logic. |
| `4_XGBoost Linkedin data...ipynb` | **Main modeling notebook.** Contains the training and evaluation of the XGBoost Regression model. | Model training, evaluation, results. |
| `requirements.txt` | List of Python dependencies required to run the project. | Environment setup. |
| `role_family_mapping.csv` | Supplementary data file for mapping job roles and reducing cardinality. | Auxiliary data. |

## Setup and Installation

### Prerequisites

  * Python (3.8+)
  * `pip` (Package installer for Python)

### Steps

1.  **Clone the Repository:**

    ```bash
    git clone [Your Repository URL]
    cd [Your Project Directory]
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    .\venv\Scripts\activate   # On Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

The project is designed to be run sequentially following the numbering of the files.

1.  **Scrape Data:**
    Run the scraper script to acquire new data:

    ```bash
    python 1_linkedin_scraper_per_engineer.py
    ```

    *(Note: You may need to configure credentials or scraper settings within the script.)*

2.  **Process and Embed Data:**
    Run the processing and embedding script:

    ```bash
    python 2_deduplicate_and_parsing_linkedin_json_fasttext.py
    ```

3.  **Final Dataset Preparation and Modeling:**
    Open the Jupyter Notebooks in order (`3_...ipynb` and `4_...ipynb`) to perform salary conversion, final feature engineering, and train the XGBoost model.

    ```bash
    jupyter notebook
    ```

    Navigate to and execute the cells in:

      * `3_salary_conversion_dataset_fasttext_30.ipynb`
      * `4_XGBoost Linkedin data...ipynb`

## Results and Performance

The performance of each model is measured by three key metrics: MAE, RMSE and R-squared.

SHAP is also used to determine feature importance.

Interactive dashboard available to UC3M community at [this link](https://lookerstudio.google.com/reporting/163a0dbf-df24-46f6-b2fe-8bb538628789)

## Contributing

You can contribute to this project by trying out different models, embeddings, or adding data sources!

-----
