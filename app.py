import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
from scipy.stats import skew
from streamlit_option_menu import option_menu

# Configure the page
st.set_page_config(
    page_title="Invistico Airlines: A Data Journey",
    layout="wide",
    initial_sidebar_state="collapsed",  # Add this line
)

# Function to load Lottie animations
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load animations with valid URLs
welcome_animation_url = "https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json"  # Celebration animation
closing_animation_url = "https://assets8.lottiefiles.com/packages/lf20_x62chJ.json"  # Thank you animation

# Sidebar navigation using option menu
menu_options = ["Welcome", "Discover the Data", "Unveil Insights", "Our Journey"]

# Horizontal menu
selected_menu = option_menu(None, menu_options, 
    icons=['house', 'bar-chart-line', 'search', 'rocket'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

# Load the Dataset
@st.cache_data
def load_data():
    df = pd.read_csv('Invistico_Airline.csv')
    return df

df = load_data()

# Add this custom CSS after the st.set_page_config() call
st.markdown("""
<style>
    .block-container {
        max-width: 1200px;
        padding-right: 1rem;
        padding-left: 1rem;
    }
    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

if selected_menu == "Welcome":
    # Welcome Page with Animation
    st.markdown(
        """
        <h1 style='text-align: center; font-size: 60px;'>Welcome to Invistico Airlines Data Journey</h1>
        """,
        unsafe_allow_html=True,
    )

    lottie_welcome = load_lottieurl(welcome_animation_url)
    if lottie_welcome:
        st_lottie(lottie_welcome, height=300, key="welcome")
    else:
        st.error("Failed to load the welcome animation.")

    st.markdown(
        """
        <h2 style='text-align: center;'>An Interactive Exploration of the Invistico Airline Dataset</h2>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        **Embark on an adventure** where data meets storytelling. Dive deep into the patterns and insights hidden within the airline industry's customer satisfaction data.

        **Use the navigation bar** to choose what you want to explore. Whether it's understanding passenger demographics, flight operations, or uncovering factors affecting delays, this app puts you in control.

        **Let's begin the journey!**
        """
    )

elif selected_menu == "Discover the Data":
    st.title("Discover the Data 📈")

    st.markdown(
        """
        The **Invistico Airline Dataset** is a comprehensive collection of information about airline passengers, encompassing demographics, travel details, and satisfaction levels. This dataset serves as a window into understanding the dynamics of the airline industry through data-driven insights.

        **Select aspects to explore** below and immerse yourself in the data!
        """
    )

    # User Choices for Exploration
    exploration_options = st.multiselect(
        "🔍 **Select aspects to explore:**",
        ["Passenger Demographics 👥", "Flight Details ✈️", "Customer Satisfaction 😊"],
    )

    if "Passenger Demographics 👥" in exploration_options:
        st.markdown("### Passenger Demographics 👥")

        # Gender Distribution
        st.markdown("**Gender Distribution**")
        gender_counts = df['Gender'].value_counts()
        fig_gender = px.pie(
            names=gender_counts.index,
            values=gender_counts.values,
            color_discrete_sequence=px.colors.sequential.RdBu,
            hole=0.4,
        )
        st.plotly_chart(fig_gender, use_container_width=True)

        # Dynamic Description for Gender Distribution
        total_gender = gender_counts.sum()
        male_percentage = (gender_counts.get('Male', 0) / total_gender) * 100
        female_percentage = (gender_counts.get('Female', 0) / total_gender) * 100

        if abs(male_percentage - female_percentage) < 5:
            gender_description = f"*The gender distribution is fairly balanced with **{male_percentage:.1f}% Male** and **{female_percentage:.1f}% Female** passengers.*"
        else:
            dominant_gender = 'Male' if male_percentage > female_percentage else 'Female'
            dominant_percentage = max(male_percentage, female_percentage)
            gender_description = f"*There is a noticeable imbalance in gender distribution, with **{dominant_percentage:.1f}% {dominant_gender}** passengers.*"

        st.markdown(gender_description)

        # Age Distribution
        st.markdown("**Age Distribution of Passengers**")
        fig_age = px.histogram(
            df,
            x='Age',
            nbins=30,
            color_discrete_sequence=['#FF7F50'],
            template='plotly_white',
        )
        st.plotly_chart(fig_age, use_container_width=True)

        # Dynamic Description for Age Distribution
        age_mean = df['Age'].mean()
        age_median = df['Age'].median()
        age_skew = skew(df['Age'])

        if age_skew > 0.5:
            age_skew_desc = "positively skewed (right-skewed)"
        elif age_skew < -0.5:
            age_skew_desc = "negatively skewed (left-skewed)"
        else:
            age_skew_desc = "approximately symmetrical"

        age_description = f"*The age distribution has a mean of **{age_mean:.1f} years**, a median of **{age_median:.1f} years**, and is **{age_skew_desc}**. This indicates that the passenger age range is diverse, primarily focusing on the working-age population.*"

        st.markdown(age_description)

    if "Flight Details ✈️" in exploration_options:
        st.markdown("### Flight Details ✈️")

        # Flight Class Distribution
        st.markdown("**Flight Class Distribution**")
        class_counts = df['Class'].value_counts()
        fig_class = px.bar(
            x=class_counts.index,
            y=class_counts.values,
            labels={'x': 'Class', 'y': 'Number of Passengers'},
            color=class_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        st.plotly_chart(fig_class, use_container_width=True)

        # Dynamic Description for Flight Class Distribution
        most_common_class = class_counts.idxmax()
        most_common_count = class_counts.max()
        most_common_percentage = (most_common_count / class_counts.sum()) * 100
        class_description = f"*The most common flight class is **{most_common_class}**, comprising **{most_common_percentage:.1f}%** of all passengers. This indicates a strong preference or availability in this class.*"
        st.markdown(class_description)

        # Flight Distance Distribution
        st.markdown("**Flight Distance Distribution**")
        fig_distance = px.histogram(
            df,
            x='Flight Distance',
            nbins=50,
            color_discrete_sequence=['#2E91E5'],
            template='plotly_white',
        )
        st.plotly_chart(fig_distance, use_container_width=True)

        # Dynamic Description for Flight Distance Distribution
        distance_mean = df['Flight Distance'].mean()
        distance_median = df['Flight Distance'].median()
        distance_skew = skew(df['Flight Distance'])

        if distance_skew > 0.5:
            distance_skew_desc = "positively skewed (right-skewed)"
        elif distance_skew < -0.5:
            distance_skew_desc = "negatively skewed (left-skewed)"
        else:
            distance_skew_desc = "approximately symmetrical"

        distance_description = f"*The flight distance distribution has a mean of **{distance_mean:.1f} km**, a median of **{distance_median:.1f} km**, and is **{distance_skew_desc}**. This suggests that the airline operates a mix of short-haul and long-haul flights.*"

        st.markdown(distance_description)

    if "Customer Satisfaction 😊" in exploration_options:
        st.markdown("### Customer Satisfaction 😊")

        # Satisfaction Counts
        st.markdown("**Customer Satisfaction Distribution**")
        satisfaction_counts = df['satisfaction'].value_counts()
        fig_satisfaction = px.pie(
            names=satisfaction_counts.index,
            values=satisfaction_counts.values,
            color_discrete_sequence=px.colors.sequential.Viridis,
            hole=0.3,
        )
        st.plotly_chart(fig_satisfaction, use_container_width=True)

        # Dynamic Description for Customer Satisfaction Distribution
        satisfied = satisfaction_counts.get('satisfied', 0)
        dissatisfied = satisfaction_counts.get('dissatisfied', 0)
        total_satisfaction = satisfied + dissatisfied
        satisfied_pct = (satisfied / total_satisfaction) * 100
        dissatisfied_pct = (dissatisfied / total_satisfaction) * 100

        satisfaction_description = f"***{satisfied_pct:.1f}%** of passengers are satisfied, while **{dissatisfied_pct:.1f}%** are dissatisfied. This highlights the overall satisfaction levels among the airline's customers.*"

        st.markdown(satisfaction_description)

        # Satisfaction by Class
        st.markdown("**Customer Satisfaction by Class**")
        fig_sat_class = px.histogram(
            df,
            x='Class',
            color='satisfaction',
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            template='presentation',
        )
        st.plotly_chart(fig_sat_class, use_container_width=True)

        # Dynamic Description for Satisfaction by Class
        sat_class = df.groupby('Class')['satisfaction'].value_counts(normalize=True).unstack().fillna(0)
        sat_class['satisfied_pct'] = sat_class.get('satisfied', 0) * 100
        sat_class_description = (
            f"*In **{sat_class.index[0]}** class, **{sat_class['satisfied_pct'].iloc[0]:.1f}%** passengers are satisfied.*\n"
            f"*In **{sat_class.index[1]}** class, **{sat_class['satisfied_pct'].iloc[1]:.1f}%** passengers are satisfied.*\n"
            f"*In **{sat_class.index[2]}** class, **{sat_class['satisfied_pct'].iloc[2]:.1f}%** passengers are satisfied.*"
        )
        st.markdown(sat_class_description)

elif selected_menu == "Unveil Insights":
    st.title("Unveil Insights 🔎")

    st.markdown(
        """
        Delve deeper into the data to uncover hidden patterns and relationships that drive customer satisfaction and operational efficiency.

        **Choose an insight to explore** below and discover the stories the data tells!
        """
    )

    # User Choices for Insights
    insights_options = st.selectbox(
        "🔍 **Select an insight to explore:**",
        [
            "Age vs. Flight Distance 📏",
            "Departure Delay vs. Arrival Delay ⏰",
            "Satisfaction Factors 🌟",
        ],
    )

    # Sample the data for certain plots
    sampled_df = df.sample(frac=0.005, random_state=42)

    if insights_options == "Age vs. Flight Distance 📏":
        # Scatter plot without internal title
        fig_age_distance = px.scatter(
            sampled_df,
            x='Age',
            y='Flight Distance',
            color='Type of Travel',
            size='Flight Distance',
            hover_data=['Class'],
            template='ggplot2',
        )
        st.plotly_chart(fig_age_distance, use_container_width=True)

        # Dynamic Description for Age vs Flight Distance
        correlation = sampled_df['Age'].corr(sampled_df['Flight Distance'])
        correlation_desc = "a strong positive" if correlation > 0.5 else "a moderate positive" if correlation > 0.3 else "a weak correlation"
        age_distance_description = (
            f"*There is **{correlation_desc} correlation ({correlation:.2f})** between age and flight distance. "
            f"This suggests that **younger passengers** tend to take **longer flights**, potentially indicating a preference for long-distance travel or business trips.*"
        )
        st.markdown(age_distance_description)

    elif insights_options == "Departure Delay vs. Arrival Delay ⏰":
        # Scatter plot with trendline without internal title
        fig_delay = px.scatter(
            sampled_df,
            x='Departure Delay in Minutes',
            y='Arrival Delay in Minutes',
            trendline='ols',
            color='satisfaction',
            template='seaborn',
        )
        st.plotly_chart(fig_delay, use_container_width=True)

        # Dynamic Description for Departure Delay vs Arrival Delay
        correlation = sampled_df['Departure Delay in Minutes'].corr(sampled_df['Arrival Delay in Minutes'])
        if correlation > 0.7:
            correlation_strength = "strong"
        elif correlation > 0.4:
            correlation_strength = "moderate"
        else:
            correlation_strength = "weak"
        delay_description = (
            f"*There is a **{correlation_strength} positive correlation ({correlation:.2f})** between departure delays and arrival delays. "
            f"This indicates that **departure delays** significantly influence **arrival delays**, emphasizing the need to address factors causing departure delays to improve overall punctuality.*"
        )
        st.markdown(delay_description)

    elif insights_options == "Satisfaction Factors 🌟":
        st.markdown("### Satisfaction Factors 🌟")

        # Satisfaction vs. Service Ratings
        service_columns = [
            'Seat comfort',
            'Food and drink',
            'Inflight wifi service',
            'Inflight entertainment',
            'Online support',
            'Ease of Online booking',
            'On-board service',
            'Leg room service',
            'Baggage handling',
            'Checkin service',
            'Cleanliness',
            'Online boarding',
        ]

        avg_ratings = df.groupby('satisfaction')[service_columns].mean().reset_index()
        melted_avg_ratings = avg_ratings.melt(id_vars='satisfaction', var_name='Service', value_name='Average Rating')

        fig_service = px.bar(
            melted_avg_ratings,
            x='Service',
            y='Average Rating',
            color='satisfaction',
            barmode='group',
            template='plotly_white',
        )
        st.plotly_chart(fig_service, use_container_width=True)

        # Dynamic Description for Satisfaction Factors
        satisfied_ratings = melted_avg_ratings[melted_avg_ratings['satisfaction'] == 'satisfied']
        dissatisfied_ratings = melted_avg_ratings[melted_avg_ratings['satisfaction'] == 'dissatisfied']

        top_services = satisfied_ratings.sort_values(by='Average Rating', ascending=False).head(3)['Service'].tolist()
        bottom_services = dissatisfied_ratings.sort_values(by='Average Rating').head(3)['Service'].tolist()

        satisfaction_description = (
            f"*Passengers who are satisfied generally give higher ratings across all service aspects. "
            f"The top contributing services to satisfaction are **{', '.join(top_services)}**. "
            f"Conversely, areas needing improvement include **{', '.join(bottom_services)}** to enhance overall customer satisfaction.*"
        )
        st.markdown(satisfaction_description)

elif selected_menu == "Our Journey":
    st.title("Conclusions and Recommendations 🚀")

    st.markdown(
        """
        ---
        **Key Insights**
        """
    )

    # Add emojis next to each key insight
    st.markdown(
        """
        - ✈️ **Passenger Demographics**: The airline serves a diverse age range, with younger passengers often taking longer flights.
        - 🛫 **Flight Operations**: A mix of short-haul, medium-haul, and some long-haul flights are operated, catering to various travel needs.
        - ⏰ **Delays**: Departure delays strongly affect arrival times, impacting customer satisfaction.
        """
    )

    st.markdown(
        """
        ---
        **Recommendations**
        """
    )

    # Add emojis next to each recommendation
    st.markdown(
        """
        1. 🛠️ **Minimize Delays**: Implement strategies to reduce departure delays, improving overall punctuality.
        2. 🌟 **Enhance Services**: Focus on service aspects that significantly influence satisfaction, such as in-flight entertainment and comfort.
        3. 🎯 **Targeted Marketing**: Develop campaigns aimed at younger travelers who are frequent long-haul passengers.
        4. 📈 **Optimize Operations**: Analyze flight routes and schedules to maximize efficiency and profitability.
        """
    )

    st.markdown(
        """
        ---
        **Thank you for being a part of this data journey! 🚀**
        """
    )

    # Closing Animation
    lottie_closing = load_lottieurl(closing_animation_url)
    if lottie_closing:
        st_lottie(lottie_closing, height=200, key="closing")
    else:
        st.error("Failed to load the closing animation.")