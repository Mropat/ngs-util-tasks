import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import click
sns.set()


@click.command()
@click.argument("filename", type=click.Path(exists=True))
def plot_mean_coverage(filename):
    coverage_df = pd.read_csv(filename, sep="\t")

    if coverage_df["meanCoverage"].mean() == 0:
        click.echo(f"No coverage in sample {filename}, aborting")
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

    plt.savefig(os.path.basename(filename)+".png", dpi=100)
    plt.close()


if __name__ == "__main__":
    plot_mean_coverage()
