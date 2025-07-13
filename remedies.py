import requests
import streamlit as st
from prettytable import PrettyTable
import base64
import os

def get_base64_image():
    for ext in ["webp", "jpg", "jpeg", "png"]:
        image_path = f"remedies2.{ext}"
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return None

bg_img = get_base64_image()

# --- Page Setup ---
if bg_img:
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.35), rgba(255, 255, 255, 0.15)),
                        url("data:image/png;base64,{bg_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 248, 243, 0.45);
            padding: 2rem 3rem;
            border-radius: 18px;
            margin-top: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #4B4B4B;
            font-family: 'Segoe UI', sans-serif;
        }}
        .export-buttons {{
            margin-top: 20px;
        }}
        .sidebar .sidebar-content {{
            background-color: rgba(255, 248, 243, 0.85);
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        </style>
    """, unsafe_allow_html=True)
st.markdown("""
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #c04600;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] * {
        color: #f0e0d7 !important;
    }

    /* Input fields inside sidebar */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea,
    [data-testid="stSidebar"] select {
        background-color: #d15410 !important;
        color: #f0e0d7 !important;
        border-color: #f0e0d7;
    }

    /* Main heading color */
    h1, h2, h3, h4, h5, h6 {
        color: #c04600 !important;
    }
    </style>
    """, unsafe_allow_html=True)
def get_season_by_weather(location):
    api_key = "7714caab332a0e2f942a94a82b500946"  # Replace with your actual OpenWeather API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    try:
        response = requests.get(base_url, params={"q": location, "appid": api_key, "units": "metric"})
        if response.status_code == 200:
            data = response.json()
            month = int(data['dt'])  # Unix time to determine the current month
            if 3 <= month <= 5:
                return "Spring"
            elif 6 <= month <= 8:
                return "Summer"
            elif 9 <= month <= 11:
                return "Autumn"
            else:
                return "Winter"
        else:
            st.error(f"Error: Unable to fetch weather data (status code {response.status_code}).")
            return None
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def display_remedies_table(remedies):
    """Display remedies in a vertical tabular format with uniform column width and borders."""
    for remedy in remedies:
        table = PrettyTable()
        table.field_names = ["Attribute", "Details"]
        table.align["Attribute"] = "l"
        table.align["Details"] = "l"
        
        # Calculate the max length for 'Details' column to make sure all columns are uniform
        max_length = max(
            len(remedy["remedy"]),
            len(remedy["ingredients"]),
            len(remedy["method"]),
            len(remedy["application"]),
            len(remedy["frequency"]),
            len(remedy["tips"]),
            len(remedy["how_it_works"]),
            len(remedy["benefits"])
        )

        # Set a uniform width for the "Details" column to ensure consistency
        table._max_width = {"Details": max_length + 5}  # Adding extra space for padding

        # Add rows to the table
        table.add_row(["Remedy", remedy["remedy"]])
        table.add_row(["Ingredients", remedy["ingredients"]])
        table.add_row(["Method", remedy["method"]])
        table.add_row(["Application", remedy["application"]])
        table.add_row(["Frequency", remedy["frequency"]])
        table.add_row(["Tips", remedy["tips"]])
        table.add_row(["How It Works", remedy["how_it_works"]])
        table.add_row(["Benefits", remedy["benefits"]])

        # Display the table
        st.write(table)

def main():
    # Display the title and introduction
    st.title("Skin Care Remedies & Seasonal Information")

    # Create sidebar for inputs
    with st.sidebar:
        st.header("User Information")
        name = st.text_input("What's your name?")
        age = st.number_input("How old are you?", min_value=1, max_value=120)
        skin_concern = st.text_input("What is your primary skin concern? (e.g., acne, dry skin, pigmentation, etc.): ").strip().lower()
        location = st.text_input("Please enter your location (city): ")

        # Fetch the season based on location
        if location:
            season = get_season_by_weather(location)
            if season:
                st.success(f"The current season in {location} is {season}.")
            else:
                st.warning("Sorry, we couldn't determine the season based on your location.")

    # Define the remedies data
    remedies = {
        "acne": [
            {
                "remedy": "Honey-Turmeric Mask",
                "ingredients": "1 tbsp raw honey, 1/2 tsp turmeric",
                "method": "Mix honey & turmeric into a paste.",
                "application": "Apply on clean face. Leave 15 min. Rinse.",
                "frequency": "Twice a week",
                "tips": "Drink water; cleanse face before applying.",
                "how_it_works": "Honey fights bacteria; turmeric calms skin.",
                "benefits": "Helps reduce acne and inflammation, brightens skin."
            },
            {
                "remedy": "Green Tea-Toner Mask",
                "ingredients": "2 tbsp brewed green tea, 1 tbsp rice flour",
                "method": "Mix tea & flour into a paste.",
                "application": "Apply to face. Leave 15 min. Rinse.",
                "frequency": "Once a week",
                "tips": "Use cooled tea; store toner in fridge.",
                "how_it_works": "Tea reduces oil; rice flour exfoliates.",
                "benefits": "Fights acne-causing bacteria and unclogs pores."
            }
        ],
        "dry skin": [
            {
                "remedy": "Aloe Vera-Coconut Moisturizer",
                "ingredients": "2 tbsp aloe vera, 1 tbsp coconut oil",
                "method": "Mix aloe & coconut oil.",
                "application": "Apply on skin. Leave 20 min. Rinse.",
                "frequency": "Daily",
                "tips": "Apply on damp skin; drink water.",
                "how_it_works": "Aloe hydrates; coconut oil locks moisture.",
                "benefits": "Hydrates dry skin and soothes irritation."
            },
            {
                "remedy": "Banana-Yogurt Hydration",
                "ingredients": "1 ripe banana, 1 tbsp yogurt",
                "method": "Mash banana; mix with yogurt.",
                "application": "Apply to dry areas. Leave 15 min. Rinse.",
                "frequency": "Every other day",
                "tips": "Use ripe banana; follow with moisturizer.",
                "how_it_works": "Banana nourishes; yogurt exfoliates.",
                "benefits": "Moisturizes and nourishes the skin, leaving it soft."
            }
        ],
        "pigmentation": [
            {
                "remedy": "Lemon-Turmeric Spot Treatment",
                "ingredients": "1 tbsp lemon juice, 1/4 tsp turmeric",
                "method": "Mix lemon juice and turmeric.",
                "application": "Apply to dark spots. Leave 10 min. Rinse.",
                "frequency": "Once a week",
                "tips": "Use SPF after treatment.",
                "how_it_works": "Lemon brightens skin; turmeric reduces dark spots.",
                "benefits": "Helps lighten pigmentation and uneven skin tone."
            },
            {
                "remedy": "Papaya-Aloe Vera Mask",
                "ingredients": "1/2 papaya, 1 tbsp aloe vera",
                "method": "Mash papaya; mix with aloe vera.",
                "application": "Apply to skin. Leave 15 min. Rinse.",
                "frequency": "Twice a week",
                "tips": "Avoid sun exposure immediately after.",
                "how_it_works": "Papaya brightens skin; aloe soothes.",
                "benefits": "Reduces pigmentation and evens out skin tone."
            }
        ],
        "blackheads": [
            {
                "remedy": "Baking Soda Face Scrub",
                "ingredients": "1 tbsp baking soda, 1 tbsp water",
                "method": "Mix baking soda with water to form paste.",
                "application": "Gently scrub on affected areas for 2-3 min.",
                "frequency": "Once a week",
                "tips": "Avoid over-scrubbing; moisturize after.",
                "how_it_works": "Baking soda unclogs pores.",
                "benefits": "Helps remove blackheads and dead skin cells."
            },
            {
                "remedy": "Charcoal Face Mask",
                "ingredients": "2 tbsp activated charcoal powder, 1 tbsp water",
                "method": "Mix charcoal with water to form paste.",
                "application": "Apply to face. Leave for 15 min. Rinse.",
                "frequency": "Once a week",
                "tips": "Use a toner afterward to close pores.",
                "how_it_works": "Charcoal absorbs impurities and dirt.",
                "benefits": "Unclogs pores and prevents blackheads."
            }
        ],
        "oily skin": [
            {
                "remedy": "Cucumber-Mint Toner",
                "ingredients": "1 cucumber, 1/4 cup mint leaves",
                "method": "Blend cucumber and mint. Strain to extract juice.",
                "application": "Apply toner with cotton ball.",
                "frequency": "Daily",
                "tips": "Store in fridge for a cooling effect.",
                "how_it_works": "Cucumber hydrates; mint controls oil.",
                "benefits": "Balances oil production and refreshes skin."
            },
            {
                "remedy": "Apple Cider Vinegar Mask",
                "ingredients": "2 tbsp apple cider vinegar, 1 tbsp honey",
                "method": "Mix apple cider vinegar with honey.",
                "application": "Apply to face. Leave for 10 min. Rinse.",
                "frequency": "Once a week",
                "tips": "Dilute with water if too strong.",
                "how_it_works": "ACV balances pH; honey soothes.",
                "benefits": "Controls oil and prevents acne breakouts."
            }
        ],
    }

    # Display remedies in the main area
    if skin_concern in remedies:
        st.subheader(f"Here are remedies for your concern ({skin_concern}):")
        display_remedies_table(remedies[skin_concern])
    elif skin_concern:
        st.warning(f"Sorry, we don't have remedies for {skin_concern}.")
    else:
        st.info("Please enter your skin concern in the sidebar to see remedies.")

if __name__ == "__main__":
    main()
