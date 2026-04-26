import numpy as np
import pandas as pd

def gerar_churn(n_samples: int = 2000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    churn = rng.integers(0, 2, size=n_samples)

    dias_sem_login    = np.where(churn, rng.integers(30, 180, n_samples),
                                        rng.integers(1, 30, n_samples))
    num_chamados      = np.where(churn, rng.integers(3, 15, n_samples),
                                        rng.integers(0, 4, n_samples))
    valor_mensalidade = rng.uniform(50, 500, n_samples).round(2)
    meses_contrato    = np.where(churn, rng.integers(1, 12, n_samples),
                                        rng.integers(6, 60, n_samples))
    nps_score         = np.where(churn, rng.integers(0, 6, n_samples),
                                        rng.integers(5, 11, n_samples))

    return pd.DataFrame({
        "dias_sem_login":    dias_sem_login,
        "num_chamados":      num_chamados,
        "valor_mensalidade": valor_mensalidade,
        "meses_contrato":    meses_contrato,
        "nps_score":         nps_score,
        "churn":             churn
    })

if __name__ == "__main__":
    df = gerar_churn()
    print(df.head())
    print(f"\nDistribuição do target:\n{df['churn'].value_counts()}")
    df.to_csv("churn_dataset.csv", index=False)
    print("\nDataset salvo em churn_dataset.csv")