import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)

def soft_threshold(lambd, x):
    """Soft-thresholding function"""
    return np.sign(x) * np.maximum(np.abs(x) - lambd, 0)

def centralize_and_standardize(X, y):
    n, p = X.shape
    X = X.copy().astype(float)
    y = y.copy().astype(float)

    X_bar = np.mean(X, axis=0)          # column means
    X_centered = X - X_bar
    X_sd = np.std(X_centered, axis=0, ddof=1)
    X_scaled = X_centered / X_sd

    y_bar = np.mean(y)
    y_centered = y - y_bar

    return X_scaled, y_centered, X_bar, X_sd, y_bar

def linear_lasso(X, y, lambd=0.0, max_iter=1000, tol=0.001):
    n, p = X.shape
    X_scaled, y_centered, X_bar, X_sd, y_bar = centralize_and_standardize(X, y)

    beta = np.zeros(p)

    for _ in range(max_iter):
        beta_old = beta.copy()
        for j in range(p):
            r = y_centered - X_scaled @ beta + X_scaled[:, j] * beta[j]
            sj = np.dot(X_scaled[:, j], r) / n
            denom = np.dot(X_scaled[:, j], X_scaled[:, j]) / n
            beta[j] = soft_threshold(lambd, sj) / denom

        if np.max(np.abs(beta - beta_old)) < tol:
            break

    # Restore to original scale
    beta_restored = beta / X_sd
    beta_0 = y_bar - np.dot(X_bar, beta_restored)
    return beta_restored, beta_0

n, d = 500, 6
z1 = np.random.normal(0, 1, n)
z2 = np.random.normal(0, 1, n)
eps   = np.random.normal(0, 1, (d, n))
eps_y = np.random.normal(0, 1, n)

X = np.zeros((n, d))
for j in range(3):
    X[:, j] = z1 + eps[j, :] / 5.0
for j in range(3, 6):
    X[:, j] = z2 + eps[j, :] / 5.0

y1 = 3 * z1 + 2 * eps_y
y2 = 3 * z1 - 1.5 * z2 + 2 * eps_y

lambda_vals = np.linspace(0.01, 2.5, 200)

datasets = [
    (y1, r"Dataset (1): $y = 3z_1 + 2\varepsilon$",          "lasso_path_dataset_1.pdf"),
    (y2, r"Dataset (2): $y = 3z_1 - 1.5z_2 + 2\varepsilon$", "lasso_path_dataset_2.pdf"),
]

for y_data, title, filename in datasets:
    paths = np.zeros((len(lambda_vals), d))
    for i, lam in enumerate(lambda_vals):
        beta_res, _ = linear_lasso(X, y_data, lambd=lam)
        paths[i, :] = beta_res

    plt.figure(figsize=(8, 5))
    colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown']
    for j in range(d):
        plt.plot(lambda_vals, paths[:, j], label=rf'$\beta_{j+1}$', color=colors[j])
    plt.axhline(0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
    plt.xlabel(r'$\lambda$')
    plt.ylabel(r'Coefficients $\hat{\beta}$')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {filename}")

print("\n--- y1 coefficient paths ---")
for lam in [0.01, 0.1, 0.3, 0.5, 1.0, 1.5, 2.0]:
    b, _ = linear_lasso(X, y1, lam)
    print(f"  lambda={lam:.2f}: {np.round(b, 3)}")

print("\n--- y2 coefficient paths ---")
for lam in [0.01, 0.1, 0.3, 0.5, 1.0, 1.5, 2.0]:
    b, _ = linear_lasso(X, y2, lam)
    print(f"  lambda={lam:.2f}: {np.round(b, 3)}")