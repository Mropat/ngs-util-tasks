import click
import pybedtools


def overlap_statistics(mo, bed_file_1, bed_file_2):
    intersect_bed = bed_file_1.intersect(bed_file_2, wo=True)
    intersect_spans = [int(x[-1]) for x in intersect_bed if int(x[-1]) >= mo]
    intersect_features_count = len(intersect_spans)
    total_intersect_bases = sum(intersect_spans)
    return intersect_features_count, total_intersect_bases

def get_join_bases(bed_file_1, bed_file_2):
    join_bed = (bed_file_1+bed_file_2).merge()
    join_bases =  sum((x.stop - x.start for x in join_bed))
    return join_bases


def get_union_bases(bed_file_1, bed_file_2):
    union_bed = (bed_file_1.cat(bed_file_2)).merge()
    union_bases = sum((x.stop - x.start for x in union_bed))
    return union_bases
    

@click.command()
@click.option('--mo', default=1, help='Minimum overlapping bases', type=click.INT)
@click.option('--in1', help='Path to BED file 1', type=click.Path(exists=True), required=True)
@click.option('--in2', help='Path to BED file 2', type=click.Path(exists=True), required=True)
def main(mo, in1, in2):
    bed_file_1 = pybedtools.BedTool(in1).remove_invalid().sort()
    bed_file_2 = pybedtools.BedTool(in2).remove_invalid().sort()

    intersect_features_count, total_intersect_bases = overlap_statistics(mo, bed_file_1, bed_file_2)
    union_bases = get_union_bases(bed_file_1, bed_file_2)
    join_bases = get_join_bases(bed_file_1, bed_file_2)

    output_string = f"""
        Join statistics   
        Input 1: {in1}
        Input 2: {in2}
        Minimum overlap span: {mo}
        Overlapping features: {intersect_features_count}
        Total overlapping bases (intersect): {total_intersect_bases}
        Total bases covered by features with overlap: {join_bases}
        Total bases in both (union): {union_bases}"""
    click.echo(output_string)


if __name__ == "__main__":
    main()
