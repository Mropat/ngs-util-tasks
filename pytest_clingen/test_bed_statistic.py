import pytest
import numpy as np
import pybedtools


@pytest.fixture
def bedfiles():
    return ["inputs/test_file1.bed", "inputs/test_file2.bed", "inputs/test_file3.bed"]



def test_bed_statistics(bedfiles):
    for path_to_bed in bedfiles:
        bedfile = pybedtools.BedTool(path_to_bed).remove_invalid().sort()
        assert type(bedfile) == pybedtools.bedtool.BedTool, "BED file can be read as bedtool"

        total_features = len(bedfile)
        assert total_features > 0, "BED file contain features"

        feature_length = list(map(lambda x: x.stop - x.start, bedfile))
        max_span_index = np.argmax(feature_length)
        assert type(max_span_index) == np.int64, "Max span position is an integer"
        max_span_length = np.max(feature_length)
        assert type(max_span_length) == np.int64, "Max span length is an integer"

        max_span_name = bedfile[int(max_span_index)].name
        max_span_coords = ":".join([str(bedfile[int(max_span_index)].chrom), str(
            bedfile[int(max_span_index)].start), str(bedfile[int(max_span_index)].end)])
        
        merged_bedfile = bedfile.merge()
        assert type(merged_bedfile) == pybedtools.bedtool.BedTool, "merged BED file is loaded as bedtool"

        assert len(merged_bedfile) > 0, "merged BED file contains features"

        covered_bases = sum(map(lambda x: x.stop - x.start, merged_bedfile))

