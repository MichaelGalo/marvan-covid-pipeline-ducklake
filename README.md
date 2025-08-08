# Marvan COVID Pipeline - DuckLake Implementation

A modern data lake pipeline built with DuckDB's DuckLake extension, demonstrating a transition from traditional dbt/Snowflake architecture to a more flexible, cost-effective data lake approach.

## Project Overview

This project was created as a learning exercise to explore DuckLake as an alternative to traditional data warehousing solutions. The pipeline processes COVID-19 related datasets through a medallion architecture (Bronze → Silver → Gold) using DuckDB's DuckLake extension with MinIO for object storage.

### Why DuckLake?

After working with dbt/Snowflake, I wanted to explore:
- **Cost efficiency**: Eliminate compute charges for idle time
- **Local development**: Full pipeline testing without cloud dependencies  
- **Flexibility**: Schema evolution and data lake patterns
- **Performance**: DuckDB's analytics engine
- **Simplicity**: Reduced infrastructure complexity

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│   MinIO     │───▶│    Bronze    │───▶│   Silver    │───▶│    Gold     │
│ (Raw CSV)   │    │  (Raw Data)  │    │ (Cleaned)   │    │ (Analytics) │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
```

### Data Flow

1. **Source**: CSV files stored in MinIO S3-compatible storage
2. **Bronze Layer**: Raw data ingestion with metadata tracking
3. **Silver Layer**: Data cleaning and standardization
4. **Gold Layer**: Business-ready analytics tables

## Datasets

The pipeline processes COVID-19 related datasets including:
- **API Metadata**: Dataset information and sources
- **CA Antibody**: California antibody testing data
- **CA Rapid Test Demand**: California rapid test demand metrics
- **UK COVID Cases**: Daily COVID cases by location in the UK
- **US Death Counts**: COVID death statistics by demographics

## Technology Stack

- **DuckDB**: Analytics database engine
- **DuckLake**: Data lake extension for DuckDB
- **MinIO**: S3-compatible object storage
- **Python**: Pipeline orchestration and logging
- **DataGrip**: Database IDE for querying
- **FastAPI**: API for Data Delivery

## Getting Started

### Prerequisites

- Python 3.8+
- MinIO server running locally

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MichaelGalo/marvan-covid-pipeline-ducklake.git
   cd ducklake-marvan-pipeline
   ```

2. **Set up Python environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # .venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Configure environment**

5. **Run setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

### Running the Pipeline

```bash
python src/main.py
```

The pipeline will:
1. Connect to DuckLake 
2. Set up MinIO S3 connectivity
3. Create Bronze, Silver, and Gold schemas
4. Ingest raw CSV files from MinIO into Bronze tables
5. Process data through Silver and Gold layers

## Querying Data

### Using DataGrip

1. **Connect to the persistent database**
   - Database type: DuckDB
   - Database file: `/path/to/project/marvan_lake.db`

2. **Set up DuckLake in your query session**
   ```sql
   LOAD ducklake;
   
   -- Attach DuckLake
   ATTACH 'ducklake:catalog.ducklake' AS my_ducklake (DATA_PATH 'data_files');
   USE my_ducklake;
   ```

3. **Query your data**
   ```sql
   -- Sample Bronze data
   SELECT * FROM bronze.your_table_raw LIMIT 10;
   
   -- Sample Gold data
   SELECT * FROM gold.cleaned_table LIMIT 10;
   ```


## Learning Outcomes

### Key Differences from dbt/Snowflake

| Aspect | dbt/Snowflake | DuckLake |
|--------|---------------|----------|
| **Cost Model** | Pay for compute time | Local processing, storage costs only |
| **Development** | Cloud-dependent | Fully local development possible |
| **Schema Evolution** | Rigid, requires migrations | Flexible, automatic schema evolution |
| **Data Storage** | Proprietary format | Open formats (Parquet, etc.) |
| **Query Engine** | Snowflake SQL | DuckDB (PostgreSQL compatible) |
| **Deployment** | SaaS platform | Self-hosted or embedded |

### Advantages of DuckLake

- **Performance**: Columnar processing with vectorized execution
- **Cost**: No idle compute charges
- **Portability**: Standard file formats, can migrate easily
- **Development Speed**: Local testing without cloud resources
- **Schema Flexibility**: Automatic schema evolution

### Trade-offs

- **Scalability**: Limited to single-node processing (for now)
- **Ecosystem**: Smaller community compared to Snowflake
- **Enterprise Features**: Fewer built-in governance tools
- **Learning Curve**: New concepts around data lake patterns

## Logging

The pipeline uses structured JSON logging with:
- Timestamp
- Log level
- Message
- Source line number

Logs are written to both console and `logs/application.log`.

---

*This project represents a journey from traditional data warehousing to modern data lake architectures. It's designed for learning and experimentation rather than production use.*
