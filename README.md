# SRAG Monitoring Dashboard

This project provides a **dashboard for monitoring Severe Acute Respiratory Syndrome (SRAG)** cases in Brazil. It leverages data from the Brazilian Ministry of Health's Open Data platform, processes it, and presents key metrics and visualizations to help analyze trends and changes over time.

---

## 🚀 Features

- **Data Ingestion**: Automatically fetches the latest SRAG data from an S3 bucket.
- **ETL Pipeline**: Processes and loads the data into a database.
- **Interactive Dashboard**: Built with Streamlit to display key metrics, charts, and insights.
- **AI-Powered Analysis**: Uses OpenAI's GPT-based models to generate summaries and insights.
- **Customizable**: Environment variables allow easy configuration for different setups.

---

## 📂 Project Structure

```
healthcare-report-agent/
├── app/
│   ├── agents/            # Agents for report generation and workflows
│   ├── config/            # Configuration settings
│   ├── data/              # Data ingestion and preprocessing
│   ├── databases/         # Database management
│   ├── nodes/             # Modular pipeline nodes
│   ├── prompts/           # Prompt templates for AI models
│   ├── services/          # Services for data visualization
│   ├── tools/             # Tools for metrics and plotting
├── streamlit_app.py       # Streamlit dashboard entry point
├── Makefile               # Makefile for common tasks
├── Dockerfile             # Dockerfile for containerizing the app
├── docker-compose.yml     # Docker Compose configuration
├── .env                   # Environment variables
├── .env.example           # Example environment variables
```

---

## 🛠️ Setup Instructions

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-repo/healthcare-report-agent.git
cd healthcare-report-agent
```

### 2. **Set Up Environment Variables**
- Copy the `.env.example` file to `.env`:
  ```bash
  cp .env.example .env
  ```
- Fill in the required values in the `.env` file:
  - `SRAG_SOURCE_URL`: URL of the SRAG dataset.
  - `DATABASE_URL`: Database connection string (e.g., SQLite or PostgreSQL).
  - `OPENAI_API_KEY`: Your OpenAI API key.
  - `SERP_API_KEY`: Your SERP API key.
  - `LANGFUSE_*`: Langfuse configuration keys.

### 3. **Install Dependencies**
- Using `pip`:
  ```bash
  pip install -r requirements.txt
  ```

### 4. **Run the Application**
- To run the Streamlit dashboard:
  ```bash
  make run-report
  ```

- To run the ETL pipeline:
  ```bash
  make feed-database
  ```

- To run both the ETL pipeline and report sequentially:
 ```bash
  make generate-report
  ```

- To generate test data and run tests:
  ```bash
  make create-data-run-tests
  ```

---

## 🐳 Docker Setup

### 1. **Build and Run with Docker Compose**
- Build the Docker image, start the services, and run the application:
  ```bash
  make build-up-run
  ```
  
- Access the dashboard at [http://localhost:8501](http://localhost:8501).

### 2. **Stop the Services**
- To stop the services, run:
  ```bash
  make down
  ```

---

## 📊 Dashboard Overview

The dashboard provides the following insights:

- **Key Metrics**:
  - Mortality rate changes
  - Case variation rate changes.
  - ICU admission changes.
  - Vaccination rate changes.

  Metrics are calculated in comparison to last month.

- **Charts**:
  - Daily cases (last 30 days).
  - Monthly cases (up to last 12 months).

- **AI-Generated Reports**:
  - Summarized insights based on the latest data.

---

## 📦 Deployment

In Progress.

---

## 🔑 Environment Variables

| Variable              | Description                                      |
|-----------------------|--------------------------------------------------|
| `SRAG_SOURCE_URL`     | URL of the SRAG dataset.                         |
| `DATABASE_URL`        | Database connection string (e.g., SQLite, Postgres). |
| `OPENAI_API_KEY`      | OpenAI API key for GPT-based models.             |
| `SERP_API_KEY`        | SERP API key for web search.                     |
| `TABLE_NAME`          | Name of the database table for SRAG data.        |
| `LANGFUSE_BASE_URL`   | Langfuse base URL for tracing.                   |
| `LANGFUSE_SECRET_KEY` | Langfuse secret key.                             |
| `LANGFUSE_PUBLIC_KEY` | Langfuse public key.                             |

---

## 📄 Makefile Commands

| Command                  | Description                                   |
|--------------------------|-----------------------------------------------|
| `make build`     | Build the Docker image. |
| `make up`     | Start the Docker container. |
| `make build-up`     | Build and start the Docker container. |
| `make down`     | Stop the Docker container. |
| `make logs`     | View logs from the app container. |
| `make run`     | Run app container. |
| `make run-report`        | Start the Streamlit dashboard.               |
| `make generate-report`   | Run the ETL pipeline and start the dashboard. |
| `make create-test-data`  | Generate test data.                          |
| `make run-tests`         | Run the test suite.                          |
| `make create-data-run-tests` | Generate test data and run tests.         |

---

## 👩‍💻 Contributors

- [Lucas de Almeida Sabino Carvalho](https://github.com/lcscarv)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

