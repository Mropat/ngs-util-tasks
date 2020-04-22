import pytest
import pybedtools
from bin.bed_overlap import get_union_bases, overlap_statistics, get_join_bases

@pytest.fixture
def bed_file_1():
    #Small test bed file with no overlapping features in other files
    return pybedtools.BedTool("test/inputs/test_file1.bed").remove_invalid().sort()

@pytest.fixture
def bed_file_2():
    #Small test bed file with one overlapping feature in file3
    return pybedtools.BedTool("test/inputs/test_file2.bed").remove_invalid().sort()

@pytest.fixture
def bed_file_3():
    #Small test bed file with one overlapping feature in file2
    return pybedtools.BedTool("test/inputs/test_file3.bed").remove_invalid().sort()

@pytest.fixture
def mo():
    #Minimum overlap
    return 1

def test_get_union_bases_int(bed_file_1, bed_file_2):
    #Test whether number bases in both files is integer (Fail if NaN)
    union_bases = get_union_bases(bed_file_1, bed_file_2)
    assert type(union_bases) == int, "Union Bases are integers"


def test_get_join_bases_int(bed_file_1, bed_file_2):
    #Test whether number bases in common is integer (Fail if NaN)
    join_bases = get_join_bases(bed_file_1, bed_file_2)
    assert type(join_bases) == int, "Union Bases are integers"


def test_get_join_bases_0(bed_file_1, bed_file_2):
    #Given two files with no overlapping bases, should find none
    join_bases = get_join_bases(bed_file_1, bed_file_2)
    assert join_bases == 0, "Should find no overlap"


def test_get_join_bases_1(bed_file_3, bed_file_2):
    #Given two files with overlapping bases, should find non-zero amount of bases
    join_bases = get_join_bases(bed_file_3, bed_file_2)
    assert join_bases != 0, "Should find overlap"


def test_overlap_statistics_1(mo, bed_file_2, bed_file_3):
    #Given two bed files with one intersecting feature, should find one intersecting feature
    intersect_features_count, total_intersect_bases = overlap_statistics(mo, bed_file_2, bed_file_3)
    assert intersect_features_count == 1, "Should find intersecting features"

    
def test_overlap_statistics_none(mo, bed_file_2, bed_file_1):
    #Given two bed files no intersecting feature, should find 0 intersecting features
    intersect_features_count, total_intersect_bases = overlap_statistics(mo, bed_file_2, bed_file_1)
    assert intersect_features_count == 0, "No intersection features"


def test_overlap_statistics_none_bases(mo, bed_file_2, bed_file_1):
    #Given two bed files no intersecting features, should find 0 intersecting bases
    intersect_features_count, total_intersect_bases = overlap_statistics(mo, bed_file_2, bed_file_1)
    assert total_intersect_bases == 0, "Should find no intersecting bases"