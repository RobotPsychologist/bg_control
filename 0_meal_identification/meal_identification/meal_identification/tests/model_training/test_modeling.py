    Sample training:
    logger.info("Training some model...")

    data_filename = "2024-11-15_500030__i5mins_d4hrs_c5g_l2hrs_n3.csv"
    data_path = INTERIM_DATA_DIR / data_filename
    current_model_path = MODELS_DIR / "model.pkl"

    train_model_instance(
        model = "GMMHMM", 
        data_path=data_path,    
        model_path=current_model_path,  
        transformer=ScaledLogitTransformer())
    logger.success("Modeling training complete.")
