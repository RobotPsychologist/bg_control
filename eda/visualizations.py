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

def gavin_k():

    return None


def jonathan_g():
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
