import tempfile
import streamlit as st

from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_car_restoration_preferences():
    st.markdown("---")
    col1, col2 = st.columns(2)

    # Column 1: Image Upload
    with col1:
        st.subheader("📸 Upload Car Image")
        uploaded_image = st.file_uploader(
            "Upload a photo of the vintage car you'd like to restore",
            type=["jpg", "jpeg", "png"]
        )

    # Column 2: Restoration Preferences
    with col2:
        st.subheader("🛠️ Restoration Preferences")

        design_approach = st.selectbox(
            "How should the restoration be approached?",
            ["Preserve Authenticity", "Subtle Modern Touches", "Full Restomod Makeover"]
        )

        styling_flavor = st.selectbox(
            "What's your preferred aesthetic direction?",
            ["Factory Original", "Retro Sport", "Contemporary Custom", "Luxury Collector", "Daily Driver Revival"]
        )

    return {
        "uploaded_image": uploaded_image,
        "design_approach": design_approach,
        "styling_flavor": styling_flavor
    }

def generate_restoration_report(user_car_restoration_preferences: dict):
    # Save uploaded image to a temporary file
    uploaded_image = user_car_restoration_preferences["uploaded_image"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_image.getvalue())
        image_path = tmp.name

    design_approach = user_car_restoration_preferences["design_approach"]
    styling_flavor = user_car_restoration_preferences["styling_flavor"]

    # Agent 1: Car Historian Agent
    car_historian_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Car Historian",
        role="Identifies the vintage car's model, decade, and visual characteristics.",
        description="You analyze the uploaded car image and identify its model, year, and design features.",
        instructions=[
            "Carefully examine the uploaded car photo.",
            "Identify the likely make, model, and decade of origin.",
            "Describe visual elements such as body style, grille, headlights, trim, and wheels.",
            "Output format:\n\n"
            "### 🧭 Detected Model & Era: **<Make + Model, Decade>**\n\n"
            "*Based on visual analysis of the uploaded car image.*\n\n"
            "### 🔍 Key Exterior Features\n\n"
            "| Feature | Description |\n|---------|-------------|\n| ... | ... |"
        ],
        markdown=True
    )
    history_response = car_historian_agent.run("Analyze the car and identify its model and decade.", images=[Image(filepath=image_path)])
    history_section = history_response.content

    # Agent 2: Design Context Agent
    context_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Design Context Agent",
        role="Explains the cultural and automotive significance of the identified car model.",
        description="You provide context about the car’s design influence, usage, and collector appeal.",
        instructions=[
            "Read the identified car model and decade.",
            "Describe what made this car historically or culturally significant.",
            "Include its role in automotive design history, pop culture, or innovation.",
            "Format using:\n\n"
            "### 📚 Historical & Cultural Significance"
        ],
        markdown=True
    )
    context_response = context_agent.run(history_section)
    context_section = context_response.content

    # Agent 3: Restoration Stylist Agent
    stylist_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Restoration Stylist",
        role="Suggests how to restore or modernize the vehicle based on the user's preference.",
        description="You provide design advice for restoration based on the original car style and user customization goals.",
        instructions=[
            "Based on the detected car and user preferences, suggest a restoration direction.",
            "Balance originality with the desired makeover level (preservation, blend, or modern).",
            "Include suggestions for paint colors, trims, tires, interior styling, etc.",
            "Use the following format:\n\n"
            "### ✨ Restoration Strategy\n\n"
            "| Element | Recommendation |\n|---------|------------------|\n| ... | ... |\n\n"
            "> 🔧 Styling Tip: [Give a one-line strategy summary here]\n\n"
            "### 🚘 How to Bring It Back\n\n"
            "- Bullet points for paint, interior, tires, emblems, etc."
        ],
        markdown=True
    )

    restoration_prompt = f"{history_section}\n\nApproach: {design_approach}\nStyling: {styling_flavor}"
    stylist_response = stylist_agent.run(restoration_prompt)
    stylist_section = stylist_response.content

    # Agent 4: Parts Finder Agent
    parts_agent = Agent(
        name="Parts Finder Agent",
        role="Finds aftermarket or OEM parts to help restore the car authentically or creatively.",
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        description=dedent("""
            You assist in finding real restoration parts based on the car model and restoration strategy.
            Source usable links from platforms like eBay, Summit Racing, Classic Industries, or Etsy.
        """),
        instructions=[
            "Use the restoration context and generate a focused parts search query.",
            "Use `search_google` to fetch part links based on model and styling preference.",
            "Extract 6–8 relevant product links to body panels, lights, tires, badges, or trim.",
            "Do not show ads or blog links. Use:\n\n"
            "### 🛠️ Recommended Parts & Accessories\n\n"
            "> *Helpful for completing your restoration:*\n\n"
            "- [Part Name or Type](https://example.com)"
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        markdown=True,
        add_datetime_to_instructions=True
    )
    parts_response = parts_agent.run(restoration_prompt)
    parts_section = parts_response.content

    # Final Commentary
    closing_remarks = (
        "### 💬 Restoration Reflection\n\n"
        "> “This vintage gem carries the spirit of a bygone era. Whether you're restoring it for the road or for display, balance form and function to let its story roll on.”\n"
    )

    # Assemble full report
    full_report = (
        "## 🚗 Vintage Car Restoration Report\n\n"
        f"{history_section}\n\n---\n\n"
        f"{context_section}\n\n---\n\n"
        f"{stylist_section}\n\n---\n\n"
        f"{parts_section}\n\n---\n\n"
        f"{closing_remarks}"
    )

    return full_report

def main() -> None:
    # Page config
    st.set_page_config(page_title="Vintage Car Restorer Bot", page_icon="🚗", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🚗 Vintage Car Restorer Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Vintage Car Restorer Bot — a Streamlit-powered automotive companion that interprets vintage car visuals, highlights historical significance, and helps you reimagine each ride with restoration tips and sourcing options.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_car_restoration_preferences = render_car_restoration_preferences()

    st.markdown("---")

    # UI button to trigger car restoration report generation
    if st.button("🔧 Generate Car Restoration Report"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        elif not user_car_restoration_preferences["uploaded_image"]:
            st.error("Please upload a vintage car image to proceed.")
        else:
            with st.spinner("Analyzing your car and preparing the restoration report..."):
                restoration_report = generate_restoration_report(user_car_restoration_preferences)

                # Save results to session state
                st.session_state.restoration_report = restoration_report
                st.session_state.uploaded_image = user_car_restoration_preferences["uploaded_image"]

    # Display result if available
    if "restoration_report" in st.session_state and "uploaded_image" in st.session_state:
        st.markdown("## 🖼️ Uploaded Car Image")
        st.image(st.session_state.uploaded_image, use_container_width=False)

        st.markdown(st.session_state.restoration_report, unsafe_allow_html=True)

        st.markdown("---")

        st.download_button(
            label="📥 Download Restoration Report",
            data=st.session_state.restoration_report,
            file_name="car_restoration_report.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()