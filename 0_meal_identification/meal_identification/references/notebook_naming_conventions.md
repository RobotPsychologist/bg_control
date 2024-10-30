# Notebook Naming Conventions

Directly from the **Open a Notebook** section on:
https://cookiecutter-data-science.drivendata.org/using-the-template/


## Open a notebook
Now you're ready to do some analysis! Make sure that your project-specific environment is activated (you can check with which jupyter) and run jupyter notebook notebooks to open a Jupyter notebook in the notebooks/ folder. You can start by creating a new notebook and doing some exploratory data analysis. We often name notebooks with a scheme that looks like this:

`0.01-pjb-data-source-1.ipynb`

- `0.01`- Helps leep work in chronological order. The structure is PHASE.NOTEBOOK. NOTEBOOK is just the Nth notebook in that phase to be created. For phases of the project, we generally use a scheme like the following, but you are welcome to design your own conventions:
  - `0` - Data exploration - often just for exploratory work
  - `1` - Data cleaning and feature creation - often writes data to data/processed or data/interim
  - `2` - Visualizations - often writes publication-ready viz to reports
  - `3` - Modeling - training machine learning models
  - `4` - Publication - Notebooks that get turned directly into reports
- `pjb` - Your initials; this is helpful for knowing who created the notebook and prevents collisions from people working in the same notebook.
- `data-source-1` - A description of what the notebook covers

Now that you have your notebook going, start your analysis!
