import click
import pybedtools
import numpy as np


@click.command()
@click.argument('bedfiles', nargs=-1, type=click.Path(exists=True))
def bed_statistics(bedfiles):
    for path_to_bed in bedfiles:
        bedfile = pybedtools.BedTool(path_to_bed).remove_invalid().sort()
        total_features = len(bedfile)
        feature_length = list(map(lambda x: x.stop - x.start, bedfile))
        max_span_index = np.argmax(feature_length)
        max_span_length = np.max(feature_length)
        max_span_name = bedfile[int(max_span_index)].name
        max_span_coords = ":".join([str(bedfile[int(max_span_index)].chrom), str(
            bedfile[int(max_span_index)].start), str(bedfile[int(max_span_index)].end)])
        merged_bedfile = bedfile.merge()
        covered_bases = sum(map(lambda x: x.stop - x.start, merged_bedfile))

        click.echo("")
        click.echo(f"Summary for input {path_to_bed}")
        click.echo(f"BED features: {total_features}")
        click.echo(f"BED bases: {covered_bases}")
        click.echo(f"Longest feature name: {max_span_name}")
        click.echo(f"Longest feature span: {max_span_length}")
        click.echo(f"Longest feature coordinates: {max_span_coords}")


if __name__ == "__main__":
    bed_statistics()
