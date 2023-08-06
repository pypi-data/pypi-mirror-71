import filecmp
import os

from numpy.testing import assert_equal

from iseq.example import example_filepath
from iseq.gff import read as read_gff


def test_gff_read():
    items = read_gff(example_filepath("duplicate.gff")).items()
    assert_equal(len(items), 14)
    assert_equal(items[3].seqid, "GALNBKIG_00914_ont_01_plus_strand")
    assert_equal(items[6].end, 474)


def test_gff_deduplicate(tmp_path):
    os.chdir(tmp_path)

    gff = read_gff(example_filepath("duplicate.gff"))
    gff.deduplicate()

    gff.write_file("output.gff")

    dedup_file = example_filepath("deduplicate.gff")
    assert_equal(filecmp.cmp(dedup_file, "output.gff", shallow=False), True)
