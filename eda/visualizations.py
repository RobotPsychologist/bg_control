'''Visualizations for the Gluroo dataset'''
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
import numpy as np


def andrew_y(df):
    df_pat1 = df[df['patient_id'] == 500030]
    df_pat2 = df[df['patient_id'] == 679372]

    # Subset the dataframe to separate bolus from basal insulin
    df_pat1_bolus = df_pat1[df_pat1['msg_type'] == 'DOSE_INSULIN'][['dose_units', 'bgl']]
    df_pat1_basal = df_pat1[df_pat1['msg_type'] == 'DOSE_BASAL_INSULIN'][['dose_units', 'bgl']]
    df_pat2_bolus = df_pat2[df_pat2['msg_type'] == 'DOSE_INSULIN'][['dose_units', 'bgl']]
    df_pat2_basal = df_pat2[df_pat2['msg_type'] == 'DOSE_BASAL_INSULIN'][['dose_units', 'bgl']]

    fig = plt.figure(figsize=(16, 9))
    gs = GridSpec(2, 2, figure=fig)

    # Plot 1: Impact of Food Glycemic Index on Glucose Levels for patient 500030
    ax1 = fig.add_subplot(gs[0, 0])
    sns.regplot(x='food_glycemic_index', y='bgl', data=df_pat1, ax=ax1, x_jitter=0.02, fit_reg=False)
    ax1.set_xlabel('Food Glycemic Index')
    ax1.set_ylabel('Blood Glucose Concentration (mg/dL)')
    ax1.set_title('Impact of Food Glycemic Index on Glucose Levels for Patient 500030')
    ax1.grid(True, which='major', linestyle='--', linewidth='0.5', color='black')

    # Plot 2: Impact of Food Glycemic Index on Glucose Levels for patient 679372
    ax2 = fig.add_subplot(gs[0, 1])
    sns.regplot(x='food_glycemic_index', y='bgl', data=df_pat2, x_jitter=0.02, ax=ax2, fit_reg=False)
    ax2.set_xlabel('Food Glycemic Index')
    ax2.set_ylabel('Blood Glucose Concentration (mg/dL)')
    ax2.set_title('Impact of Food Glycemic Index on Glucose Levels for Patient 679372')
    ax2.grid(True, which='major', linestyle='--', linewidth='0.5', color='black')

    # Set the same x and y limits for the top two plots
    x_max_gi = max(df_pat1['food_glycemic_index'].max(), df_pat2['food_glycemic_index'].max())

    ax1.set_xlim(0, x_max_gi)
    ax1.set_ylim(0, 250)
    ax2.set_xlim(0, x_max_gi)
    ax2.set_ylim(0, 250)

    # Plot 3: Effect of Insulin Doses on Glucose Trends (occupying two subplots)
    ax3 = fig.add_subplot(gs[1, 0])
    sns.scatterplot(x='dose_units', y='bgl', data=df_pat1_bolus, label='Patient 500030 Bolus', alpha=0.6, ax=ax3)
    sns.scatterplot(x='dose_units', y='bgl', data=df_pat1_basal, label='Patient 500030 Basal', alpha=0.6, ax=ax3)
    ax3.set_xlabel('Insulin Dose (units)')
    ax3.set_ylabel('Blood Glucose Concentration (mg/dL)')
    ax3.set_title('Effect of Insulin Doses on Glucose Trends')
    ax3.legend()
    ax3.grid(True, which='major', linestyle='--', linewidth='0.5', color='black')

    ax4 = fig.add_subplot(gs[1, 1])
    sns.scatterplot(x='dose_units', y='bgl', data=df_pat2_bolus, label='Patient 679372 Bolus', alpha=0.6, ax=ax4)
    sns.scatterplot(x='dose_units', y='bgl', data=df_pat2_basal, label='Patient 679372 Basal', alpha=0.6, ax=ax4)
    ax4.set_xlabel('Insulin Dose (units)')
    ax4.set_ylabel('Blood Glucose Concentration (mg/dL)')
    ax4.set_title('Effect of Insulin Doses on Glucose Trends')
    ax4.legend()
    ax4.grid(True, which='major', linestyle='--', linewidth='0.5', color='black')

    x_max_idose = max(df_pat1['dose_units'].max(), df_pat2['dose_units'].max())

    ax3.set_xlim(0, x_max_idose)
    ax3.set_ylim(0, 350)
    ax4.set_xlim(0, x_max_idose)
    ax4.set_ylim(0, 350)

    plt.tight_layout()
    plt.show()

    return None

def anton_r(df):
    all_food = df[(df["msg_type"] == "ANNOUNCE_MEAL")]["text"].str.cat(sep=' ').lower()
    foods = {
    'Cappuccino': 'healthy',
    'Eggs': 'healthy',
    'Toast': 'unhealthy',
    'Mandarin': 'healthy',
    'Wasa': 'healthy',
    'Nutella': 'unhealthy',
    'RX Bar': 'healthy',
    'Chick-fil-A salad': 'healthy',
    'Nuggets': 'unhealthy',
    'Chips': 'unhealthy',
    'Taffy': 'unhealthy',
    'Coffee creamer': 'unhealthy',
    'Sandwich': 'unhealthy',
    'Chocolate': 'unhealthy',
    'Ice cream': 'unhealthy',
    'Bar': 'unhealthy',
    'Crackers': 'unhealthy',
    'Burrito': 'unhealthy',
    'Quiche': 'unhealthy',
    'Pastries': 'unhealthy',
    'Gyro bowl': 'unhealthy',
    'Basmati rice': 'healthy',
    'Graham crackers': 'unhealthy',
    'Salad': 'healthy',
    'Beer': 'unhealthy',
    'Mac n cheese': 'unhealthy',
    'Breakfast burrito': 'unhealthy',
    'Cafe au lait': 'healthy',
    'Bread': 'unhealthy',
    'Soup': 'healthy',
    'Omelette': 'healthy',
    'Strawberries': 'healthy',
    'Latte': 'healthy',
    'Taco Bell': 'unhealthy',
    'Salmon': 'healthy',
    'Pineapple': 'healthy',
    'Waffle': 'unhealthy',
    'Blueberries': 'healthy',
    'M&Ms': 'unhealthy',
    'Trail mix': 'healthy',
    'Sweet potato fries': 'healthy',
    'Yogurt bowl': 'healthy',
    'Berries': 'healthy',
    'Walnuts': 'healthy',
    'Chicken tenders': 'unhealthy',
    'Broccoli': 'healthy',
    'Pie': 'unhealthy',
    'Pastry': 'unhealthy',
    'Mochas': 'healthy',
    'Guacamole': 'healthy',
    'Beef': 'healthy',
    'Rice': 'unhealthy',
    'Pad Thai': 'unhealthy',
    'Taco': 'unhealthy',
    'Popcorn': 'unhealthy',
    'Meatballs': 'healthy',
    'Pizza': 'unhealthy',
    'Caesar salad': 'healthy',
    'Chicken biscuit': 'unhealthy',
    'English muffin': 'unhealthy',
    'Ham': 'unhealthy',
    'Pancake': 'unhealthy',
    'Coconut cream pie': 'unhealthy',
    'Gelato': 'unhealthy',
    'French fries': 'unhealthy',
    'Risotto': 'unhealthy',
    'Fajitas': 'unhealthy',
    'Cookies': 'unhealthy',
    'Brownie': 'unhealthy',
    'Ribs': 'unhealthy',
    'Sausage': 'unhealthy',
    'Avocado': 'healthy',
    'Frittata': 'healthy',
    'Corn tortilla': 'healthy',
    'Samosa': 'unhealthy',
    'Quesadilla': 'unhealthy',
    'Chicken shawarma': 'unhealthy',
    'Granola': 'healthy',
    'Macadamia nuts': 'healthy',
    'Beef Gozleme': 'unhealthy',
    'Coconut curry soup': 'healthy',
    'Fried chicken': 'unhealthy',
    'Tacos': 'unhealthy',
    'Sushi': 'healthy',
    'Almond butter': 'healthy',
    'Pita': 'unhealthy',
    'Chocolate mousse': 'unhealthy'
    }

    foods = pd.DataFrame(list(foods.items()), columns=['Food', 'Health_Status']) #convert dictionary above into df

    foods["Food"] = foods["Food"].apply(lambda x: x.lower()) #and lowercase everything

    def food_freq(df, foods):
        loc_foods = foods.copy() #not the cleanest way to go around the problem of passing data by reference, but it works
        all_food = df[(df["msg_type"] == "ANNOUNCE_MEAL")]["text"].str.cat(sep=' ').lower()

        loc_foods["Count"] = 0

        for iter, i in enumerate(loc_foods["Food"]): #count the number of times each food appears in the patient data
            loc_foods.loc[iter, "Count"] = all_food.count(i)

        return loc_foods

    df_pat1_foods = food_freq(df[df['patient_id']==500030], foods)
    df_pat2_foods = food_freq(df[df['patient_id']==679372], foods)
    patient_ids = ['500030', '679372']

    def graph_foods(PWD, patient_ids=patient_ids):
        fig = plt.figure(figsize=(16, 9))
        gs = GridSpec(2, 2, figure=fig)
        sns.despine(fig)

        ax1 = fig.add_subplot(gs[0, 0])
        ax1.grid(True, which='major', linestyle='--', linewidth='0.5', color='black')
        top_10_pwd_0 = PWD[0].iloc[PWD[0]['Count'].nlargest(n=10).index]
        sns.barplot(ax=ax1, x=top_10_pwd_0["Food"], y=top_10_pwd_0["Count"], hue=top_10_pwd_0["Health_Status"])
        ax1.tick_params(axis='x', labelrotation=60)
        ax1.set_xlabel("")
        ax1.set_ylabel("Food Consumption Count")
        ax1.set_title(f"Patient #{patient_ids[0]}")

        ax2 = fig.add_subplot(gs[0, 1])
        ax2.grid(True, which='major', linestyle='--', linewidth='0.5', color='black')
        top_10_pwd_1 = PWD[1].iloc[PWD[1]['Count'].nlargest(n=10).index]
        sns.barplot(ax = ax2, x = top_10_pwd_1["Food"], y = top_10_pwd_1["Count"], hue = top_10_pwd_1["Health_Status"])
        ax2.tick_params(axis='x', labelrotation=60)
        ax2.set_xlabel("")
        ax2.set_ylabel("Food Consumption Count")
        ax2.set_title(f"Patient #{patient_ids[1]}")

        ax3 = fig.add_subplot(gs[1, :])
        ax3.grid(True, which='major', linestyle='--', linewidth='0.5', color='black')
        ax3.set_ylabel("Percent Healthy Food")
        health_summary_pwd_0 = PWD[0].groupby(by = "Health_Status")["Count"].sum().reset_index()
        health_summary_pwd_0["Patient"] = patient_ids[0]
        health_summary_pwd_1 = PWD[1].groupby(by = "Health_Status")["Count"].sum().reset_index()
        health_summary_pwd_1["Patient"] = patient_ids[1]
        health_summary = pd.concat([health_summary_pwd_0, health_summary_pwd_1])
        total = health_summary.groupby('Patient')['Count'].sum().reset_index()
        unhealthy = health_summary[health_summary.Health_Status == "unhealthy"].groupby('Patient')["Count"].sum().reset_index()

        unhealthy['Count'] = [i / j * 100 for i,j in zip(unhealthy['Count'], total['Count'])]
        total['Count'] = [i / j * 100 for i,j in zip(total['Count'], total['Count'])]

        # bar chart 1 -> top bars (group of 'smoker=No')
        bar1 = sns.barplot(x="Patient",  y="Count", data=total, color='#1f77b4')

        # bar chart 2 -> bottom bars (group of 'smoker=Yes')
        bar2 = sns.barplot(x="Patient", y="Count", data=unhealthy, color='darkorange')

        # add legend
        top_bar = mpatches.Patch(color='#1f77b4', label='Unhealthy = No')
        bottom_bar = mpatches.Patch(color='darkorange', label='Unhealthy = Yes')
        plt.legend(handles=[top_bar, bottom_bar])

        # show the graph
        plt.tight_layout()
        plt.show()

    graph_foods([df_pat1_foods, df_pat2_foods])
    return None

def gavin_k(df):
    df['date_original'] = pd.to_datetime(df['date_original'], errors='coerce')
    df['hour'] = df['date_original'].dt.hour
    df['day_of_week'] = df['date_original'].dt.dayofweek
    df['week'] = df['date_original'].dt.isocalendar().week
    df['day'] = df['date_original'].dt.date

    # Remove rows with NaN or invalid blood glucose levels (i.e. negative or NaN values in bgl)
    df_clean = df.dropna(subset=['bgl']).loc[df['bgl'] > 0].copy()

    # Drop any irrelevant columns
    columns_to_drop = ['sender_id', 'bgl_date_millis', 'text', 'template', 'msg_type',
                    'affects_fob', 'affects_iob', 'dose_units', 'food_g', 'food_glycemic_index',
                    'dose_automatic', 'fp_bgl', 'message_basal_change', '__typename', 'trend']

    df_clean.drop(columns=columns_to_drop, inplace=True)
    df = df_clean
    # Plot 1: Heatmap of Blood Glucose by Hour and Day of the Week
    plt.figure(figsize=(12, 8))
    heatmap_data = df.pivot_table(index='hour', columns='day_of_week', values='bgl', aggfunc='median')
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='.1f', linewidths=.5)
    plt.title('Hourly Glucose Heatmap')
    plt.xlabel('Day of the Week (0=Monday, 6=Sunday)')
    plt.ylabel('Hour of the Day')
    plt.show()

    # Plot 2: Boxplot of Blood Glucose Levels by Hour
    plt.figure(figsize=(14, 8))
    plt.boxplot([df[df['hour'] == hour]['bgl'] for hour in range(24)], positions=range(24))
    plt.title('Boxplot of Blood Glucose Levels by Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Blood Glucose Level (mg/dL)')
    plt.grid(True)
    plt.axhline(y=180, color='red', linestyle='--', label='Hyperglycemia Threshold')
    plt.axhline(y=70, color='green', linestyle='--', label='Hypoglycemia Threshold')
    plt.legend()
    plt.show()

    # Plot 3: Blood Glucose Distribution with KDE
    plt.figure(figsize=(12, 8))
    sns.histplot(df['bgl'], kde=True, bins=30, color='skyblue', edgecolor='black')
    plt.title('Blood Glucose Distribution with KDE')
    plt.xlabel('Blood Glucose Level (mg/dL)')
    plt.ylabel('Density')
    plt.grid(True)
    plt.axvline(x=180, color='red', linestyle='--', label='Hyperglycemia Threshold')
    plt.axvline(x=70, color='green', linestyle='--', label='Hypoglycemia Threshold')
    plt.legend()
    plt.show()

    return None


def jonathan_g(df, user_id):
    plt.figure(figsize=(16,9))
    df_cleaned = df.dropna(subset=df.iloc[:, 2:17].columns, how='all')
    user_ids = [user_id] # can add more patients to the list such as [500030, 679372]

    # can replace user_ids with this when wanting to visualize all patients df_cleaned['user_id'].unique()
    for patient_id in user_ids:

        # Filter data for each patient
        patient_data = df_cleaned[df_cleaned['user_id'] == patient_id].copy()
        patient_data = patient_data.sort_values(by='date')

        # Patients data on a time interval
        patient_data = patient_data.iloc[150:500]

        # Plot the patient's data
        plt.plot(patient_data['date'], patient_data['bgl'], label=f'Patient {patient_id}')

        # Compute the derivative (rate of change) of BGL levels
        patient_data['BGL_Derivative'] = patient_data['bgl'].diff().fillna(0)

        # Plot the derivative
        plt.plot(patient_data['date'], patient_data['BGL_Derivative'], '--', label=f'BG" Derivative - Patient {patient_id}')

    plt.xlabel('Date')
    plt.ylabel('BGL Level and their derivative')
    plt.title('BGL Levels Over Time by Patient and the derivative of BGL levels')
    plt.legend()

    plt.show()
    return None

def julia_z():
    return None

def junwon_p():
    return None

def rebecca_m():
    return None

def safiya_m():
    return None

def sneha_s():
    return None

def tony_c():
    return None

def vilohith_r():
    return None

def yimeng_x():
    return None
