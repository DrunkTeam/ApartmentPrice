from datetime import timedelta
from feast import Entity, Feature, FeatureView, FileSource, ValueType

# Define an entity for the feature
customer = Entity(
    name="customer_id",
    value_type=ValueType.INT64,
    description="customer id",
)

# Define a source for the features
file_source = FileSource(
    path="data/features.parquet",
    timestamp_field="timestamp",
)

# Define the features
feature_view = FeatureView(
    name="customer_features",
    entities=["customer_id"],
    ttl=timedelta(days=1),
    batch_source=file_source,
    features=[
        Feature(name="feature_1", dtype=ValueType.FLOAT),
        Feature(name="feature_2", dtype=ValueType.INT64),
    ],
)

# Apply the changes
feast apply
