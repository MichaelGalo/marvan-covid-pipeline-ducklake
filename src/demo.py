import duckdb
import time


total_start_time = time.time()


duckdb.install_extension("ducklake")
duckdb.load_extension("ducklake")

setup_start_time = time.time()
con = duckdb.connect("my_ducklake.db")
con.execute("ATTACH 'ducklake:my_ducklake.db' AS my_lake")
con.execute("USE my_lake")

con.execute("CREATE SCHEMA IF NOT EXISTS bronze")
con.execute("CREATE SCHEMA IF NOT EXISTS silver")
con.execute("CREATE SCHEMA IF NOT EXISTS gold")
setup_end_time = time.time()
print(f"Database setup completed in {setup_end_time - setup_start_time:.2f} seconds")

bronze_start_time = time.time()


con.execute(
    "CREATE TABLE IF NOT EXISTS bronze.nppes AS SELECT * FROM read_csv('data/*.csv', all_varchar=True)"
)


bronze_count = con.execute("SELECT COUNT(*) FROM bronze.nppes").fetchone()[0]
bronze_end_time = time.time()
print(
    f"Data Ingested into Bronze Layer in {bronze_end_time - bronze_start_time:.2f} seconds ({bronze_count:,} total records)"
)

silver_start_time = time.time()
with open("sql/cleaning.sql", "r") as f:
    con.execute(f.read())


silver_count = con.execute("SELECT COUNT(*) FROM silver.nppes").fetchone()[0]
silver_end_time = time.time()
print(
    f"Data Cleaned and Stored in Silver Layer in {silver_end_time - silver_start_time:.2f} seconds ({silver_count:,} cleaned records)"
)

gold_start_time = time.time()
with open("sql/providers_by_state.sql", "r") as f:
    con.execute(f.read())
gold_count = con.execute("SELECT COUNT(*) FROM gold.providers_by_state").fetchone()[0]
gold_end_time = time.time()
print(
    f"Gold Layer Created with Providers by State Analysis in {gold_end_time - gold_start_time:.2f} seconds ({gold_count} states analyzed)"
)


query_start_time = time.time()
count = con.execute("SELECT COUNT(*) FROM gold.providers_by_state").fetchone()[0]
result = con.execute("SELECT * FROM gold.providers_by_state LIMIT 10").fetchall()
query_end_time = time.time()

print(f"\nRESULTS (Query executed in {query_end_time - query_start_time:.2f} seconds)")
print(f"Total states with providers: {count}")
print("\nSample data from gold.providers_by_state:")
for row in result:
    print(row)


summary_start_time = time.time()
print("\nSample data from gold.state_provider_summary:")
summary = con.execute("SELECT * FROM gold.state_provider_summary").fetchall()
for row in summary:
    print(row)
summary_end_time = time.time()
print(f"Summary query executed in {summary_end_time - summary_start_time:.2f} seconds")


con.close()


total_end_time = time.time()
total_execution_time = total_end_time - total_start_time
print(f"\nTOTAL PIPELINE EXECUTION TIME: {total_execution_time:.2f} seconds")


print("\nPERFORMANCE BREAKDOWN:")
print(
    f"  Database Setup:    {setup_end_time - setup_start_time:.2f}s ({((setup_end_time - setup_start_time) / total_execution_time * 100):.1f}%)"
)
print(
    f"  Bronze Layer:      {bronze_end_time - bronze_start_time:.2f}s ({((bronze_end_time - bronze_start_time) / total_execution_time * 100):.1f}%)"
)
print(
    f"  Silver Layer:      {silver_end_time - silver_start_time:.2f}s ({((silver_end_time - silver_start_time) / total_execution_time * 100):.1f}%)"
)
print(
    f"  Gold Layer:        {gold_end_time - gold_start_time:.2f}s ({((gold_end_time - gold_start_time) / total_execution_time * 100):.1f}%)"
)
print(
    f"  Verification:      {(query_end_time - query_start_time) + (summary_end_time - summary_start_time):.2f}s ({(((query_end_time - query_start_time) + (summary_end_time - summary_start_time)) / total_execution_time * 100):.1f}%)"
)
