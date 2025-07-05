# **AI Data Analyst Project Plan: From Setup to Deployment**

A 7-week modular plan to build and deploy an AI-powered data analyst for the CDC NHANES dataset.

### **Week 1: Module 0 \- Project Setup & Git Initialization 🛠️**

* **Goal:** Create a clean, authenticated, and version-controlled environment for the entire project.  
* **Tasks:**  
  1. **Create Google Cloud Project:** In the Google Cloud Console, create a new, dedicated project.  
  2. **Enable APIs:** Activate the **Vertex AI API** and the **BigQuery API**.  
  3. **Set Up Authentication:** Install the gcloud CLI and run gcloud auth application-default login.  
  4. **Initialize GitHub Repository:** Create a new repository on GitHub. Clone it to your local machine.  
  5. **Create Python Environment:** Set up a virtual environment (e.g., .venv).  
  6. **Install Base Packages:** Install google-cloud-aiplatform, google-cloud-bigquery, pandas, notebook, and langchain-google-vertexai.  
  7. **Create .gitignore:** Add your virtual environment folder (e.g., .venv/) to this file.  
  8. **First Commit:** Add the .gitignore file and an empty README.md to Git and push to GitHub.  
* **Outcome:** A fully configured local and cloud environment, ready for development and version-controlled with Git.  
* **Potential Article:** "Setting Up Your Environment for a Google Cloud AI Project."

### **Week 2: Module 1 \- Foundational Data Exploration 🗺️**

* **Goal:** Manually explore the NHANES dataset to find an interesting relationship to focus on.  
* **Outcome:** A short report or Jupyter notebook and a few visualizations.  
* **Potential Article:** "Uncovering Health Trends: A First Look at the CDC NHANES Dataset with AI."

### **Week 3: Module 2 \- The Text-to-SQL Agent 💬 → 쿼리**

* **Goal:** Build a simple agent that translates a natural language question into a BigQuery SQL query.  
* **Outcome:** A script that reliably converts a question into a SQL query string.  
* **Potential Article:** "How to Build a Natural Language to BigQuery SQL Translator."

### **Week 4: Module 3 \- The Query Execution System ⚙️**

* **Goal:** Give your agent the ability to execute the query and return data.  
* **Outcome:** A function that takes a question and returns a pandas DataFrame with the answer.  
* **Potential Article:** "From Question to Answer: Building an Agent That Queries BigQuery."

### **Week 5: Module 4 \- The Visualization Agent 📊**

* **Goal:** Teach your system to create its own visualizations.  
* **Outcome:** A system that can answer a question and generate a chart of the result.  
* **Potential Article:** "Let Your Agent Draw: Adding a Visualization Tool to a Data Agent."

### **Week 6: Module 5 \- The Analyst Agent 💡**

* **Goal:** Add a final layer of intelligence that interprets the results.  
* **Outcome:** A complete system that takes a question and returns an answer, a chart, and a written insight.  
* **Potential Article:** "From Data to Insight: Creating a Full-Stack AI Analyst."

### **Week 7: Module 6 \- Deployment 🚀**

* **Goal:** Deploy the full agentic system as a shareable web service.  
* **Outcome:** A public URL that can be used to interact with your AI data analyst.  
* **Potential Article:** "From Notebook to Web: Deploying an AI Data Analyst with Cloud Run."