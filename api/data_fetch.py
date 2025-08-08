import duckdb
from src.logger import setup_logging

logger = setup_logging()

DATASET_CONFIG = {
    0: {
        "table_name": "gold.api_metadata"
    },
    1: {
        "table_name": "gold.ca_antibody"
    },
    2: {
        "table_name": "gold.ca_rapidtestdemand"
    },
    3: {
        "table_name": "gold.uk_covcasesbyday"
    },
    4: {
        "table_name": "gold.us_deathcounts"
    }
}

def fetch_single_dataset(dataset_id, offset, limit):
    logger.info(f"Fetching dataset {dataset_id} with offset={offset}, limit={limit}")
    
    dataset = DATASET_CONFIG[dataset_id]
    logger.info(f"Using dataset: {dataset['table_name']}")
    
    con = duckdb.connect("marvan_lake.db")
    con.execute("""
    ATTACH 'ducklake:/Users/michaelgalo/Workspace/data-engineering/projects/ducklake-marvan-pipeline/catalog.ducklake'
    AS my_ducklake (DATA_PATH '/Users/michaelgalo/Workspace/data-engineering/projects/ducklake-marvan-pipeline/data');

    USE my_ducklake;
    """)

    
    try:
        query = f"""
            SELECT * FROM {dataset['table_name']} 
            OFFSET {offset} 
            LIMIT {limit}
        """
        logger.info(f"Executing query: {query}")
        result = con.execute(query).fetchall()
        columns = [desc[0] for desc in con.description]
        
        # Normalize column names to lowercase for API 
        normalized_columns = [col.lower() for col in columns]
        data = [dict(zip(normalized_columns, row)) for row in result]

        logger.info(f"Retrieved {len(data)} records")
        return data
        
    except Exception as e:
        logger.error(f"Error fetching dataset {dataset_id}: {e}")
        raise
    finally:
        con.close()