import pandas as pd
import numpy as np
import os
import time
import dotenv
import ast
from sqlalchemy.sql import text
from datetime import datetime, timedelta
from typing import Dict, List, Union
from sqlalchemy import create_engine, Engine

# Create an SQLite database
db_engine = create_engine("sqlite:///munder_difflin.db")

# List containing the different kinds of papers 
paper_supplies = [
    # Paper Types (priced per sheet unless specified)
    {"item_name": "A4 paper",                         "category": "paper",        "unit_price": 0.05},
    {"item_name": "Letter-sized paper",              "category": "paper",        "unit_price": 0.06},
    {"item_name": "Cardstock",                        "category": "paper",        "unit_price": 0.15},
    {"item_name": "Colored paper",                    "category": "paper",        "unit_price": 0.10},
    {"item_name": "Glossy paper",                     "category": "paper",        "unit_price": 0.20},
    {"item_name": "Matte paper",                      "category": "paper",        "unit_price": 0.18},
    {"item_name": "Recycled paper",                   "category": "paper",        "unit_price": 0.08},
    {"item_name": "Eco-friendly paper",               "category": "paper",        "unit_price": 0.12},
    {"item_name": "Poster paper",                     "category": "paper",        "unit_price": 0.25},
    {"item_name": "Banner paper",                     "category": "paper",        "unit_price": 0.30},
    {"item_name": "Kraft paper",                      "category": "paper",        "unit_price": 0.10},
    {"item_name": "Construction paper",               "category": "paper",        "unit_price": 0.07},
    {"item_name": "Wrapping paper",                   "category": "paper",        "unit_price": 0.15},
    {"item_name": "Glitter paper",                    "category": "paper",        "unit_price": 0.22},
    {"item_name": "Decorative paper",                 "category": "paper",        "unit_price": 0.18},
    {"item_name": "Letterhead paper",                 "category": "paper",        "unit_price": 0.12},
    {"item_name": "Legal-size paper",                 "category": "paper",        "unit_price": 0.08},
    {"item_name": "Crepe paper",                      "category": "paper",        "unit_price": 0.05},
    {"item_name": "Photo paper",                      "category": "paper",        "unit_price": 0.25},
    {"item_name": "Uncoated paper",                   "category": "paper",        "unit_price": 0.06},
    {"item_name": "Butcher paper",                    "category": "paper",        "unit_price": 0.10},
    {"item_name": "Heavyweight paper",                "category": "paper",        "unit_price": 0.20},
    {"item_name": "Standard copy paper",              "category": "paper",        "unit_price": 0.04},
    {"item_name": "Bright-colored paper",             "category": "paper",        "unit_price": 0.12},
    {"item_name": "Patterned paper",                  "category": "paper",        "unit_price": 0.15},

    # Product Types (priced per unit)
    {"item_name": "Paper plates",                     "category": "product",      "unit_price": 0.10},  # per plate
    {"item_name": "Paper cups",                       "category": "product",      "unit_price": 0.08},  # per cup
    {"item_name": "Paper napkins",                    "category": "product",      "unit_price": 0.02},  # per napkin
    {"item_name": "Disposable cups",                  "category": "product",      "unit_price": 0.10},  # per cup
    {"item_name": "Table covers",                     "category": "product",      "unit_price": 1.50},  # per cover
    {"item_name": "Envelopes",                        "category": "product",      "unit_price": 0.05},  # per envelope
    {"item_name": "Sticky notes",                     "category": "product",      "unit_price": 0.03},  # per sheet
    {"item_name": "Notepads",                         "category": "product",      "unit_price": 2.00},  # per pad
    {"item_name": "Invitation cards",                 "category": "product",      "unit_price": 0.50},  # per card
    {"item_name": "Flyers",                           "category": "product",      "unit_price": 0.15},  # per flyer
    {"item_name": "Party streamers",                  "category": "product",      "unit_price": 0.05},  # per roll
    {"item_name": "Decorative adhesive tape (washi tape)", "category": "product", "unit_price": 0.20},  # per roll
    {"item_name": "Paper party bags",                 "category": "product",      "unit_price": 0.25},  # per bag
    {"item_name": "Name tags with lanyards",          "category": "product",      "unit_price": 0.75},  # per tag
    {"item_name": "Presentation folders",             "category": "product",      "unit_price": 0.50},  # per folder

    # Large-format items (priced per unit)
    {"item_name": "Large poster paper (24x36 inches)", "category": "large_format", "unit_price": 1.00},
    {"item_name": "Rolls of banner paper (36-inch width)", "category": "large_format", "unit_price": 2.50},

    # Specialty papers
    {"item_name": "100 lb cover stock",               "category": "specialty",    "unit_price": 0.50},
    {"item_name": "80 lb text paper",                 "category": "specialty",    "unit_price": 0.40},
    {"item_name": "250 gsm cardstock",                "category": "specialty",    "unit_price": 0.30},
    {"item_name": "220 gsm poster paper",             "category": "specialty",    "unit_price": 0.35},
]

# Given below are some utility functions you can use to implement your multi-agent system

def generate_sample_inventory(paper_supplies: list, coverage: float = 0.4, seed: int = 137) -> pd.DataFrame:
    """
    Generate inventory for exactly a specified percentage of items from the full paper supply list.

    This function randomly selects exactly `coverage` × N items from the `paper_supplies` list,
    and assigns each selected item:
    - a random stock quantity between 200 and 800,
    - a minimum stock level between 50 and 150.

    The random seed ensures reproducibility of selection and stock levels.

    Args:
        paper_supplies (list): A list of dictionaries, each representing a paper item with
                               keys 'item_name', 'category', and 'unit_price'.
        coverage (float, optional): Fraction of items to include in the inventory (default is 0.4, or 40%).
        seed (int, optional): Random seed for reproducibility (default is 137).

    Returns:
        pd.DataFrame: A DataFrame with the selected items and assigned inventory values, including:
                      - item_name
                      - category
                      - unit_price
                      - current_stock
                      - min_stock_level
    """
    # Ensure reproducible random output
    np.random.seed(seed)

    # Calculate number of items to include based on coverage
    num_items = int(len(paper_supplies) * coverage)

    # Randomly select item indices without replacement
    selected_indices = np.random.choice(
        range(len(paper_supplies)),
        size=num_items,
        replace=False
    )

    # Extract selected items from paper_supplies list
    selected_items = [paper_supplies[i] for i in selected_indices]

    # Construct inventory records
    inventory = []
    for item in selected_items:
        inventory.append({
            "item_name": item["item_name"],
            "category": item["category"],
            "unit_price": item["unit_price"],
            "current_stock": np.random.randint(200, 800),  # Realistic stock range
            "min_stock_level": np.random.randint(50, 150)  # Reasonable threshold for reordering
        })

    # Return inventory as a pandas DataFrame
    return pd.DataFrame(inventory)

def init_database(db_engine: Engine, seed: int = 137) -> Engine:    
    """
    Set up the Munder Difflin database with all required tables and initial records.

    This function performs the following tasks:
    - Creates the 'transactions' table for logging stock orders and sales
    - Loads customer inquiries from 'quote_requests.csv' into a 'quote_requests' table
    - Loads previous quotes from 'quotes.csv' into a 'quotes' table, extracting useful metadata
    - Generates a random subset of paper inventory using `generate_sample_inventory`
    - Inserts initial financial records including available cash and starting stock levels

    Args:
        db_engine (Engine): A SQLAlchemy engine connected to the SQLite database.
        seed (int, optional): A random seed used to control reproducibility of inventory stock levels.
                              Default is 137.

    Returns:
        Engine: The same SQLAlchemy engine, after initializing all necessary tables and records.

    Raises:
        Exception: If an error occurs during setup, the exception is printed and raised.
    """
    try:
        # ----------------------------
        # 1. Create an empty 'transactions' table schema
        # ----------------------------
        transactions_schema = pd.DataFrame({
            "id": [],
            "item_name": [],
            "transaction_type": [],  # 'stock_orders' or 'sales'
            "units": [],             # Quantity involved
            "price": [],             # Total price for the transaction
            "transaction_date": [],  # ISO-formatted date
        })
        transactions_schema.to_sql("transactions", db_engine, if_exists="replace", index=False)

        # Set a consistent starting date
        initial_date = datetime(2025, 1, 1).isoformat()

        # ----------------------------
        # 2. Load and initialize 'quote_requests' table
        # ----------------------------
        quote_requests_df = pd.read_csv("quote_requests.csv")
        quote_requests_df["id"] = range(1, len(quote_requests_df) + 1)
        quote_requests_df.to_sql("quote_requests", db_engine, if_exists="replace", index=False)

        # ----------------------------
        # 3. Load and transform 'quotes' table
        # ----------------------------
        quotes_df = pd.read_csv("quotes.csv")
        quotes_df["request_id"] = range(1, len(quotes_df) + 1)
        quotes_df["order_date"] = initial_date

        # Unpack metadata fields (job_type, order_size, event_type) if present
        if "request_metadata" in quotes_df.columns:
            quotes_df["request_metadata"] = quotes_df["request_metadata"].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else x
            )
            quotes_df["job_type"] = quotes_df["request_metadata"].apply(lambda x: x.get("job_type", ""))
            quotes_df["order_size"] = quotes_df["request_metadata"].apply(lambda x: x.get("order_size", ""))
            quotes_df["event_type"] = quotes_df["request_metadata"].apply(lambda x: x.get("event_type", ""))

        # Retain only relevant columns
        quotes_df = quotes_df[[
            "request_id",
            "total_amount",
            "quote_explanation",
            "order_date",
            "job_type",
            "order_size",
            "event_type"
        ]]
        quotes_df.to_sql("quotes", db_engine, if_exists="replace", index=False)

        # ----------------------------
        # 4. Generate inventory and seed stock
        # ----------------------------
        inventory_df = generate_sample_inventory(paper_supplies, seed=seed)

        # Seed initial transactions
        initial_transactions = []

        # Add a starting cash balance via a dummy sales transaction
        initial_transactions.append({
            "item_name": None,
            "transaction_type": "sales",
            "units": None,
            "price": 50000.0,
            "transaction_date": initial_date,
        })

        # Add one stock order transaction per inventory item
        for _, item in inventory_df.iterrows():
            initial_transactions.append({
                "item_name": item["item_name"],
                "transaction_type": "stock_orders",
                "units": item["current_stock"],
                "price": item["current_stock"] * item["unit_price"],
                "transaction_date": initial_date,
            })

        # Commit transactions to database
        pd.DataFrame(initial_transactions).to_sql("transactions", db_engine, if_exists="append", index=False)

        # Save the inventory reference table
        inventory_df.to_sql("inventory", db_engine, if_exists="replace", index=False)

        return db_engine

    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

def create_transaction(
    item_name: str,
    transaction_type: str,
    quantity: int,
    price: float,
    date: Union[str, datetime],
) -> int:
    """
    This function records a transaction of type 'stock_orders' or 'sales' with a specified
    item name, quantity, total price, and transaction date into the 'transactions' table of the database.

    Args:
        item_name (str): The name of the item involved in the transaction.
        transaction_type (str): Either 'stock_orders' or 'sales'.
        quantity (int): Number of units involved in the transaction.
        price (float): Total price of the transaction.
        date (str or datetime): Date of the transaction in ISO 8601 format.

    Returns:
        int: The ID of the newly inserted transaction.

    Raises:
        ValueError: If `transaction_type` is not 'stock_orders' or 'sales'.
        Exception: For other database or execution errors.
    """
    try:
        # Convert datetime to ISO string if necessary
        date_str = date.isoformat() if isinstance(date, datetime) else date

        # Validate transaction type
        if transaction_type not in {"stock_orders", "sales"}:
            raise ValueError("Transaction type must be 'stock_orders' or 'sales'")

        # Prepare transaction record as a single-row DataFrame
        transaction = pd.DataFrame([{
            "item_name": item_name,
            "transaction_type": transaction_type,
            "units": quantity,
            "price": price,
            "transaction_date": date_str,
        }])

        # Insert the record into the database
        transaction.to_sql("transactions", db_engine, if_exists="append", index=False)

        # Fetch and return the ID of the inserted row
        result = pd.read_sql("SELECT last_insert_rowid() as id", db_engine)
        return int(result.iloc[0]["id"])

    except Exception as e:
        print(f"Error creating transaction: {e}")
        raise

def get_all_inventory(as_of_date: str) -> Dict[str, int]:
    """
    Retrieve a snapshot of available inventory as of a specific date.

    This function calculates the net quantity of each item by summing 
    all stock orders and subtracting all sales up to and including the given date.

    Only items with positive stock are included in the result.

    Args:
        as_of_date (str): ISO-formatted date string (YYYY-MM-DD) representing the inventory cutoff.

    Returns:
        Dict[str, int]: A dictionary mapping item names to their current stock levels.
    """
    # SQL query to compute stock levels per item as of the given date
    query = """
        SELECT
            item_name,
            SUM(CASE
                WHEN transaction_type = 'stock_orders' THEN units
                WHEN transaction_type = 'sales' THEN -units
                ELSE 0
            END) as stock
        FROM transactions
        WHERE item_name IS NOT NULL
        AND transaction_date <= :as_of_date
        GROUP BY item_name
        HAVING stock > 0
    """

    # Execute the query with the date parameter
    result = pd.read_sql(query, db_engine, params={"as_of_date": as_of_date})

    # Convert the result into a dictionary {item_name: stock}
    return dict(zip(result["item_name"], result["stock"]))

def get_stock_level(item_name: str, as_of_date: Union[str, datetime]) -> pd.DataFrame:
    """
    Retrieve the stock level of a specific item as of a given date.

    This function calculates the net stock by summing all 'stock_orders' and 
    subtracting all 'sales' transactions for the specified item up to the given date.

    Args:
        item_name (str): The name of the item to look up.
        as_of_date (str or datetime): The cutoff date (inclusive) for calculating stock.

    Returns:
        pd.DataFrame: A single-row DataFrame with columns 'item_name' and 'current_stock'.
    """
    # Convert date to ISO string format if it's a datetime object
    if isinstance(as_of_date, datetime):
        as_of_date = as_of_date.isoformat()

    # SQL query to compute net stock level for the item
    stock_query = """
        SELECT
            item_name,
            COALESCE(SUM(CASE
                WHEN transaction_type = 'stock_orders' THEN units
                WHEN transaction_type = 'sales' THEN -units
                ELSE 0
            END), 0) AS current_stock
        FROM transactions
        WHERE item_name = :item_name
        AND transaction_date <= :as_of_date
    """

    # Execute query and return result as a DataFrame
    return pd.read_sql(
        stock_query,
        db_engine,
        params={"item_name": item_name, "as_of_date": as_of_date},
    )

def get_supplier_delivery_date(input_date_str: str, quantity: int) -> str:
    """
    Estimate the supplier delivery date based on the requested order quantity and a starting date.

    Delivery lead time increases with order size:
        - ≤10 units: same day
        - 11–100 units: 1 day
        - 101–1000 units: 4 days
        - >1000 units: 7 days

    Args:
        input_date_str (str): The starting date in ISO format (YYYY-MM-DD).
        quantity (int): The number of units in the order.

    Returns:
        str: Estimated delivery date in ISO format (YYYY-MM-DD).
    """
    # Debug log (comment out in production if needed)
    print(f"FUNC (get_supplier_delivery_date): Calculating for qty {quantity} from date string '{input_date_str}'")

    # Attempt to parse the input date
    try:
        input_date_dt = datetime.fromisoformat(input_date_str.split("T")[0])
    except (ValueError, TypeError):
        # Fallback to current date on format error
        print(f"WARN (get_supplier_delivery_date): Invalid date format '{input_date_str}', using today as base.")
        input_date_dt = datetime.now()

    # Determine delivery delay based on quantity
    if quantity <= 10:
        days = 0
    elif quantity <= 100:
        days = 1
    elif quantity <= 1000:
        days = 4
    else:
        days = 7

    # Add delivery days to the starting date
    delivery_date_dt = input_date_dt + timedelta(days=days)

    # Return formatted delivery date
    return delivery_date_dt.strftime("%Y-%m-%d")

def get_cash_balance(as_of_date: Union[str, datetime]) -> float:
    """
    Calculate the current cash balance as of a specified date.

    The balance is computed by subtracting total stock purchase costs ('stock_orders')
    from total revenue ('sales') recorded in the transactions table up to the given date.

    Args:
        as_of_date (str or datetime): The cutoff date (inclusive) in ISO format or as a datetime object.

    Returns:
        float: Net cash balance as of the given date. Returns 0.0 if no transactions exist or an error occurs.
    """
    try:
        # Convert date to ISO format if it's a datetime object
        if isinstance(as_of_date, datetime):
            as_of_date = as_of_date.isoformat()

        # Query all transactions on or before the specified date
        transactions = pd.read_sql(
            "SELECT * FROM transactions WHERE transaction_date <= :as_of_date",
            db_engine,
            params={"as_of_date": as_of_date},
        )

        # Compute the difference between sales and stock purchases
        if not transactions.empty:
            total_sales = transactions.loc[transactions["transaction_type"] == "sales", "price"].sum()
            total_purchases = transactions.loc[transactions["transaction_type"] == "stock_orders", "price"].sum()
            return float(total_sales - total_purchases)

        return 0.0

    except Exception as e:
        print(f"Error getting cash balance: {e}")
        return 0.0


def generate_financial_report(as_of_date: Union[str, datetime]) -> Dict:
    """
    Generate a complete financial report for the company as of a specific date.

    This includes:
    - Cash balance
    - Inventory valuation
    - Combined asset total
    - Itemized inventory breakdown
    - Top 5 best-selling products

    Args:
        as_of_date (str or datetime): The date (inclusive) for which to generate the report.

    Returns:
        Dict: A dictionary containing the financial report fields:
            - 'as_of_date': The date of the report
            - 'cash_balance': Total cash available
            - 'inventory_value': Total value of inventory
            - 'total_assets': Combined cash and inventory value
            - 'inventory_summary': List of items with stock and valuation details
            - 'top_selling_products': List of top 5 products by revenue
    """
    # Normalize date input
    if isinstance(as_of_date, datetime):
        as_of_date = as_of_date.isoformat()

    # Get current cash balance
    cash = get_cash_balance(as_of_date)

    # Get current inventory snapshot
    inventory_df = pd.read_sql("SELECT * FROM inventory", db_engine)
    inventory_value = 0.0
    inventory_summary = []

    # Compute total inventory value and summary by item
    for _, item in inventory_df.iterrows():
        stock_info = get_stock_level(item["item_name"], as_of_date)
        stock = stock_info["current_stock"].iloc[0]
        item_value = stock * item["unit_price"]
        inventory_value += item_value

        inventory_summary.append({
            "item_name": item["item_name"],
            "stock": stock,
            "unit_price": item["unit_price"],
            "value": item_value,
        })

    # Identify top-selling products by revenue
    top_sales_query = """
        SELECT item_name, SUM(units) as total_units, SUM(price) as total_revenue
        FROM transactions
        WHERE transaction_type = 'sales' AND transaction_date <= :date
        GROUP BY item_name
        ORDER BY total_revenue DESC
        LIMIT 5
    """
    top_sales = pd.read_sql(top_sales_query, db_engine, params={"date": as_of_date})
    top_selling_products = top_sales.to_dict(orient="records")

    return {
        "as_of_date": as_of_date,
        "cash_balance": cash,
        "inventory_value": inventory_value,
        "total_assets": cash + inventory_value,
        "inventory_summary": inventory_summary,
        "top_selling_products": top_selling_products,
    }


def search_quote_history(search_terms: List[str], limit: int = 5) -> List[Dict]:
    """
    Retrieve a list of historical quotes that match any of the provided search terms.

    The function searches both the original customer request (from `quote_requests`) and
    the explanation for the quote (from `quotes`) for each keyword. Results are sorted by
    most recent order date and limited by the `limit` parameter.

    Args:
        search_terms (List[str]): List of terms to match against customer requests and explanations.
        limit (int, optional): Maximum number of quote records to return. Default is 5.

    Returns:
        List[Dict]: A list of matching quotes, each represented as a dictionary with fields:
            - original_request
            - total_amount
            - quote_explanation
            - job_type
            - order_size
            - event_type
            - order_date
    """
    conditions = []
    params = {}

    # Build SQL WHERE clause using LIKE filters for each search term
    for i, term in enumerate(search_terms):
        param_name = f"term_{i}"
        conditions.append(
            f"(LOWER(qr.response) LIKE :{param_name} OR "
            f"LOWER(q.quote_explanation) LIKE :{param_name})"
        )
        params[param_name] = f"%{term.lower()}%"

    # Combine conditions; fallback to always-true if no terms provided
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Final SQL query to join quotes with quote_requests
    query = f"""
        SELECT
            qr.response AS original_request,
            q.total_amount,
            q.quote_explanation,
            q.job_type,
            q.order_size,
            q.event_type,
            q.order_date
        FROM quotes q
        JOIN quote_requests qr ON q.request_id = qr.id
        WHERE {where_clause}
        ORDER BY q.order_date DESC
        LIMIT {limit}
    """

    # Execute parameterized query
    with db_engine.connect() as conn:
        result = conn.execute(text(query), params)
        return [dict(row._mapping) for row in result]

########################
########################
########################
# YOUR MULTI AGENT STARTS HERE
########################
########################
########################


# Set up and load your env parameters and instantiate your model.
from dataclasses import asdict, dataclass
from pathlib import Path
import json
import re

from smolagents import OpenAIServerModel, ToolCallingAgent, tool
from smolagents.models import ChatMessage


@dataclass
class RequestedItem:
    original_name: str
    normalized_name: str
    quantity: int
    unit_label: str
    recognized: bool
    note: str = ""


@dataclass
class ParsedRequest:
    original_request: str
    request_date: str
    deadline_date: str
    request_kind: str
    items: List[RequestedItem]
    event_keyword: str = ""


@dataclass
class InventoryDecision:
    request_date: str
    deadline_date: str
    accepted_items: List[Dict]
    rejected_items: List[Dict]
    unknown_items: List[Dict]
    can_fulfill_any: bool
    delivery_date: str
    staged_delivery: bool
    cash_available: float


@dataclass
class QuoteDecision:
    subtotal: float
    discount_percent: float
    total_amount: int
    contextual_bonus: float
    history_hits: List[Dict]
    quoted_items: List[Dict]
    explanation: str


@dataclass
class FulfillmentDecision:
    status: str
    delivery_date: str
    staged_delivery: bool
    accepted_items: List[Dict]
    rejected_items: List[Dict]
    transactions: List[Dict]
    customer_response: str


class DeterministicModel:
    """Fallback callable used to satisfy smolagents initialization in local runs."""

    def __call__(self, messages: List[Dict[str, str]]) -> ChatMessage:
        return ChatMessage(
            role="assistant",
            content="Deterministic mode is active for this Beaver's Choice Paper Company project.",
        )


PROJECT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(__file__).resolve().parents[2]
db_engine = create_engine(f"sqlite:///{PROJECT_DIR / 'munder_difflin.db'}")
dotenv.load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
openai_api_key = os.getenv("UDACITY_OPENAI_API_KEY")

llm_model = (
    OpenAIServerModel(
        model_id="gpt-4o-mini",
        api_key=openai_api_key,
        api_base="https://openai.vocareum.com/v1",
    )
    if openai_api_key
    else DeterministicModel()
)

_starter_init_database = init_database


def init_database(db_engine_override: Engine = db_engine, seed: int = 137) -> Engine:
    original_cwd = Path.cwd()
    try:
        os.chdir(PROJECT_DIR)
        return _starter_init_database(db_engine_override, seed=seed)
    finally:
        os.chdir(original_cwd)

CATALOG_BY_NAME = {item["item_name"]: item for item in paper_supplies}
MONTH_NAME_DATE_PATTERN = re.compile(
    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}",
    re.IGNORECASE,
)
REQUEST_DATE_PATTERN = re.compile(r"Date of request:\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE)
ORDER_START_PATTERN = re.compile(r"\b\d[\d,]*\s+[A-Za-z]")

# Ordered from most-specific to most-general so that closest catalog matches win.
NORMALIZATION_RULES = [
    (
        re.compile(r"\bdecorative (?:adhesive )?tape\b|\bwashi tape\b", re.IGNORECASE),
        "Decorative adhesive tape (washi tape)",
        "Mapped the decorative tape request to the stocked washi tape item.",
    ),
    (re.compile(r"\btable covers?\b", re.IGNORECASE), "Table covers", ""),
    (re.compile(r"\bpresentation folders?\b", re.IGNORECASE), "Presentation folders", ""),
    (re.compile(r"\bname tags?\b", re.IGNORECASE), "Name tags with lanyards", ""),
    (re.compile(r"\bpaper party bags?\b", re.IGNORECASE), "Paper party bags", ""),
    (re.compile(r"\binvitation cards?\b", re.IGNORECASE), "Invitation cards", ""),
    (
        re.compile(r"\b(?:biodegradable\s+)?paper cups?\b|\bbiodegradable cups?\b", re.IGNORECASE),
        "Paper cups",
        "",
    ),
    (re.compile(r"\bdisposable cups?\b", re.IGNORECASE), "Disposable cups", ""),
    (
        re.compile(r"\b(?:compostable\s+)?paper plates?\b", re.IGNORECASE),
        "Paper plates",
        "",
    ),
    (
        re.compile(r"\bpaper napkins?\b|\btable napkins?\b|\bdinner napkins?\b", re.IGNORECASE),
        "Paper napkins",
        "",
    ),
    (re.compile(r"\bparty streamers?\b|\bstreamers?\b", re.IGNORECASE), "Party streamers", ""),
    (re.compile(r"\benvelopes?\b", re.IGNORECASE), "Envelopes", ""),
    (re.compile(r"\bflyers?\b", re.IGNORECASE), "Flyers", ""),
    (
        re.compile(r"\bposter boards?\b|\bposter board\b|\b24\"?\s*x\s*36\"?\b|\b24x36\b", re.IGNORECASE),
        "Large poster paper (24x36 inches)",
        "Mapped the poster board request to the stocked 24x36 poster stock.",
    ),
    (re.compile(r"\bposters?\b", re.IGNORECASE), "Poster paper", "Mapped the poster request to poster paper stock."),
    (re.compile(r"\bposter paper\b", re.IGNORECASE), "Poster paper", ""),
    (re.compile(r"\bbanner paper\b", re.IGNORECASE), "Banner paper", ""),
    (re.compile(r"\bglossy photo paper\b|\bphoto paper\b", re.IGNORECASE), "Photo paper", ""),
    (re.compile(r"\bglossy\b", re.IGNORECASE), "Glossy paper", ""),
    (re.compile(r"\bmatte\b", re.IGNORECASE), "Matte paper", ""),
    (re.compile(r"\brecycled paper\b", re.IGNORECASE), "Recycled paper", ""),
    (
        re.compile(r"\beco[- ]friendly paper\b|\benvironmentally friendly paper\b", re.IGNORECASE),
        "Eco-friendly paper",
        "",
    ),
    (re.compile(r"\bkraft paper\b", re.IGNORECASE), "Kraft paper", ""),
    (re.compile(r"\bconstruction paper\b", re.IGNORECASE), "Construction paper", ""),
    (re.compile(r"\bwrapping paper\b", re.IGNORECASE), "Wrapping paper", ""),
    (re.compile(r"\bglitter paper\b", re.IGNORECASE), "Glitter paper", ""),
    (re.compile(r"\bdecorative paper\b", re.IGNORECASE), "Decorative paper", ""),
    (re.compile(r"\bletterhead paper\b", re.IGNORECASE), "Letterhead paper", ""),
    (re.compile(r"\blegal[- ]size paper\b", re.IGNORECASE), "Legal-size paper", ""),
    (re.compile(r"\bcrepe paper\b", re.IGNORECASE), "Crepe paper", ""),
    (re.compile(r"\buncoated paper\b", re.IGNORECASE), "Uncoated paper", ""),
    (re.compile(r"\bheavyweight paper\b", re.IGNORECASE), "Heavyweight paper", ""),
    (re.compile(r"\b100 lb cover stock\b|\bcover stock\b", re.IGNORECASE), "100 lb cover stock", ""),
    (re.compile(r"\b80 lb text paper\b", re.IGNORECASE), "80 lb text paper", ""),
    (re.compile(r"\b250 gsm cardstock\b", re.IGNORECASE), "250 gsm cardstock", ""),
    (re.compile(r"\b220 gsm poster paper\b", re.IGNORECASE), "220 gsm poster paper", ""),
    (
        re.compile(
            r"\bheavy(?:weight)? cardstock\b|\bsturdy cardstock\b|\bwhite cardstock\b|\bcolored cardstock\b|\bcardstock\b",
            re.IGNORECASE,
        ),
        "Cardstock",
        "",
    ),
    (re.compile(r"\bbright[- ]colored paper\b", re.IGNORECASE), "Bright-colored paper", ""),
    (re.compile(r"\bpatterned paper\b", re.IGNORECASE), "Patterned paper", ""),
    (
        re.compile(r"\b8\.5\"?x11\"?\s+colored paper\b|\bcolored printer paper\b|\bcolored paper\b|\bcolorful paper\b", re.IGNORECASE),
        "Colored paper",
        "",
    ),
    (re.compile(r"\bletter-sized paper\b", re.IGNORECASE), "Letter-sized paper", ""),
    (
        re.compile(r"\ba4 (?:white )?(?:printer |printing )?paper\b|\ba4 paper\b", re.IGNORECASE),
        "A4 paper",
        "",
    ),
    (
        re.compile(r"\bstandard (?:copy|printer|printing) paper\b|\bprinter paper\b|\bprinting paper\b|\bwhite printer paper\b", re.IGNORECASE),
        "Standard copy paper",
        "Mapped the printer paper request to standard copy paper.",
    ),
]

GENERIC_KEYWORDS = {
    "paper",
    "papers",
    "sheets",
    "sheet",
    "stock",
    "size",
    "white",
    "assorted",
    "colors",
    "color",
}


def safe_json_loads(payload: str) -> Dict:
    return json.loads(payload) if payload else {}


def as_json(data: Union[Dict, List, str]) -> str:
    if isinstance(data, str):
        return data
    return json.dumps(data, indent=2)


def get_catalog_price(item_name: str) -> float:
    return float(CATALOG_BY_NAME[item_name]["unit_price"])


def get_inventory_reference(item_name: str) -> Dict[str, Union[str, float, int]]:
    inventory_reference = pd.read_sql(
        "SELECT * FROM inventory WHERE item_name = :item_name",
        db_engine,
        params={"item_name": item_name},
    )
    if not inventory_reference.empty:
        row = inventory_reference.iloc[0]
        return {
            "item_name": row["item_name"],
            "unit_price": float(row["unit_price"]),
            "min_stock_level": int(row["min_stock_level"]),
        }

    return {
        "item_name": item_name,
        "unit_price": get_catalog_price(item_name),
        "min_stock_level": 100,
    }


def extract_request_date(request_text: str) -> str:
    request_date_match = REQUEST_DATE_PATTERN.search(request_text)
    if request_date_match:
        return request_date_match.group(1)
    return datetime.now().strftime("%Y-%m-%d")


def extract_deadline_date(request_text: str, request_date: str) -> str:
    deadline_match = MONTH_NAME_DATE_PATTERN.search(request_text)
    if deadline_match:
        deadline = datetime.strptime(deadline_match.group(0), "%B %d, %Y")
        return deadline.strftime("%Y-%m-%d")
    return request_date


def isolate_order_body(request_text: str) -> str:
    no_request_metadata = REQUEST_DATE_PATTERN.sub("", request_text)
    deadline_match = MONTH_NAME_DATE_PATTERN.search(no_request_metadata)
    body = no_request_metadata[: deadline_match.start()] if deadline_match else no_request_metadata
    body = body.replace("\n- ", " ").replace("\n", " ")
    body = re.sub(r"\s+", " ", body)
    return body.strip()


def detect_request_kind(request_text: str) -> str:
    lowered = request_text.lower()
    if any(keyword in lowered for keyword in ["inventory", "in stock", "available", "stock level", "how many do you have"]):
        return "inventory_query"
    return "order_request"


def detect_event_keyword(request_text: str) -> str:
    event_patterns = [
        r"\bfor (?:our|the) upcoming ([a-z ]+?)(?:\.|,|$)",
        r"\bfor the ([a-z ]+?)(?:\.|,|$)",
        r"\bfor our ([a-z ]+?)(?:\.|,|$)",
    ]
    for pattern in event_patterns:
        event_match = re.search(pattern, request_text.lower())
        if event_match:
            return event_match.group(1).strip()
    return ""


def convert_requested_quantity(quantity: int, segment_text: str) -> int:
    if re.search(r"\breams?\b", segment_text, re.IGNORECASE):
        return quantity * 500
    return quantity


def detect_unit_label(segment_text: str) -> str:
    unit_match = re.search(
        r"\b(sheets?|reams?|rolls?|roll|packets?|packs?|boxes?|cups?|plates?|napkins?|covers?|folders?|posters?|flyers?|tickets?|balloons?)\b",
        segment_text,
        re.IGNORECASE,
    )
    return unit_match.group(1).lower() if unit_match else "units"


def extract_display_name(rest: str) -> str:
    fallback = rest.strip(" ,;:-.")
    cleaned = re.sub(
        r"^(sheets?|reams?|rolls?|roll|packets?|packs?|boxes?)\s+(?:of\s+)?",
        "",
        rest,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\bfor (?:the|our)\b.*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bplease\b.*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bwe need\b.*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bi need\b.*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\band$", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip(" ,;:-.")
    return cleaned if cleaned else fallback


def normalize_item_name(segment_text: str) -> tuple[str, str]:
    for pattern, normalized_name, base_note in NORMALIZATION_RULES:
        if pattern.search(segment_text):
            note = base_note
            lowered = segment_text.lower()
            if any(size_hint in lowered for size_hint in ["a3", "a5"]) and normalized_name not in lowered:
                size_note = f"Used the closest stocked {normalized_name.lower()} option because the exact size variant is not in the catalog."
                note = f"{base_note} {size_note}".strip()
            return normalized_name, note.strip()
    return "unknown", "No reliable catalog match was found for this requested item."


def parse_requested_items(request_text: str) -> List[RequestedItem]:
    request_body = isolate_order_body(request_text)
    start_positions = [match.start() for match in ORDER_START_PATTERN.finditer(request_body)]
    requested_items: List[RequestedItem] = []

    for index, start_position in enumerate(start_positions):
        end_position = start_positions[index + 1] if index + 1 < len(start_positions) else len(request_body)
        segment = request_body[start_position:end_position].strip(" ,;:-")
        quantity_match = re.match(r"(?P<quantity>\d[\d,]*)\s+(?P<rest>.+)", segment)
        if not quantity_match:
            continue

        raw_quantity = int(quantity_match.group("quantity").replace(",", ""))
        rest = quantity_match.group("rest").strip(" ,;:-")
        quantity = convert_requested_quantity(raw_quantity, segment)
        normalized_name, note = normalize_item_name(segment)
        requested_items.append(
            RequestedItem(
                original_name=extract_display_name(rest),
                normalized_name=normalized_name,
                quantity=quantity,
                unit_label=detect_unit_label(segment),
                recognized=normalized_name != "unknown",
                note=note,
            )
        )

    return requested_items


def parse_request(request_text: str) -> ParsedRequest:
    request_date = extract_request_date(request_text)
    return ParsedRequest(
        original_request=request_text,
        request_date=request_date,
        deadline_date=extract_deadline_date(request_text, request_date),
        request_kind=detect_request_kind(request_text),
        items=parse_requested_items(request_text),
        event_keyword=detect_event_keyword(request_text),
    )


def lookup_stock_level(item_name: str, as_of_date: str) -> int:
    stock_df = get_stock_level(item_name, as_of_date)
    if stock_df.empty:
        return 0
    return int(stock_df["current_stock"].iloc[0])


def lookup_quote_history_terms(parsed_request: ParsedRequest, accepted_items: List[Dict]) -> List[str]:
    candidate_terms = []
    if parsed_request.event_keyword:
        candidate_terms.extend(re.findall(r"[a-z]{4,}", parsed_request.event_keyword.lower()))
    for item in accepted_items:
        item_terms = [
            token
            for token in re.findall(r"[a-z]{4,}", item["item_name"].lower())
            if token not in GENERIC_KEYWORDS
        ]
        candidate_terms.extend(item_terms)

    deduped_terms = []
    for term in candidate_terms:
        if term not in deduped_terms:
            deduped_terms.append(term)
    return deduped_terms[:2]


def allocate_discounted_item_totals(accepted_items: List[Dict], total_amount: int, discount_multiplier: float) -> List[Dict]:
    if not accepted_items:
        return []

    priced_items = []
    for item in accepted_items:
        line_subtotal = round(item["quantity"] * get_catalog_price(item["item_name"]), 2)
        priced_items.append({**item, "line_subtotal": line_subtotal})

    running_total = 0.0
    for item in priced_items[:-1]:
        line_total = round(item["line_subtotal"] * discount_multiplier, 2)
        item["discounted_line_total"] = line_total
        running_total += line_total

    priced_items[-1]["discounted_line_total"] = round(total_amount - running_total, 2)
    return priced_items


def build_inventory_summary(accepted_items: List[Dict], rejected_items: List[Dict], unknown_items: List[Dict]) -> str:
    accepted_summary = ", ".join(
        [
            f"{item['quantity']} {item['item_name']} (available {item['available_on']})"
            for item in accepted_items
        ]
    )
    rejected_summary = ", ".join([item["original_name"] for item in rejected_items + unknown_items])
    if accepted_summary and rejected_summary:
        return f"Accepted: {accepted_summary}. Rejected: {rejected_summary}."
    if accepted_summary:
        return f"Accepted: {accepted_summary}."
    if rejected_summary:
        return f"Rejected: {rejected_summary}."
    return "No actionable items were found."


"""Set up tools for your agents to use, these should be methods that combine the database functions above
 and apply criteria to them to ensure that the flow of the system is correct."""


# Tools for inventory agent
@tool
def inventory_snapshot_tool(as_of_date: str) -> str:
    """
    Retrieve a full inventory snapshot for a given date.

    Args:
        as_of_date: ISO date used to evaluate inventory levels.

    Returns:
        JSON string with all stocked catalog items and quantities.
    """
    return as_json(get_all_inventory(as_of_date))


@tool
def stock_level_tool(item_name: str, as_of_date: str) -> str:
    """
    Retrieve the stock level for one catalog item on a given date.

    Args:
        item_name: Exact catalog item name.
        as_of_date: ISO date used to evaluate the stock level.

    Returns:
        JSON string with the requested stock level row.
    """
    return get_stock_level(item_name, as_of_date).to_json(orient="records")


@tool
def supplier_delivery_tool(start_date: str, quantity: int) -> str:
    """
    Estimate the supplier delivery date for a replenishment order.

    Args:
        start_date: ISO date when the replenishment is requested.
        quantity: Number of units to replenish.

    Returns:
        ISO date string with the estimated supplier delivery date.
    """
    return get_supplier_delivery_date(start_date, quantity)


@tool
def financial_report_tool(as_of_date: str) -> str:
    """
    Generate a financial snapshot for the company.

    Args:
        as_of_date: ISO date used to compute the report.

    Returns:
        JSON string with cash balance, inventory value, and top products.
    """
    return as_json(generate_financial_report(as_of_date))


# Tools for quoting agent
@tool
def quote_history_tool(search_terms_csv: str, limit: int = 5) -> str:
    """
    Search historical quotes using a compact CSV list of search terms.

    Args:
        search_terms_csv: Comma-separated search terms.
        limit: Maximum number of quote rows to return.

    Returns:
        JSON string with matching quote history rows.
    """
    search_terms = [term.strip() for term in search_terms_csv.split(",") if term.strip()]
    return as_json(search_quote_history(search_terms, limit=limit))


# Tools for ordering agent
@tool
def cash_balance_tool(as_of_date: str) -> str:
    """
    Retrieve the current cash balance for a given date.

    Args:
        as_of_date: ISO date used to compute cash balance.

    Returns:
        Cash balance as a stringified float.
    """
    return str(get_cash_balance(as_of_date))


@tool
def record_stock_order_tool(item_name: str, quantity: int, price: float, transaction_date: str) -> str:
    """
    Record a supplier stock order transaction.

    Args:
        item_name: Exact catalog item name.
        quantity: Number of units in the replenishment.
        price: Total replenishment cost.
        transaction_date: ISO date of the replenishment transaction.

    Returns:
        Stringified transaction ID.
    """
    return str(create_transaction(item_name, "stock_orders", quantity, price, transaction_date))


@tool
def record_sale_tool(item_name: str, quantity: int, price: float, transaction_date: str) -> str:
    """
    Record a customer sale transaction.

    Args:
        item_name: Exact catalog item name.
        quantity: Number of units sold.
        price: Total sales price.
        transaction_date: ISO date of the sale transaction.

    Returns:
        Stringified transaction ID.
    """
    return str(create_transaction(item_name, "sales", quantity, price, transaction_date))


# Set up your agents and create an orchestration agent that will manage them.
class BeaverChoiceAgent(ToolCallingAgent):
    """Small deterministic agent shell that keeps the module 4 smolagents shape."""

    def __init__(self, tools: List, model_to_use, name: str, description: str) -> None:
        super().__init__(
            tools=tools,
            model=model_to_use,
            name=name,
            description=description,
        )


class InventoryAgent(BeaverChoiceAgent):
    """Agent specialized in stock assessment and replenishment feasibility."""

    def __init__(self, model_to_use) -> None:
        super().__init__(
            tools=[
                inventory_snapshot_tool,
                stock_level_tool,
                supplier_delivery_tool,
                cash_balance_tool,
                financial_report_tool,
            ],
            model_to_use=model_to_use,
            name="inventory_agent",
            description="Checks current stock, evaluates replenishment feasibility, and explains delivery timing.",
        )

    def run(self, task: str, stream: bool = False, reset: bool = True, images=None, additional_args=None, max_steps: int | None = None):
        payload = safe_json_loads(task)
        parsed_request = ParsedRequest(
            original_request=payload["original_request"],
            request_date=payload["request_date"],
            deadline_date=payload["deadline_date"],
            request_kind=payload["request_kind"],
            items=[RequestedItem(**item) for item in payload["items"]],
            event_keyword=payload.get("event_keyword", ""),
        )

        accepted_items = []
        rejected_items = []
        unknown_items = []
        cash_available = float(self.tools["cash_balance_tool"](parsed_request.request_date))
        reserved_cash = 0.0
        delivery_dates = []

        for item in parsed_request.items:
            if not item.recognized:
                unknown_items.append(
                    {
                        "original_name": item.original_name,
                        "reason": "No reliable catalog match was found for this request.",
                    }
                )
                continue

            current_stock = lookup_stock_level(item.normalized_name, parsed_request.request_date)
            shortfall = max(0, item.quantity - current_stock)
            available_on = parsed_request.request_date
            reorder_cost = 0.0
            replenishment_needed = shortfall > 0

            if replenishment_needed:
                available_on = supplier_delivery_tool(parsed_request.request_date, shortfall)
                reorder_cost = round(shortfall * get_catalog_price(item.normalized_name), 2)

            if available_on > parsed_request.deadline_date:
                rejected_items.append(
                    {
                        "item_name": item.normalized_name,
                        "original_name": item.original_name,
                        "quantity": item.quantity,
                        "reason": f"Supplier timing reaches {available_on}, after the requested deadline of {parsed_request.deadline_date}.",
                    }
                )
                continue

            if reserved_cash + reorder_cost > cash_available:
                rejected_items.append(
                    {
                        "item_name": item.normalized_name,
                        "original_name": item.original_name,
                        "quantity": item.quantity,
                        "reason": "Cash on hand is not sufficient to replenish this item in time.",
                    }
                )
                continue

            reserved_cash += reorder_cost
            delivery_dates.append(available_on)
            accepted_items.append(
                {
                    "item_name": item.normalized_name,
                    "original_name": item.original_name,
                    "quantity": item.quantity,
                    "unit_label": item.unit_label,
                    "note": item.note,
                    "current_stock": current_stock,
                    "shortfall": shortfall,
                    "replenishment_needed": replenishment_needed,
                    "reorder_cost": reorder_cost,
                    "available_on": available_on,
                    "min_stock_level": int(get_inventory_reference(item.normalized_name)["min_stock_level"]),
                }
            )

        delivery_date = max(delivery_dates) if delivery_dates else parsed_request.request_date
        staged_delivery = len(set(delivery_dates)) > 1
        inventory_decision = InventoryDecision(
            request_date=parsed_request.request_date,
            deadline_date=parsed_request.deadline_date,
            accepted_items=accepted_items,
            rejected_items=rejected_items,
            unknown_items=unknown_items,
            can_fulfill_any=bool(accepted_items),
            delivery_date=delivery_date,
            staged_delivery=staged_delivery,
            cash_available=cash_available,
        )
        return as_json(asdict(inventory_decision))


class QuoteAgent(BeaverChoiceAgent):
    """Agent specialized in pricing, discounts, and historical quote context."""

    def __init__(self, model_to_use) -> None:
        super().__init__(
            tools=[quote_history_tool],
            model_to_use=model_to_use,
            name="quote_agent",
            description="Builds customer-friendly quotes using catalog prices, bulk discounts, and quote history.",
        )

    def run(self, task: str, stream: bool = False, reset: bool = True, images=None, additional_args=None, max_steps: int | None = None):
        payload = safe_json_loads(task)
        parsed_request = ParsedRequest(**payload["parsed_request"])
        inventory_decision = InventoryDecision(**payload["inventory_decision"])

        if not inventory_decision.accepted_items:
            empty_quote = QuoteDecision(
                subtotal=0.0,
                discount_percent=0.0,
                total_amount=0,
                contextual_bonus=0.0,
                history_hits=[],
                quoted_items=[],
                explanation="No valid items were available to quote.",
            )
            return as_json(asdict(empty_quote))

        subtotal = round(
            sum(item["quantity"] * get_catalog_price(item["item_name"]) for item in inventory_decision.accepted_items),
            2,
        )
        total_units = sum(item["quantity"] for item in inventory_decision.accepted_items)

        if total_units >= 5000 or subtotal >= 1500:
            base_discount = 12.0
        elif total_units >= 1500 or subtotal >= 400:
            base_discount = 8.0
        else:
            base_discount = 5.0

        search_terms = lookup_quote_history_terms(parsed_request, inventory_decision.accepted_items)
        history_hits = []
        for search_term in search_terms:
            raw_hits = safe_json_loads(quote_history_tool(search_term, limit=3))
            for hit in raw_hits:
                try:
                    total_amount = float(hit["total_amount"])
                except (TypeError, ValueError):
                    total_amount = -1
                if total_amount > 0:
                    history_hits.append(hit)
            if history_hits:
                break

        contextual_bonus = 2.0 if len(history_hits) >= 3 else 1.0 if history_hits else 0.0
        discount_percent = min(15.0, base_discount + contextual_bonus)
        discount_multiplier = 1 - (discount_percent / 100)
        total_amount = int(round(subtotal * discount_multiplier))
        quoted_items = allocate_discounted_item_totals(
            inventory_decision.accepted_items,
            total_amount,
            discount_multiplier,
        )
        explanation = (
            f"We built the quote from the live catalog subtotal of ${subtotal:.2f}. "
            f"A {base_discount:.0f}% bulk discount was applied for the requested volume, "
            f"and a {contextual_bonus:.0f}% contextual adjustment was added from similar quote history."
            if contextual_bonus
            else f"We built the quote from the live catalog subtotal of ${subtotal:.2f} and applied a {base_discount:.0f}% bulk discount for the requested volume."
        )
        quote_decision = QuoteDecision(
            subtotal=subtotal,
            discount_percent=discount_percent,
            total_amount=total_amount,
            contextual_bonus=contextual_bonus,
            history_hits=history_hits[:3],
            quoted_items=quoted_items,
            explanation=explanation,
        )
        return as_json(asdict(quote_decision))


class FulfillmentAgent(BeaverChoiceAgent):
    """Agent specialized in persisting transactions and generating final customer responses."""

    def __init__(self, model_to_use) -> None:
        super().__init__(
            tools=[cash_balance_tool, record_stock_order_tool, record_sale_tool, financial_report_tool],
            model_to_use=model_to_use,
            name="fulfillment_agent",
            description="Finalizes viable orders, records transactions, and returns customer-facing confirmations.",
        )

    def run(self, task: str, stream: bool = False, reset: bool = True, images=None, additional_args=None, max_steps: int | None = None):
        payload = safe_json_loads(task)
        parsed_request = ParsedRequest(**payload["parsed_request"])
        inventory_decision = InventoryDecision(**payload["inventory_decision"])
        quote_decision = QuoteDecision(**payload["quote_decision"])

        if not inventory_decision.accepted_items:
            rejected_reasons = [item["reason"] for item in inventory_decision.rejected_items + inventory_decision.unknown_items]
            customer_response = (
                "Beaver's Choice Paper Company could not confirm this order. "
                f"Reason: {' '.join(rejected_reasons) if rejected_reasons else 'No valid catalog items were identified.'}"
            )
            fulfillment_decision = FulfillmentDecision(
                status="rejected",
                delivery_date=parsed_request.request_date,
                staged_delivery=False,
                accepted_items=[],
                rejected_items=inventory_decision.rejected_items + inventory_decision.unknown_items,
                transactions=[],
                customer_response=customer_response,
            )
            return as_json(asdict(fulfillment_decision))

        transactions = []
        accepted_item_summaries = []
        for item in quote_decision.quoted_items:
            if item["shortfall"] > 0:
                stock_order_id = record_stock_order_tool(
                    item["item_name"],
                    item["shortfall"],
                    item["reorder_cost"],
                    parsed_request.request_date,
                )
                transactions.append(
                    {
                        "transaction_type": "stock_orders",
                        "transaction_id": stock_order_id,
                        "item_name": item["item_name"],
                        "quantity": item["shortfall"],
                        "price": item["reorder_cost"],
                        "transaction_date": parsed_request.request_date,
                    }
                )

            sale_transaction_id = record_sale_tool(
                item["item_name"],
                item["quantity"],
                item["discounted_line_total"],
                parsed_request.request_date,
            )
            transactions.append(
                {
                    "transaction_type": "sales",
                    "transaction_id": sale_transaction_id,
                    "item_name": item["item_name"],
                    "quantity": item["quantity"],
                    "price": item["discounted_line_total"],
                    "transaction_date": parsed_request.request_date,
                }
            )

            accepted_item_summaries.append(
                {
                    "item_name": item["item_name"],
                    "quantity": item["quantity"],
                    "available_on": item["available_on"],
                    "note": item["note"],
                }
            )

        accepted_summary = "; ".join(
            [
                f"{item['quantity']} units of {item['item_name']} available on {item['available_on']}"
                for item in accepted_item_summaries
            ]
        )
        rejected_bits = inventory_decision.rejected_items + inventory_decision.unknown_items
        rejected_summary = " ".join(
            [
                f"We could not include {item.get('original_name', item.get('item_name', 'that item'))} because {item['reason']}"
                for item in rejected_bits
            ]
        )
        note_summary = " ".join([item["note"] for item in accepted_item_summaries if item["note"]])

        response_parts = [
            "Beaver's Choice Paper Company confirmed your request.",
            f"Quoted total: ${quote_decision.total_amount}.",
            quote_decision.explanation,
            f"Confirmed items: {accepted_summary}.",
            f"The latest committed delivery date is {inventory_decision.delivery_date}, which stays within your requested deadline of {parsed_request.deadline_date}.",
        ]
        if inventory_decision.staged_delivery:
            response_parts.append("This order may arrive in staged deliveries because some items require supplier replenishment.")
        if note_summary:
            response_parts.append(note_summary)
        if rejected_summary:
            response_parts.append(rejected_summary)

        fulfillment_decision = FulfillmentDecision(
            status="fulfilled" if not rejected_bits else "partial",
            delivery_date=inventory_decision.delivery_date,
            staged_delivery=inventory_decision.staged_delivery,
            accepted_items=accepted_item_summaries,
            rejected_items=rejected_bits,
            transactions=transactions,
            customer_response=" ".join(response_parts),
        )
        return as_json(asdict(fulfillment_decision))


class PaperCompanyOrchestrator(BeaverChoiceAgent):
    """Orchestrator that routes inventory, quote, and fulfillment work between agents."""

    def __init__(self, model_to_use) -> None:
        self.inventory_agent = InventoryAgent(model_to_use)
        self.quote_agent = QuoteAgent(model_to_use)
        self.fulfillment_agent = FulfillmentAgent(model_to_use)

        @tool
        def assess_inventory(parsed_request_json: str) -> str:
            """
            Route a parsed request to the inventory agent.

            Args:
                parsed_request_json: JSON string representing the parsed customer request.

            Returns:
                JSON string with inventory assessment details.
            """
            return self.inventory_agent.run(parsed_request_json)

        @tool
        def build_quote(request_bundle_json: str) -> str:
            """
            Route an inventory-approved bundle to the quote agent.

            Args:
                request_bundle_json: JSON string with parsed request and inventory decision.

            Returns:
                JSON string with pricing details.
            """
            return self.quote_agent.run(request_bundle_json)

        @tool
        def finalize_order(order_bundle_json: str) -> str:
            """
            Route the final order bundle to the fulfillment agent.

            Args:
                order_bundle_json: JSON string with parsed request, inventory decision, and quote decision.

            Returns:
                JSON string with persisted transaction details and the customer response.
            """
            return self.fulfillment_agent.run(order_bundle_json)

        super().__init__(
            tools=[assess_inventory, build_quote, finalize_order],
            model_to_use=model_to_use,
            name="paper_company_orchestrator",
            description="Coordinates inventory assessment, quote generation, and order fulfillment for Beaver's Choice Paper Company.",
        )

    def run(self, task: str, stream: bool = False, reset: bool = True, images=None, additional_args=None, max_steps: int | None = None):
        parsed_request = parse_request(task)

        if not parsed_request.items and parsed_request.request_kind == "inventory_query":
            inventory_snapshot = safe_json_loads(inventory_snapshot_tool(parsed_request.request_date))
            report = safe_json_loads(financial_report_tool(parsed_request.request_date))
            top_items = list(inventory_snapshot.items())[:5]
            stock_lines = ", ".join([f"{name}: {qty}" for name, qty in top_items]) if top_items else "No inventory currently available."
            return (
                f"Beaver's Choice Paper Company inventory snapshot for {parsed_request.request_date}: "
                f"{stock_lines} Current cash balance: ${report['cash_balance']:.2f}."
            )

        parsed_request_json = as_json(asdict(parsed_request))
        inventory_decision = safe_json_loads(self.tools["assess_inventory"](parsed_request_json))

        if not inventory_decision["accepted_items"]:
            fulfillment_result = FulfillmentDecision(
                status="rejected",
                delivery_date=parsed_request.request_date,
                staged_delivery=False,
                accepted_items=[],
                rejected_items=inventory_decision["rejected_items"] + inventory_decision["unknown_items"],
                transactions=[],
                customer_response=(
                    "Beaver's Choice Paper Company could not confirm this order. "
                    + " ".join(
                        [
                            item["reason"]
                            for item in inventory_decision["rejected_items"] + inventory_decision["unknown_items"]
                        ]
                    )
                ),
            )
            return fulfillment_result.customer_response

        quote_bundle_json = as_json(
            {
                "parsed_request": asdict(parsed_request),
                "inventory_decision": inventory_decision,
            }
        )
        quote_decision = safe_json_loads(self.tools["build_quote"](quote_bundle_json))
        fulfillment_bundle_json = as_json(
            {
                "parsed_request": asdict(parsed_request),
                "inventory_decision": inventory_decision,
                "quote_decision": quote_decision,
            }
        )
        fulfillment_decision = safe_json_loads(self.tools["finalize_order"](fulfillment_bundle_json))
        return fulfillment_decision["customer_response"]


paper_company_system = None


def call_your_multi_agent_system(request_with_date: str) -> str:
    return paper_company_system.run(request_with_date)


# Run your test scenarios by writing them here. Make sure to keep track of them.

def run_test_scenarios():
    
    print("Initializing Database...")
    init_database()
    try:
        quote_requests_sample = pd.read_csv(PROJECT_DIR / "quote_requests_sample.csv")
        quote_requests_sample["request_date"] = pd.to_datetime(
            quote_requests_sample["request_date"], format="%m/%d/%y", errors="coerce"
        )
        quote_requests_sample.dropna(subset=["request_date"], inplace=True)
        quote_requests_sample = quote_requests_sample.sort_values("request_date")
    except Exception as e:
        print(f"FATAL: Error loading test data: {e}")
        return

    # Get initial state
    initial_date = quote_requests_sample["request_date"].min().strftime("%Y-%m-%d")
    report = generate_financial_report(initial_date)
    current_cash = report["cash_balance"]
    current_inventory = report["inventory_value"]

    ############
    ############
    ############
    # INITIALIZE YOUR MULTI AGENT SYSTEM HERE
    ############
    ############
    ############
    global paper_company_system
    paper_company_system = PaperCompanyOrchestrator(llm_model)

    results = []
    for idx, row in quote_requests_sample.iterrows():
        request_date = row["request_date"].strftime("%Y-%m-%d")

        print(f"\n=== Request {idx+1} ===")
        print(f"Context: {row['job']} organizing {row['event']}")
        print(f"Request Date: {request_date}")
        print(f"Cash Balance: ${current_cash:.2f}")
        print(f"Inventory Value: ${current_inventory:.2f}")

        # Process request
        request_with_date = f"{row['request']} (Date of request: {request_date})"

        ############
        ############
        ############
        # USE YOUR MULTI AGENT SYSTEM TO HANDLE THE REQUEST
        ############
        ############
        ############
        response = call_your_multi_agent_system(request_with_date)

        # Update state
        report = generate_financial_report(request_date)
        current_cash = report["cash_balance"]
        current_inventory = report["inventory_value"]

        print(f"Response: {response}")
        print(f"Updated Cash: ${current_cash:.2f}")
        print(f"Updated Inventory: ${current_inventory:.2f}")

        results.append(
            {
                "request_id": idx + 1,
                "request_date": request_date,
                "cash_balance": current_cash,
                "inventory_value": current_inventory,
                "response": response,
            }
        )

        time.sleep(1)

    # Final report
    final_date = quote_requests_sample["request_date"].max().strftime("%Y-%m-%d")
    final_report = generate_financial_report(final_date)
    print("\n===== FINAL FINANCIAL REPORT =====")
    print(f"Final Cash: ${final_report['cash_balance']:.2f}")
    print(f"Final Inventory: ${final_report['inventory_value']:.2f}")

    # Save results
    pd.DataFrame(results).to_csv(PROJECT_DIR / "test_results.csv", index=False)
    return results


if __name__ == "__main__":
    results = run_test_scenarios()
