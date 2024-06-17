import great_expectations as gx

context = gx.get_context(project_root_dir = "services")

retrieved_checkpoint = context.get_checkpoint(name="initial_data_validation_checkpoint")

results = retrieved_checkpoint.run()

assert results.success