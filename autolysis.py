# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "python-dotenv",
#   "pandas",
#   "requests",
#   "numpy",
#   "matplotlib",
#   "seaborn",
#   "scikit-learn"
# ]
# ///

# Load proxy token from .env file
from dotenv import load_dotenv
import pandas as pd
import os
import sys

import requests
import re
import base64
import traceback


load_dotenv()  # Load .env file
proxy_token = os.getenv("AIPROXY_TOKEN")

analysis_types = """
1. Outlier and Anomaly Detection
Outlier and anomaly detection techniques help identify data points that deviate significantly from the rest of the data, which may indicate errors, fraud, or interesting patterns.

- What are the outliers or anomalies in the dataset?
- Which data points deviate from the general trend or expected behavior?
- Are there any unusual or extreme values in the dataset that could indicate errors or rare events?
- How can we identify potential fraud or mistakes in the dataset based on outliers?
- What methods can we use to remove or handle outliers without distorting the overall analysis?
- How does the presence of outliers affect the results of the analysis or model?

2. Correlation Analysis, Regression Analysis, and Feature Importance Analysis
These techniques analyze relationships between variables and help predict outcomes based on feature dependencies.

- What are the relationships between different variables in the dataset?
- Which variables are most strongly correlated with each other?
- How do independent variables influence a dependent variable in a regression model?
- Which features are the most important predictors of a target variable?
- Can we predict one variable based on others? If so, which variables provide the best predictive power?
- What are the coefficients of a regression model, and what do they tell us about the relationship between variables?
- How can we assess multicollinearity and its impact on the regression model?

3. Time Series Analysis
Time series analysis is used to analyze data points collected or recorded at specific time intervals, helping uncover trends, cycles, and seasonal patterns.

- What are the long-term trends in the data?
- Are there any seasonal patterns or periodic cycles in the data?
- Can we predict future values or trends based on historical data?
- How do we model time-dependent data and account for seasonality and trends?
- Are there any sudden shifts or anomalies in the time series data (e.g., structural breaks)?
- What is the forecast for future values in the time series?
- How do different time intervals (e.g., daily, monthly, yearly) affect the analysis?

4. Cluster Analysis
Cluster analysis groups similar data points together, helping identify natural groupings or patterns in the data, often used in market segmentation, customer analysis, or pattern recognition.

- How can we group the data into distinct clusters based on similar characteristics?
- What are the different segments or categories that naturally exist in the dataset?
- How can we identify homogeneous groups in the dataset that share common features?
- What characteristics define each of the identified clusters?
- How many clusters should we use, and how do we evaluate the quality of clustering?
- What is the distance or similarity between different clusters?
- What happens to the data when it is clustered using different methods (e.g., K-means, hierarchical)?

5. Geographic Analysis
Geographic analysis looks at spatial relationships between data points, helping to understand the geographic distribution and relationships between locations.

- What patterns exist in the data based on geographical location?
- Are there geographic areas where specific events or trends are more prominent?
- How are variables distributed across different geographic regions or areas?
- Can we identify areas of interest or concern based on spatial data?
- What are the relationships between location and certain outcomes (e.g., sales, health outcomes)?
- Can we visualize the data geographically to identify clusters or patterns?
- What is the effect of geographic factors (e.g., proximity to resources, location-specific policies) on the data?

6. Network/Graph Analysis
Network analysis focuses on the relationships and interactions between entities (nodes) connected by edges (links). It is often used to study social networks, communication networks, transportation systems, etc.

- What is the structure of the network (e.g., social network, communication network)?
- How do different nodes (individuals, entities) in the network interact with each other?
- Which nodes are most central or influential in the network?
- Are there any communities or clusters of nodes that are more densely connected?
- What is the shortest path or optimal route between two nodes in the network?
- How do changes in one part of the network affect other parts of the network?
- Are there any isolated nodes or disconnected subgraphs in the network?
- How resilient or robust is the network to node or edge failures?
- What is the flow of information or resources through the network?
"""

# Pass data to the template
# Usage: script_template.format(data)
# Usage: script_template.format(data=data)
script_template = """
Write a script which uses different analysis techniques as appropriate and saves files in the current folder. For analysis you can print descriptive logs. You can also generate PNG images to help in analysis.
Image and log file names should be descriptive, meaningful and should include the name of the technique used. Image should be stored with `.png` extension and log file with `.txt` extension. Logs printed should be descriptive and should clearly show how the analysis was performed.

You can use any system dependency but only use the following third party dependencies: pandas, numpy, matplotlib, seaborn, scikit-learn when writing the analyse script.

Choose from the following analysis techniques and write a script which would print logs and images which can help in answering questions. Example questions which can be answered by each of the techniques are listed below.:
1. Outlier and Anomaly Detection
Outlier and anomaly detection techniques help identify data points that deviate significantly from the rest of the data, which may indicate errors, fraud, or interesting patterns.

- What are the outliers or anomalies in the dataset?
- Which data points deviate from the general trend or expected behavior?
- Are there any unusual or extreme values in the dataset that could indicate errors or rare events?
- How can we identify potential fraud or mistakes in the dataset based on outliers?
- What methods can we use to remove or handle outliers without distorting the overall analysis?
- How does the presence of outliers affect the results of the analysis or model?

2. Correlation Analysis, Regression Analysis, and Feature Importance Analysis
These techniques analyze relationships between variables and help predict outcomes based on feature dependencies.

- What are the relationships between different variables in the dataset?
- Which variables are most strongly correlated with each other?
- How do independent variables influence a dependent variable in a regression model?
- Which features are the most important predictors of a target variable?
- Can we predict one variable based on others? If so, which variables provide the best predictive power?
- What are the coefficients of a regression model, and what do they tell us about the relationship between variables?
- How can we assess multicollinearity and its impact on the regression model?

3. Time Series Analysis
Time series analysis is used to analyze data points collected or recorded at specific time intervals, helping uncover trends, cycles, and seasonal patterns.

- What are the long-term trends in the data?
- Are there any seasonal patterns or periodic cycles in the data?
- Can we predict future values or trends based on historical data?
- How do we model time-dependent data and account for seasonality and trends?
- Are there any sudden shifts or anomalies in the time series data (e.g., structural breaks)?
- What is the forecast for future values in the time series?
- How do different time intervals (e.g., daily, monthly, yearly) affect the analysis?

4. Cluster Analysis
Cluster analysis groups similar data points together, helping identify natural groupings or patterns in the data, often used in market segmentation, customer analysis, or pattern recognition.

- How can we group the data into distinct clusters based on similar characteristics?
- What are the different segments or categories that naturally exist in the dataset?
- How can we identify homogeneous groups in the dataset that share common features?
- What characteristics define each of the identified clusters?
- How many clusters should we use, and how do we evaluate the quality of clustering?
- What is the distance or similarity between different clusters?
- What happens to the data when it is clustered using different methods (e.g., K-means, hierarchical)?

5. Geographic Analysis
Geographic analysis looks at spatial relationships between data points, helping to understand the geographic distribution and relationships between locations.

- What patterns exist in the data based on geographical location?
- Are there geographic areas where specific events or trends are more prominent?
- How are variables distributed across different geographic regions or areas?
- Can we identify areas of interest or concern based on spatial data?
- What are the relationships between location and certain outcomes (e.g., sales, health outcomes)?
- Can we visualize the data geographically to identify clusters or patterns?
- What is the effect of geographic factors (e.g., proximity to resources, location-specific policies) on the data?

6. Network/Graph Analysis
Network analysis focuses on the relationships and interactions between entities (nodes) connected by edges (links). It is often used to study social networks, communication networks, transportation systems, etc.

- What is the structure of the network (e.g., social network, communication network)?
- How do different nodes (individuals, entities) in the network interact with each other?
- Which nodes are most central or influential in the network?
- Are there any communities or clusters of nodes that are more densely connected?
- What is the shortest path or optimal route between two nodes in the network?
- How do changes in one part of the network affect other parts of the network?
- Are there any isolated nodes or disconnected subgraphs in the network?
- How resilient or robust is the network to node or edge failures?
- What is the flow of information or resources through the network?

The dataset would be passed to the function above as the only argument. The structure of the dataset is as below.
{data}
"""

improve_script_template = """
Below python script had an error:
```py
{script}
```
Error message:
{error}

Please fix the error in the script and output the complete script to be executed.
"""

summary_template = """
"Prepare a detailed report from all the image and log/text files passed which are stored in the current folder. The content should be presented as a narrative. The content returned should be in markdown format.
This content would be added in the README in the current folder and should reference the images stored in the current folder as appropriate.

The report should atleast include descriptive statistics, observations and conclusions among other things.
The summary statistics generated for this dataset is as follow:
{summary_stats}


Use the below image links when inserting images so it would load in markdown. Eg. ![](image_link):
{image_links}
"""


def parse_script(content):

    # Regex to extract code block between triple backticks
    code_block_pattern = r"```python\n(.*?)\n```"

    # Find all matches
    matches = re.findall(code_block_pattern, content, re.DOTALL)

    # If a match is found, extract the Python code
    if matches:
        python_code = matches[0]
        print("Extracted Python Code:")
        return python_code
    else:
        # Throw an exception
        raise ValueError("No Python code block found in the input.")


def get_script(data_description):
    response = requests.post(
        "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {proxy_token}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": script_template.format(data=data_description),
                },
            ],
        },
    )
    result = response.json()
    answer = result["choices"][0]["message"]["content"]

    script = parse_script(answer)
    print("Generated Script:")
    print(script)

    return script


def improve_script(script, error_msg):
    response = requests.post(
        "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {proxy_token}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": improve_script_template.format(
                        script=script, error=error_msg
                    ),
                },
            ],
        },
    )
    result = response.json()
    answer = result["choices"][0]["message"]["content"]

    script = parse_script(answer)
    print("Improved Script:")
    print(script)

    return script


# Retry script execution if failed by improving it
def retry_script_if_failed(script, retry_count=3):
    """Retry script execution if failed, up to a max retry count."""
    if retry_count <= 0:
        print("Max retries reached. Could not fix the script.")
        return

    try:
        # Create a dictionary for the global scope else exec would run in the current scope
        global_scope = globals().copy()
        exec(script, global_scope)  # Try to execute the script
    except Exception as e:
        # Capture the error message
        error_message = str(e)

        # Capture the full stack trace
        stack_trace = traceback.format_exc()

        # Print the error message and stack trace for debugging
        print(f"Error occurred: {error_message}")
        print(f"Stack trace:\n{stack_trace}")

        # Pass both the error message and the stack trace to improve_script
        improved_script = improve_script(script, error_message + "\n\n" + stack_trace)
        print("Retrying with the improved script...")
        # Retry the execution with the improved script
        retry_script_if_failed(improved_script, retry_count - 1)


def prepare_summary(summary_statistics):
    print("Generating summary")
    content = []
    image_links = []
    # Iterate over all the files in current folder
    # Get the current working directory
    current_directory = os.getcwd()
    for file_name in os.listdir(current_directory):
        # If file is an image
        if file_name.endswith(".png"):
            # Get base64 encoded image content
            image_path = os.path.join(current_directory, file_name)

            image_links.append(file_name)
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode()

            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "detail": "low",
                        # Instead of passing the image URL, we create a base64 encoded data URL
                        "url": f"data:image/png;base64,{image_base64}",
                    },
                }
            )
        # If file is a text file
        elif file_name.endswith(".txt"):
            with open(os.path.join(current_directory, file_name), "r") as file:
                text_content = file.read()
                content.append({"type": "text", "text": text_content})

    print("Image links are below:")
    print(image_links)

    response = requests.post(
        "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {proxy_token}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": summary_template.format(
                                image_links="\n".join(image_links),
                                summary_stats=summary_statistics,
                            ),
                        }
                    ],
                },
                {"role": "user", "content": content},
            ],
        },
    )
    result = response.json()
    try:
        answer = result["choices"][0]["message"]["content"]
    except KeyError as e:
        print(f"Error: Missing expected key in API response - {e}")
        print("Full API response:", result)
        return

    # Store the content returned in a README file. The file may not exist
    # Always override the file if it exists.
    # Create README.md file if it does not exist.
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        open(readme_path, "w").close()

    # Write the content returned by ChatGPT to a README.md file.
    with open(readme_path, "w") as f:
        f.write(answer)


def main():
    # Ensure the filename is provided as the first argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <dataset_filename>")
        sys.exit(1)

    # Load filename from the first argument
    filename = sys.argv[1]

    # Check if file exists
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' does not exist.")
        sys.exit(1)

    print(f"Loading dataset from: {filename}")

    # Step 0: Cleanup
    # Remove .png and .txt from current directory
    os.system("rm -f *.png *.txt README.md")

    # Step 1: Load dataset
    with open(filename, encoding="utf-8", errors="replace") as f:
        df = pd.read_csv(f)
    df.to_csv(filename, index=False, encoding="utf-8")

    # Step 2: Pass analysis results to the LLM and get the script
    llm_input = {
        "filename": filename,
        "columns": [{"name": col, "type": str(df[col].dtype)} for col in df.columns],
    }

    script = get_script(llm_input)

    # Execute the LLM script and retry if it fails
    retry_script_if_failed(script, retry_count=1)

    # Check if any png and txt file got created in current folder
    current_directory = os.getcwd()
    new_png_files = [f for f in os.listdir(current_directory) if f.endswith(".png")]
    new_text_files = [f for f in os.listdir(current_directory) if f.endswith(".txt")]
    if len(new_png_files) == 0 and len(new_text_files) == 0:
        print("Error! No new png or txt files created.")
        script = improve_script(
            script,
            "Please execute the script to generate the .png and .txt files. Maybe you forgot to call the function which generates those files. Or you are not generating the files in the current folder.",
        )
        retry_script_if_failed(script, retry_count=1)

    # Check the analysis in the analysis folder and prepare a summary
    prepare_summary(df.describe(include="all"))


if __name__ == "__main__":
    main()
