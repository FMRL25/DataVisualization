import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Title of the app
st.title("Data Visualization App")

# Section Selector
st.sidebar.header("Select Visualization Type")
visualization_type = st.sidebar.selectbox("Choose a chart type:", ["Before and After Stacked Bar", "Date Progression Line Chart"])

if visualization_type == "Before and After Stacked Bar":
    # Input Section for Stacked Bar
    st.header("Input Data for Stacked Bar Chart")

    # Input the 'before' value
    before = st.number_input("Enter the 'before' value", min_value=0.0, value=0.0, step=1.0)

    # Input the 'after' values
    after = st.text_area(
        "Enter the 'after' values (comma-separated)",
        "1, 2, 3"
    )

    # Input legend names for the 'after' segments
    after_legend_names = st.text_area(
        "Enter the legend names for 'after' segments (comma-separated, must match number of 'after' values)",
        "Segment 1, Segment 2, Segment 3"
    )

    # Input legend name for the 'before' segment
    before_legend_name = st.text_input("Enter the legend name for 'Before' segment", "Before Grading")
    after_legend_name = st.text_input("Enter the legend name for 'After' segment", "After Grading")

    # Predefined color options
    color_options = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "yellow", "cyan"]

    # Input color for the 'before' column
    before_color = st.selectbox("Select the color for the 'Before' column", color_options)

    # Select colors for each segment dynamically based on the number of segments
    try:
        # Replace commas with periods for decimal values
        after_values = list(map(lambda x: float(x.replace(",", ".")), after.split(",")))
        after_legend_labels = after_legend_names.split(",")

        if len(after_values) != len(after_legend_labels):
            raise ValueError("The number of 'after' values and legend names must match.")

        # Select colors for 'after' segments
        colors = []
        st.subheader("Select Colors for 'After' Segments")
        for i in range(len(after_values)):
            color = st.selectbox(f"Select color for {after_legend_labels[i].strip()}:", color_options, index=i % len(color_options))
            colors.append(color)

        # Extend color options if more segments are provided than predefined colors
        while len(colors) < len(after_values):
            colors.append(color_options[len(colors) % len(color_options)])

    except ValueError as e:
        st.error(f"Input Error: {e}")
        after_values = []

    # Input chart title
    title = st.text_input("Enter the chart title", "Before vs After Stacked Bar Chart")

    # Input axis titles
    x_axis_title = st.text_input("Enter the X-axis title", "Category")
    y_axis_title = st.text_input("Enter the Y-axis title", "Values")

    # Displaying the Stacked Bar Chart
    if before >= 0 and after_values:
        st.header("Stacked Bar Chart")

        # Prepare the data
        categories = [before_legend_name, after_legend_name]

        # Plot the data
        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot the 'before' bar with selected color
        bar_before = ax.bar(categories[0], before, color=before_color, label=before_legend_name)

        # Add data label for 'before' bar
        for bar in bar_before:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, height / 2, f"{int(height)}", ha="center", va="center", color="white", fontsize=10, fontweight="bold")

        # Plot the 'after' bar with stacked segments
        bottom = 0  # Initialize the bottom position for stacking
        for i, value in enumerate(after_values):
            bar_after = ax.bar(categories[1], value, bottom=bottom, color=colors[i].strip(), label=after_legend_labels[i].strip())

            # Add data label for each segment in 'after' bar
            for bar in bar_after:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2.0, bottom + height / 2, f"{int(height)}", ha="center", va="center", color="black", fontsize=10, fontweight="bold")

            bottom += value

        # Add labels
        ax.set_xlabel(x_axis_title, fontsize=12)
        ax.set_ylabel(y_axis_title, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")

        # Calculate and display percentage increase
        if before > 0:
            percent_increase = ((sum(after_values) - before) / before) * 100
            st.write(f"Percentage Increase: {percent_increase:.2f}%")

        # Adjust legend placement and styling
        ax.legend(
            loc="lower center",
            fontsize=10,
            frameon=False,
            ncol=2,  # Dynamically adjust the number of columns
            bbox_to_anchor=(0.5, -0.25)  # Add more distance from the graph
        )

        # Customize gridlines and aesthetics
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        # Display the chart
        st.pyplot(fig)
    else:
        st.warning("Please provide valid input for both 'before' and 'after' values.")

elif visualization_type == "Date Progression Line Chart":
    # Input Section for Line Chart
    st.header("Input Data for Line Chart")

    # Input multiple lines of data
    st.write("Enter data for multiple lines, each in the format: DD-MM-YYYY <space> value, with two empty lines between each new line.")

    # Example Input format: "01-01-2023 <space> 10.56\n01-02-2023 <space> 15.85\n\n\n01-01-2023 <space> 12.58\n01-02-2023 <space> 18.47"
    data_input = st.text_area(
        "Enter the data",
        "01-01-2023 10.56\n01-02-2023 15.85\n\n\n01-01-2023 12.58\n01-02-2023 18.47"
    )

    # Input legend names for each line
    line_legend_names = st.text_area(
        "Enter the legend names for each line (comma-separated, must match number of lines)",
        "Line 1, Line 2"
    )

    # Input line colors
    color_options = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "yellow", "cyan"]
    st.subheader("Select Colors for Each Line")
    line_colors = []
    for i in range(10):
        color = st.selectbox(f"Select color for Line {i+1}", color_options, index=i % len(color_options))
        line_colors.append(color)

    # Input chart title and axis titles
    title = st.text_input("Enter the chart title", "Date Progression Line Chart")
    x_axis_title = st.text_input("Enter the X-axis title", "Date")
    y_axis_title = st.text_input("Enter the Y-axis title", "Value")

    # Parse the input data
    try:
        # Split the input into lines and identify separate line series
        series_data = data_input.split("\n\n\n")  # Split into series by two empty lines

        all_series_data = []
        for data_line in series_data:
            # Split lines by space, ensure there's a valid date and value
            data = [line.split(" ") for line in data_line.splitlines() if len(line.split(" ")) == 2]

            if not data:
                raise ValueError("Data is missing or not formatted correctly. Each line must have 'DD-MM-YYYY <space> value' format.")

            df = pd.DataFrame(data, columns=["Date", "Value"])
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")

            # Replace commas with periods for decimal values in the 'Value' column
            df["Value"] = df["Value"].str.replace(",", ".").astype(float)

            df.dropna(inplace=True)
            all_series_data.append(df)

        if len(all_series_data) == 0:
            raise ValueError("No valid data was entered.")
    except Exception as e:
        st.error(f"Error parsing data: {e}")
        all_series_data = []

    # Display the Line Chart
    if all_series_data:
        st.header("Line Chart")

        # Plot the data
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot each line
        for i, df in enumerate(all_series_data):
            ax.plot(df["Date"], df["Value"], marker="o", linestyle="-", color=line_colors[i % len(line_colors)], label=line_legend_names.split(",")[i])

        # Add labels and title
        ax.set_xlabel(x_axis_title, fontsize=12)
        ax.set_ylabel(y_axis_title, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")

        # Display the chart
        st.pyplot(fig)
