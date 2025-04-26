""" OpenSearch setup """
from opensearch_client import OpenSearchClient
import settings

def setup_opensearch():
    client = OpenSearchClient()

    # Update ML-related cluster settings
    cluster_settings_filepath = (settings.OPENSEARCH_CONFIG_DIR / "cluster-settings.json").as_posix()
    cluster_settings = client._load_json_config(cluster_settings_filepath)
    client._update_cluster_settings(cluster_settings)

    # Register a model group
    model_group_id = client.register_model_group("Model group", "NLP model group")

    # Register a model to the model group
    model_id = client.register_model(settings.MODEL_URL, "1.0.1", "Model group")

    # # Deploy the model
    client.deploy_model(model_id)

    # Create an ingest pipeline
    client.create_ingest_pipeline(settings.PIPELINE_NAME, "NLP ingest pipeline", model_id)

