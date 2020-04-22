import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import click
sns.set()


def read_count_data(filename):
    coverage_df = pd.read_csv(filename, sep="\t")
    return coverage_df


def plot_mean_coverage(coverage_df, filename):
    _, axs = plt.subplots(1, 2)
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


@click.command()
@click.argument("filename", type=click.Path(exists=True))
def main(filename):
    coverage_df = read_count_data(filename)
    if coverage_df["meanCoverage"].mean() == 0:
        click.echo("No coverage detected, aborting")
    else:
        plot_mean_coverage(coverage_df, filename)
        click.echo("Success!")

if __name__ == "__main__":
    main()
