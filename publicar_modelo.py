import os
import joblib
from huggingface_hub import HfApi, login

token = os.environ.get("HF_TOKEN")
login(token=token)

api = HfApi()

repo_id = "becamparezzo/churn-model"

api.create_repo(repo_id=repo_id, exist_ok=True)

api.upload_file(
    path_or_fileobj="model.pkl",
    path_in_repo="model.pkl",
    repo_id=repo_id,
)

api.upload_file(
    path_or_fileobj="requirements.txt",
    path_in_repo="requirements.txt",
    repo_id=repo_id,
)

print(f"Modelo publicado em: https://huggingface.co/{repo_id}")