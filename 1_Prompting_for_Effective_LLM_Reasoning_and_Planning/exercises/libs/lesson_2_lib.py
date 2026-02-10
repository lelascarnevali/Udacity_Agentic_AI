import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
from IPython.display import Markdown, display

class OpenAIModels(str, Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_41_MINI = "gpt-4.1-mini"
    GPT_41_NANO = "gpt-4.1-nano"

# Helper function to display responses as Markdown, horizontally
def display_responses(*args):
    markdown_string = "<table><tr>"
    # Headers
    for arg in args:
        markdown_string += f"<th>System Prompt:<br />{arg['system_prompt']}<br /><br />"
        markdown_string += f"User Prompt:<br />{arg['user_prompt']}</th>"
    markdown_string += "</tr>"
    # Rows
    markdown_string += "<tr>"
    for arg in args:
        markdown_string += f"<td>Response:<br />{arg['response']}</td>"
    markdown_string += "</tr></table>"
    display(Markdown(markdown_string))

def get_completion(system_prompt, user_prompt, model="gpt-4.1-nano", client = None):
    """
    Function to get a completion from the OpenAI API.
    Args:
        system_prompt: The system prompt
        user_prompt: The user prompt
        model: The model to use (default is gpt-4.1-mini)
    Returns:
        The completion text
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

    
def get_sales_data(products: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    data = [
        {
            "date": datetime.date(2024, 1, 10),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 255,
            "revenue": 15547.35,
        },
        {
            "date": datetime.date(2024, 1, 10),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 65,
            "revenue": 2297.1,
        },
        {
            "date": datetime.date(2024, 1, 10),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 90,
            "revenue": 7301.7,
        },
        {
            "date": datetime.date(2024, 1, 10),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 171,
            "revenue": 8296.92,
        },
        {
            "date": datetime.date(2024, 1, 10),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 96,
            "revenue": 2587.2,
        },
        {
            "date": datetime.date(2024, 1, 11),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 235,
            "revenue": 14327.95,
        },
        {
            "date": datetime.date(2024, 1, 11),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 86,
            "revenue": 3039.24,
        },
        {
            "date": datetime.date(2024, 1, 11),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 79,
            "revenue": 6409.27,
        },
        {
            "date": datetime.date(2024, 1, 11),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 145,
            "revenue": 7035.4,
        },
        {
            "date": datetime.date(2024, 1, 11),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 114,
            "revenue": 3072.3,
        },
        {
            "date": datetime.date(2024, 1, 12),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 310,
            "revenue": 18900.7,
        },
        {
            "date": datetime.date(2024, 1, 12),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 80,
            "revenue": 2827.2,
        },
        {
            "date": datetime.date(2024, 1, 12),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 108,
            "revenue": 8762.04,
        },
        {
            "date": datetime.date(2024, 1, 12),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 143,
            "revenue": 6938.36,
        },
        {
            "date": datetime.date(2024, 1, 12),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 342,
            "revenue": 9216.9,
        },
        {
            "date": datetime.date(2024, 1, 13),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 302,
            "revenue": 18412.94,
        },
        {
            "date": datetime.date(2024, 1, 13),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 68,
            "revenue": 2403.12,
        },
        {
            "date": datetime.date(2024, 1, 13),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 96,
            "revenue": 7788.48,
        },
        {
            "date": datetime.date(2024, 1, 13),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 130,
            "revenue": 6307.6,
        },
        {
            "date": datetime.date(2024, 1, 13),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 103,
            "revenue": 2775.85,
        },
        {
            "date": datetime.date(2024, 1, 14),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 305,
            "revenue": 18595.85,
        },
        {
            "date": datetime.date(2024, 1, 14),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 84,
            "revenue": 2968.56,
        },
        {
            "date": datetime.date(2024, 1, 14),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 99,
            "revenue": 8031.87,
        },
        {
            "date": datetime.date(2024, 1, 14),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 167,
            "revenue": 8102.84,
        },
        {
            "date": datetime.date(2024, 1, 14),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 104,
            "revenue": 2802.8,
        },
        {
            "date": datetime.date(2024, 1, 15),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 301,
            "revenue": 18351.97,
        },
        {
            "date": datetime.date(2024, 1, 15),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 73,
            "revenue": 2579.82,
        },
        {
            "date": datetime.date(2024, 1, 15),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 89,
            "revenue": 7220.57,
        },
        {
            "date": datetime.date(2024, 1, 15),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 126,
            "revenue": 6113.52,
        },
        {
            "date": datetime.date(2024, 1, 15),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 100,
            "revenue": 2695.0,
        },
        {
            "date": datetime.date(2024, 1, 16),
            "product_id": "P001",
            "product_name": "Product 1",
            "quantity": 226,
            "revenue": 13779.22,
        },
        {
            "date": datetime.date(2024, 1, 16),
            "product_id": "P002",
            "product_name": "Product 2",
            "quantity": 80,
            "revenue": 2827.2,
        },
        {
            "date": datetime.date(2024, 1, 16),
            "product_id": "P003",
            "product_name": "Product 3",
            "quantity": 83,
            "revenue": 6733.79,
        },
        {
            "date": datetime.date(2024, 1, 16),
            "product_id": "P004",
            "product_name": "Product 4",
            "quantity": 175,
            "revenue": 8491.0,
        },
        {
            "date": datetime.date(2024, 1, 16),
            "product_id": "P005",
            "product_name": "Product 5",
            "quantity": 125,
            "revenue": 3368.75,
        },
    ]
    if products:
        return [item for item in data if item["product_id"] in products]
    return data


def get_promotions_data() -> List[Dict[str, Any]]:
    import datetime

    data = [
        {
            "promotion_id": "PROMO001",
            "name": "Weekend Special",
            "discount": "10% off",
            "products": ["P002"],
            "start_date": datetime.date(2024, 1, 12),
            "end_date": datetime.date(2024, 1, 14),
        },
        {
            "promotion_id": "PROMO002",
            "name": "Flash Sale",
            "discount": "15% off",
            "products": ["P001", "P003", "P005"],
            "start_date": datetime.date(2024, 1, 15),
            "end_date": datetime.date(2024, 1, 16),
        },
    ]
    return data


def get_weather_data() -> List[Dict[str, Any]]:
    data = [
        {
            "date": "2024-01-10",
            "temperature": {"fahrenheit": 23.4, "celsius": -4.8},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
        {
            "date": "2024-01-11",
            "temperature": {"fahrenheit": 39.3, "celsius": 4.1},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
        {
            "date": "2024-01-12",
            "temperature": {"fahrenheit": 41.1, "celsius": 5.1},
            "conditions": {
                "main": "Heavy Rain",
                "precipitation": "Heavy Rain",
                "precipitation_amount": 2.7,
                "special_event": "Flood Warning",
            },
        },
        {
            "date": "2024-01-13",
            "temperature": {"fahrenheit": 27.2, "celsius": -2.6},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
        {
            "date": "2024-01-14",
            "temperature": {"fahrenheit": 22.9, "celsius": -5.1},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
        {
            "date": "2024-01-15",
            "temperature": {"fahrenheit": 33.2, "celsius": 0.7},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": "High Winds",
            },
        },
        {
            "date": "2024-01-16",
            "temperature": {"fahrenheit": 23.3, "celsius": -4.8},
            "conditions": {
                "main": "Clear",
                "precipitation": "None",
                "precipitation_amount": 0,
                "special_event": None,
            },
        },
    ]
    return data


def call_weather_api(date: str) -> Dict[str, Any]:
    data = get_weather_data()

    data = {item["date"]: item for item in data}
    return data[date]


def get_competitor_pricing_data():
    data = [
        {
            "product": "Product 1",
            "date": "2024-01-10",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 56.88,
            "competitor_b_price": 62.23,
            "competitor_c_price": 51.8,
        },
        {
            "product": "Product 1",
            "date": "2024-01-11",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 59.65,
            "competitor_b_price": 72.47,
            "competitor_c_price": 72.5,
        },
        {
            "product": "Product 1",
            "date": "2024-01-12",
            "our_price": 60.97,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 69.24,
                    "sale_price": 50.55,
                    "discount_percentage": 27,
                },
                "CompetitorC": {
                    "original_price": 49.92,
                    "sale_price": 39.44,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 65.4,
            "competitor_b_price": 50.55,
            "competitor_c_price": 39.44,
        },
        {
            "product": "Product 1",
            "date": "2024-01-13",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 72.13,
            "competitor_b_price": 57.54,
            "competitor_c_price": 51.1,
        },
        {
            "product": "Product 1",
            "date": "2024-01-14",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 72.36,
            "competitor_b_price": 70.04,
            "competitor_c_price": 61.04,
        },
        {
            "product": "Product 1",
            "date": "2024-01-15",
            "our_price": 60.97,
            "competitor_sales": {},
            "competitor_a_price": 68.52,
            "competitor_b_price": 59.63,
            "competitor_c_price": 73.03,
        },
        {
            "product": "Product 1",
            "date": "2024-01-16",
            "our_price": 60.97,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 53.84,
                    "sale_price": 44.69,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 44.69,
            "competitor_b_price": 57.69,
            "competitor_c_price": 70.51,
        },
        {
            "product": "Product 2",
            "date": "2024-01-10",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 34.57,
            "competitor_b_price": 42.01,
            "competitor_c_price": 42.02,
        },
        {
            "product": "Product 2",
            "date": "2024-01-11",
            "our_price": 35.34,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 40.13,
                    "sale_price": 29.29,
                    "discount_percentage": 27,
                },
                "CompetitorC": {
                    "original_price": 28.93,
                    "sale_price": 22.85,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 37.91,
            "competitor_b_price": 29.29,
            "competitor_c_price": 22.85,
        },
        {
            "product": "Product 2",
            "date": "2024-01-12",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 41.81,
            "competitor_b_price": 33.35,
            "competitor_c_price": 29.62,
        },
        {
            "product": "Product 2",
            "date": "2024-01-13",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 41.94,
            "competitor_b_price": 40.6,
            "competitor_c_price": 35.38,
        },
        {
            "product": "Product 2",
            "date": "2024-01-14",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 39.71,
            "competitor_b_price": 34.56,
            "competitor_c_price": 42.33,
        },
        {
            "product": "Product 2",
            "date": "2024-01-15",
            "our_price": 35.34,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 31.21,
                    "sale_price": 25.9,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 25.9,
            "competitor_b_price": 33.44,
            "competitor_c_price": 40.87,
        },
        {
            "product": "Product 2",
            "date": "2024-01-16",
            "our_price": 35.34,
            "competitor_sales": {},
            "competitor_a_price": 33.86,
            "competitor_b_price": 28.92,
            "competitor_c_price": 41.03,
        },
        {
            "product": "Product 3",
            "date": "2024-01-10",
            "our_price": 81.13,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 92.14,
                    "sale_price": 67.26,
                    "discount_percentage": 27,
                },
                "CompetitorC": {
                    "original_price": 66.42,
                    "sale_price": 52.47,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 87.02,
            "competitor_b_price": 67.26,
            "competitor_c_price": 52.47,
        },
        {
            "product": "Product 3",
            "date": "2024-01-11",
            "our_price": 81.13,
            "competitor_sales": {},
            "competitor_a_price": 95.98,
            "competitor_b_price": 76.56,
            "competitor_c_price": 68.0,
        },
        {
            "product": "Product 3",
            "date": "2024-01-12",
            "our_price": 81.13,
            "competitor_sales": {},
            "competitor_a_price": 96.29,
            "competitor_b_price": 93.2,
            "competitor_c_price": 81.22,
        },
        {
            "product": "Product 3",
            "date": "2024-01-13",
            "our_price": 81.13,
            "competitor_sales": {},
            "competitor_a_price": 91.17,
            "competitor_b_price": 79.35,
            "competitor_c_price": 97.18,
        },
        {
            "product": "Product 3",
            "date": "2024-01-14",
            "our_price": 81.13,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 71.64,
                    "sale_price": 59.46,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 59.46,
            "competitor_b_price": 76.76,
            "competitor_c_price": 93.83,
        },
        {
            "product": "Product 3",
            "date": "2024-01-15",
            "our_price": 81.13,
            "competitor_sales": {},
            "competitor_a_price": 77.73,
            "competitor_b_price": 66.39,
            "competitor_c_price": 94.19,
        },
        {
            "product": "Product 3",
            "date": "2024-01-16",
            "our_price": 81.13,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 80.32,
                    "sale_price": 63.45,
                    "discount_percentage": 21,
                }
            },
            "competitor_a_price": 63.45,
            "competitor_b_price": 87.76,
            "competitor_c_price": 81.93,
        },
        {
            "product": "Product 4",
            "date": "2024-01-10",
            "our_price": 48.52,
            "competitor_sales": {},
            "competitor_a_price": 57.4,
            "competitor_b_price": 45.79,
            "competitor_c_price": 40.67,
        },
        {
            "product": "Product 4",
            "date": "2024-01-11",
            "our_price": 48.52,
            "competitor_sales": {},
            "competitor_a_price": 57.59,
            "competitor_b_price": 55.74,
            "competitor_c_price": 48.58,
        },
        {
            "product": "Product 4",
            "date": "2024-01-12",
            "our_price": 48.52,
            "competitor_sales": {},
            "competitor_a_price": 54.52,
            "competitor_b_price": 47.45,
            "competitor_c_price": 58.12,
        },
        {
            "product": "Product 4",
            "date": "2024-01-13",
            "our_price": 48.52,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 42.85,
                    "sale_price": 35.57,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 35.57,
            "competitor_b_price": 45.91,
            "competitor_c_price": 56.11,
        },
        {
            "product": "Product 4",
            "date": "2024-01-14",
            "our_price": 48.52,
            "competitor_sales": {},
            "competitor_a_price": 46.49,
            "competitor_b_price": 39.7,
            "competitor_c_price": 56.33,
        },
        {
            "product": "Product 4",
            "date": "2024-01-15",
            "our_price": 48.52,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 48.04,
                    "sale_price": 37.95,
                    "discount_percentage": 21,
                }
            },
            "competitor_a_price": 37.95,
            "competitor_b_price": 52.48,
            "competitor_c_price": 49.0,
        },
        {
            "product": "Product 4",
            "date": "2024-01-16",
            "our_price": 48.52,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 50.93,
                    "sale_price": 45.84,
                    "discount_percentage": 10,
                },
                "CompetitorC": {
                    "original_price": 51.01,
                    "sale_price": 40.3,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 41.82,
            "competitor_b_price": 45.84,
            "competitor_c_price": 40.3,
        },
        {
            "product": "Product 5",
            "date": "2024-01-10",
            "our_price": 26.95,
            "competitor_sales": {},
            "competitor_a_price": 31.99,
            "competitor_b_price": 30.96,
            "competitor_c_price": 26.98,
        },
        {
            "product": "Product 5",
            "date": "2024-01-11",
            "our_price": 26.95,
            "competitor_sales": {},
            "competitor_a_price": 30.29,
            "competitor_b_price": 26.36,
            "competitor_c_price": 32.28,
        },
        {
            "product": "Product 5",
            "date": "2024-01-12",
            "our_price": 26.95,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 23.8,
                    "sale_price": 19.75,
                    "discount_percentage": 17,
                }
            },
            "competitor_a_price": 19.75,
            "competitor_b_price": 25.5,
            "competitor_c_price": 31.17,
        },
        {
            "product": "Product 5",
            "date": "2024-01-13",
            "our_price": 26.95,
            "competitor_sales": {},
            "competitor_a_price": 25.82,
            "competitor_b_price": 22.05,
            "competitor_c_price": 31.29,
        },
        {
            "product": "Product 5",
            "date": "2024-01-14",
            "our_price": 26.95,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 26.68,
                    "sale_price": 21.08,
                    "discount_percentage": 21,
                }
            },
            "competitor_a_price": 21.08,
            "competitor_b_price": 29.15,
            "competitor_c_price": 27.21,
        },
        {
            "product": "Product 5",
            "date": "2024-01-15",
            "our_price": 26.95,
            "competitor_sales": {
                "CompetitorB": {
                    "original_price": 28.29,
                    "sale_price": 25.46,
                    "discount_percentage": 10,
                },
                "CompetitorC": {
                    "original_price": 28.33,
                    "sale_price": 22.38,
                    "discount_percentage": 21,
                },
            },
            "competitor_a_price": 23.23,
            "competitor_b_price": 25.46,
            "competitor_c_price": 22.38,
        },
        {
            "product": "Product 5",
            "date": "2024-01-16",
            "our_price": 26.95,
            "competitor_sales": {
                "CompetitorA": {
                    "original_price": 27.28,
                    "sale_price": 24.01,
                    "discount_percentage": 12,
                },
                "CompetitorB": {
                    "original_price": 24.9,
                    "sale_price": 19.42,
                    "discount_percentage": 22,
                },
                "CompetitorC": {
                    "original_price": 30.56,
                    "sale_price": 23.53,
                    "discount_percentage": 23,
                },
            },
            "competitor_a_price": 24.01,
            "competitor_b_price": 19.42,
            "competitor_c_price": 23.53,
        },
    ]
    return data


def call_competitor_pricing_api(
    product_name: str, date: datetime.date
) -> Dict[str, Any]:
    data = get_competitor_pricing_data()
    data_by_product_name_and_date = {
        (item["product"], item["date"]): item for item in data
    }
    try:
        return data_by_product_name_and_date[(product_name, date.strftime("%Y-%m-%d"))]
    except KeyError:
        print(f"No data found for product {product_name} and date {date}")
        return None


SINGLE_TAB_LEVEL = 4


def print_in_box(text, title="", cols=100, tab_level=0):
    """
    Prints the given text in a box with the specified title and dimensions.

    Args:
        text: The text to print in the box.
        title: The title of the box.
        cols: The width of the box.
        tab_level: The level of indentation for the box.
    """
    import textwrap

    text = str(text)

    # Make a box using extended ASCII characters
    if cols < 4 + tab_level * SINGLE_TAB_LEVEL:
        cols = 4 + tab_level * SINGLE_TAB_LEVEL

    tabs = " " * tab_level * SINGLE_TAB_LEVEL

    top = (
        tabs
        + "\u2554"
        + "\u2550" * (cols - 2 - tab_level * SINGLE_TAB_LEVEL)
        + "\u2557"
    )
    if tab_level == 0:
        print()  # Print a newline before any box at level 0

    if title:
        # replace the middle of the top with the title
        title = "[ " + title + " ]"
        top = top[: (cols - len(title)) // 2] + title + top[(cols + len(title)) // 2 :]
    print(top)

    for line in text.split("\n"):
        for wrapped_line in textwrap.wrap(
            line, cols - 4 - tab_level * SINGLE_TAB_LEVEL
        ):
            print(
                f"{tabs}\u2551 {wrapped_line:<{cols - 4 - tab_level * SINGLE_TAB_LEVEL}} \u2551"
            )

    print(
        f"{tabs}\u255a"
        + "\u2550" * (cols - 2 - tab_level * SINGLE_TAB_LEVEL)
        + "\u255d"
    )
