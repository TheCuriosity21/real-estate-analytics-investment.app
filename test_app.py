import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Streamlit Test App",
    page_icon="🧪",
    layout="wide"
)

# Add title and introduction
st.title("Simple Streamlit Test Application")
st.header("This is a basic demo app with no external dependencies")

# Add some explanatory text
st.write("""
This is a simple Streamlit application that demonstrates the basic functionality of Streamlit.
If you can see this, your Streamlit deployment is working correctly!
""")

# Create some interactive elements
st.subheader("Interactive Elements")

# Sidebar with options
with st.sidebar:
    st.write("## Options")
    name = st.text_input("Enter your name:", "Guest")
    age = st.slider("Select your age:", 1, 100, 25)
    favorite_color = st.selectbox(
        "Choose your favorite color:",
        ["Red", "Blue", "Green", "Yellow", "Purple"]
    )

# Main content
st.write(f"Hello, **{name}**! You are {age} years old and your favorite color is {favorite_color}.")

# Create columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Visualization Example")
    chart_data = {
        "Category": ["A", "B", "C", "D"],
        "Values": [10, 25, 15, 30]
    }
    st.bar_chart(chart_data)

with col2:
    st.subheader("Interactive Button")
    if st.button("Click me!"):
        st.success("Button was clicked!")
        st.balloons()
    else:
        st.info("Click the button to see what happens")

# Add a final note
st.markdown("---")
st.write("This simple test app confirms that your Streamlit deployment is working correctly.")
st.info("You can now build more complex applications using Streamlit!")

