import pytest
import pybedtools

@pytest.fixture
def in1():
    return "inputs/test_file1.bed"


@pytest.fixture
def in2():
    return "inputs/test_file2.bed"


@pytest.fixture
def mo():
    return 1


def test_overlap_statistics(mo, in1, in2):
    bed_file_1 = pybedtools.BedTool(in1).remove_invalid().sort()
    assert type(bed_file_1) == pybedtools.bedtool.BedTool, "BED file can be read as bedtool"
    bed_file_2 = pybedtools.BedTool(in2).remove_invalid().sort()
    assert type(bed_file_2) == pybedtools.bedtool.BedTool, "BED file can be read as bedtool"

    intersect_bed = bed_file_1.intersect(bed_file_2, wo=True)
    assert type(intersect_bed) == pybedtools.bedtool.BedTool, "Overlap BED file can be read as bedtool"

    intersect_spans = [int(x[-1])
                       for x in list(intersect_bed) if int(x[-1]) >= mo]
    intersect_features_count = len(intersect_spans)
    total_intersect_bases = sum(intersect_spans)

    union_bed = (bed_file_1+bed_file_2).merge()
    assert type(union_bed) == pybedtools.bedtool.BedTool, "Union BED file can be read as bedtool"
    union_bases = sum(map(lambda x: x.stop - x.start, union_bed))
