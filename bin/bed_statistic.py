import click
import pybedtools
import numpy as np


class BedSummary:
    def __init__(self, bedfile):
        self.total_features = len(bedfile)
        self.feature_length = [x.stop - x.start for x in bedfile]
        self.max_span_index = np.argmax(self.feature_length)
        self.max_span_length = np.max(self.feature_length)
        self.max_span_name = bedfile[int(self.max_span_index)].name
        self.covered_bases = sum(x.stop - x.start for x in  bedfile.merge())


@click.command()
@click.argument('bedfiles', nargs=-1, type=click.Path(exists=True))
def main(bedfiles):
    for path in bedfiles:
        bedfile = pybedtools.BedTool(path).remove_invalid().sort()
        summary = BedSummary(bedfile)
        output_string = f"""
            Summary for input {path}
            BED features: {summary.total_features}
            BED bases: {summary.covered_bases}
            Longest feature name: {summary.max_span_name}
            Longest feature span: {summary.max_span_length}"""
        click.echo(output_string)


if __name__ == "__main__":
    main()
