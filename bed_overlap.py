import click
import pybedtools
import numpy as np


@click.command()
@click.option('--mo', default=1, help='Minimum overlapping bases', type=click.INT)
@click.option('--in1', help='Path to BED file 1', type=click.Path(exists=True), required=True)
@click.option('--in2', help='Path to BED file 2', type=click.Path(exists=True), required=True)
def overlap_statistics(mo, in1, in2):
    bed_file_1 = pybedtools.BedTool(in1).remove_invalid().sort()
    bed_file_2 = pybedtools.BedTool(in2).remove_invalid().sort()

    intersect_bed = bed_file_1.intersect(bed_file_2, wo=True)
    intersect_spans = [int(x[-1])
                       for x in list(intersect_bed) if int(x[-1]) >= mo]
    intersect_features_count = len(intersect_spans)
    total_intersect_bases = sum(intersect_spans)

    union_bed = (bed_file_1+bed_file_2).merge()
    union_bases = sum(map(lambda x: x.stop - x.start, union_bed))

    click.echo("")
    click.echo(f"Join statistics")
    click.echo(f"Input 1: {in1}")
    click.echo(f"Input 2: {in2}")
    click.echo(f"Minimum overlap span: {mo}")
    click.echo(f"Overlapping features: {intersect_features_count}")
    click.echo(f"Total overlapping bases (intersect): {total_intersect_bases}")
    click.echo(f"Total bases (union): {union_bases}")


if __name__ == "__main__":
    overlap_statistics()
