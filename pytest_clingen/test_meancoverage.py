import pytest
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
sns.set()

@pytest.fixture
def filename():
    return "inputs/test_L001_flat.cov"

def test_plot_mean_coverage(filename):
    coverage_df = pd.read_csv(filename, sep="\t")
    assert type(coverage_df) == pd.core.frame.DataFrame, "DataFrame can be loaded"

    if coverage_df["meanCoverage"].mean() == 0:
        print(f"No coverage in sample {filename}, aborting")
        return False

    fig, axs = plt.subplots(1, 2)
    axs[0].hist(coverage_df["meanCoverage"], bins=50)
    axs[0].axvline(100, color="red", lw=1)
    axs[0].set_title("meanCoverage")

    axs[1].hist(coverage_df["meanCoverage"] /
                coverage_df["meanCoverage"].mean(), bins=50)
    axs[1].axvline(100 / coverage_df["meanCoverage"].mean(), color="red", lw=1)
    axs[1].set_title("Normalized meanCoverage")

    for ax in axs.flat:
        ax.set(xlabel='Coverage', ylabel='Frequency')
        ax.figure.set_size_inches(12, 5)
        ax.label_outer()

    plt.savefig("out/"+ os.path.basename(filename)+".png", dpi=100)
    assert os.path.exists("out/"+ os.path.basename(filename)+".png"), "Figure is saved"

    plt.close()

