import hydra
import dvc.api
import pandas as pd

@hydra.main(config_path="../config", config_name = "name", version_base=None)
def app(cfg = None):
    url = dvc.api.get_url(
        path=cfg.data.path,
        remote = cfg.data.remote,
        repo = cfg.data.repo,
        rev = cfg.data.version
    )
    df = pd.read_csv(url)
    print(df.head())

if __name__ == "__main__":
    app()