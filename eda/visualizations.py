'''Visualizations for the Gluroo dataset'''
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
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

def anton_r():
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
