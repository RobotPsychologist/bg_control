import matplotlib.pyplot as plt

def plot_announce_meal_histogram(df, hours_or_15minutes='hours'):
    """
    Plot a histogram of the intervals of the day where 'ANNOUNCE_MEAL' occurs.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame with columns 'msg_type' and a datetime index.
    hours_or_15minutes : str, optional
        Whether to plot by 'hours' or 'minutes' (15-minute intervals).

    Returns
    -------
    None
    """
    # Filter the DataFrame to include only 'ANNOUNCE_MEAL' events
    announce_meal_df = df[df['msg_type'] == 'ANNOUNCE_MEAL']

    if announce_meal_df.empty:
        print("No 'ANNOUNCE_MEAL' events found.")
        return

    # Extract the hour and minute from the timestamp
    announce_meal_hours = announce_meal_df['date'].dt.hour
    announce_meal_minutes = announce_meal_df['date'].dt.minute

    if hours_or_15minutes == 'minutes':
        # Convert to fractional hours for 15-minute intervals
        announce_meal_fractional_hours = announce_meal_hours + announce_meal_minutes / 60.0

        # Plot histogram with 15-minute intervals (96 bins for 24 hours)
        plt.figure(figsize=(10, 6))
        plt.hist(announce_meal_fractional_hours, bins=96, range=(0, 24), edgecolor='black')
        plt.xlabel('Minute of the Day (15-minute intervals)')
        plt.ylabel('Count')
        plt.title('Histogram of 15-Minute Intervals Where ANNOUNCE_MEAL Occurs')
        plt.xticks(ticks=[i/4 for i in range(0, 24*4+1, 4)], labels=[f"{i}:00" for i in range(0, 25, 1)], rotation=90)
    elif hours_or_15minutes == 'hours':
        # Plot histogram by hours
        plt.figure(figsize=(10, 6))
        plt.hist(announce_meal_hours, bins=24, range=(0, 24), edgecolor='black')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Count')
        plt.title('Histogram of Hours Where ANNOUNCE_MEAL Occurs')
        plt.xticks(range(0, 25, 1))
    else:
        raise ValueError("Invalid value for hours_or_15minutes. Choose 'hours' or 'minutes'.")

    plt.grid(True)
    plt.tight_layout()
    plt.show()
