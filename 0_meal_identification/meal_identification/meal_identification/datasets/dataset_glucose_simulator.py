import pandas as pd
import os
from simglucose.simulation.user_interface import simulate
from simglucose.simulation.scenario import CustomScenario
from simglucose.simulation.scenario_gen import RandomScenario
from simglucose.controller.basal_bolus_ctrller import BBController
from dataset_operations import get_root_dir
from datetime import datetime, timedelta


def process_simulated_data(df):
    """
    Process individual patient's glucose data into project-specific format.

    Parameters
    ----------
    df (pd.DataFrame): Input DataFrame with simulation data

    Returns
    -------
    pd.DataFrame: Processed DataFrame with project-specific format
    """
    # Create a copy to avoid modifying the original
    processed_df = df.copy()

    # Create two separate dataframes for BG and CGM readings
    processed_df = processed_df[['Time', 'BG', 'CGM', 'CHO']].copy()

    # Add required columns
    processed_df['msg_type'] = ''
    processed_df['food_glycemic_index'] = ''
    processed_df['affects_iob'] = ''
    processed_df['affects_fob'] = ''
    processed_df['dose_units'] = ''

    # Map CGM to bgl column, Time to date and BG to bgl_real for reference only
    processed_df = processed_df.rename(columns={'CGM': 'bgl', 'BG': 'bgl_real', 'Time': 'date'})

    processed_df.loc[processed_df['CHO'] > 0, 'msg_type'] = 'ANNOUNCE_MEAL'

    # Rename CHO to food_g where it's > 0
    processed_df.loc[processed_df['CHO'] > 0, 'food_g'] = processed_df.loc[processed_df['CHO'] > 0, 'CHO']

    # Drop the CHO column
    processed_df = processed_df.drop(columns=['CHO'])


    return processed_df


def run_glucose_simulation(
        start_time=None,
        simulation_days=7,
        scenario_type='random',
        custom_meal_schedule=None,
        patient_names=None,
        cgm_name="Dexcom",
        insulin_pump_name="Cozmo",
        global_seed=123,
        animate=False,
        parallel=True,
):
    # Set default values
    if start_time is None:
        start_time = pd.Timestamp('2024-01-01 00:00:00')
    if patient_names is None:
        patient_names = ['adult#001']
    if custom_meal_schedule is None and scenario_type == 'custom':
        custom_meal_schedule = [(1, 20)]  # Default meal at hour 1 with 20g carbs

    # Create controller
    controller = BBController()

    # Set up simulation time
    sim_time = pd.Timedelta(days=simulation_days)

    # Scenario
    if scenario_type == 'custom':
        scenario = CustomScenario(
            start_time=start_time,
            scenario=custom_meal_schedule
        )
    else:
        scenario = RandomScenario(
            start_time=start_time,
            seed=global_seed
        )

    # Set up result directory
    project_root = get_root_dir()
    result_dir = os.path.join(project_root, '0_meal_identification', 'meal_identification', 'data', 'sim')
    os.makedirs(result_dir, exist_ok=True)

    # Run simulation
    simulate(
        sim_time=sim_time,
        scenario=scenario,
        controller=controller,
        start_time=start_time,
        save_path=result_dir,
        cgm_name=cgm_name,
        cgm_seed=global_seed,
        insulin_pump_name=insulin_pump_name,
        animate=animate,
        parallel=parallel,
        patient_names=patient_names,
    )

    return result_dir


def process_sim_data(simulation_days):
    """
    Process all patient CSV files in the sim directory and output them to data/raw.

    Returns:
    dict: Dictionary with patient IDs as keys and processed DataFrames as values
    """
    # Get the project root and construct sim directory path
    project_root = get_root_dir()
    sim_dir = os.path.join(project_root, '0_meal_identification', 'meal_identification', 'data', 'sim')
    processed_dir = os.path.join(project_root, '0_meal_identification', 'meal_identification', 'data', 'raw')

    # Convert to Path object for easier handling
    csv_files = [f for f in os.listdir(sim_dir) if f.endswith('.csv')]

    # Dictionary to store processed data for each patient
    processed_data = {}

    for file in csv_files:
        # Skip CVGA_stats.csv and risk_trace.csv
        if ('CVGA' in file) or ('risk_trace' in file) or ('performance' in file):
            continue

        file_path = os.path.join(sim_dir, file)
        try:
            df = pd.read_csv(file_path)

            # Convert Time column to datetime
            df['date'] = pd.to_datetime(df['Time'])

            # Process the data
            processed_df = process_simulated_data(df)

            # Create new filename (first 3 + last 3 characters before .csv)
            base_name = file.replace('.csv', '')
            short_name = f"{base_name[:3]}{base_name[-3:]}"
            timestamp = datetime.today()
            to = timestamp + timedelta(days=simulation_days)
            start_date = timestamp.strftime('%Y-%m-%d')
            end_date = to.strftime('%Y-%m-%d')
            file = f"{short_name}_{start_date}_{end_date}.csv"

            # Store in dictionary
            processed_data[file] = processed_df

            print(f"Successfully processed {file}")

        except Exception as e:
            print(f"Error processing {file}: {str(e)}")

    # Save processed data
    os.makedirs(processed_dir, exist_ok=True)
    for file, df in processed_data.items():
        output_file = os.path.join(processed_dir, file)
        df.to_csv(output_file)
        print(f"Saved processed data for {file}")

    return processed_data


def generate_simulated_data(
        start_time=None,
        simulation_days=7,
        scenario_type='random',
        custom_meal_schedule=None,
        patient_names=None,
        cgm_name="Dexcom",
        insulin_pump_name="Cozmo",
        global_seed=123,
        animate=False,
        parallel=True,
):
    """
    Run a glucose simulation with specified parameters and output to data/raw.
    Animate and parallel can not be set to True at the same time for Mac. Not sure about Windows and Linux
    General data flow: Sim -> Raw

    Parameters
    ----------
    start_time (pd.Timestamp, optional): Start time for simulation. Defaults to '2024-01-01 00:00:00'.
    simulation_days (int, optional): Duration of simulation in days. Defaults to 7.
    scenario_type (str, optional): Type of scenario
         - 'random' | 'custom'. Defaults to 'random'.
    custom_meal_schedule (list, optional): List of tuples (hour, carbs) for custom scenario.
    patient_names (list, optional): List of patient IDs to simulate. Each patient's data will look different.
    cgm_name (str, optional): Name of the cgm device.
         - "Dexcom" | "GuardianRT" | "Navigator". Defaults to "Dexcom".
    insulin_pump_name (str, optional): Name of the insulin pump device.
         - "Cozmo" | "Insulet". Defaults to "Cozmo".
    global_seed (int, optional): Random seed for reproducibility. Defaults to 123.
    animate (bool, optional): Whether to animate the simulation. Defaults to False.
    parallel (bool, optional): Whether to run simulations in parallel. Defaults to True.
    patient_names (list, optional): List of patient IDs to simulate.
         - patient_names can be from adult#001 ~ adult#009 and child#001 ~ child#009. Default to ["adult#001"].

    Returns
    -------
    str: Path to the directory containing simulation results.
    """
    run_glucose_simulation(
        start_time=start_time,
        simulation_days=simulation_days,
        scenario_type=scenario_type,
        custom_meal_schedule=custom_meal_schedule,
        patient_names=patient_names,
        cgm_name=cgm_name,
        insulin_pump_name=insulin_pump_name,
        global_seed=global_seed,
        animate=animate,
        parallel=parallel,
    )
    process_sim_data(simulation_days=simulation_days)


default_patient_names = ['adult#001', 'adult#003']
generate_simulated_data(
    patient_names=default_patient_names
)
