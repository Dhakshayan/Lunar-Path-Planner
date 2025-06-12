import kagglehub

# Download latest version of the lunar surface dataset
path = kagglehub.dataset_download("filippopelosi/lunar-surface-dataset")
print("Dataset downloaded to:", path)
