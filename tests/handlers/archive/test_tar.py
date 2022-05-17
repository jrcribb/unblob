import pytest
from helpers import unhex

from unblob.file_utils import File
from unblob.handlers.archive.tar import TarHandler, _get_tar_end_offset

GNU_TAR_CONTENTS = unhex(
    """\
00000000  74 65 73 74 2f 66 6f 6f  2e 64 61 74 00 00 00 00  |test/foo.dat....|
00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000060  00 00 00 00 30 30 30 30  36 34 34 00 30 30 30 31  |....0000644.0001|
00000070  37 35 30 00 30 30 30 30  31 34 34 00 30 30 30 30  |750.0000144.0000|
00000080  30 30 30 30 32 30 30 00  31 34 31 36 30 30 35 35  |0000200.14160055|
00000090  37 32 35 00 30 31 30 32  32 33 00 20 30 00 00 00  |725.010223. 0...|
000000a0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000100  00 75 73 74 61 72 20 20  00 00 00 00 00 00 00 00  |.ustar  ........|
00000110  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000200  c4 d8 da 39 27 3e 70 1b  ec 79 fc 36 d7 e4 4e 58  |...9'>p..y.6..NX|
00000210  e7 ef 90 0d 83 26 a9 f6  71 a2 42 b0 19 43 d3 ea  |.....&..q.B..C..|
00000220  29 48 38 39 cd a0 e9 ad  38 1e 53 3f 60 4d e1 2a  |)H89....8.S?`M.*|
00000230  de 8b ca f8 64 66 c1 0d  5e 4c aa fa cc c5 ab 73  |....df..^L.....s|
00000240  1d 2d ec f1 1b 5f aa 4a  b4 c7 94 95 00 60 3a a3  |.-..._.J.....`:.|
00000250  42 d9 45 2c d8 b1 99 11  da f7 33 34 7d 21 2f d4  |B.E,......34}!/.|
00000260  b3 f6 cd c6 62 80 d1 39  0c 47 c1 fe 30 15 42 39  |....b..9.G..0.B9|
00000270  7b fd 92 94 f7 fe 90 94  77 97 8c 76 61 e7 2c 13  |{.......w..va.,.|
00000280  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000400
"""
)

POSIX_TAR_CONTENTS = unhex(
    """\
00000000  2e 2f 50 61 78 48 65 61  64 65 72 73 2f 74 65 73  |./PaxHeaders/tes|
00000010  74 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |t...............|
00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000060  00 00 00 00 30 30 30 30  36 34 34 00 30 30 30 30  |....0000644.0000|
00000070  30 30 30 00 30 30 30 30  30 30 30 00 30 30 30 30  |000.0000000.0000|
00000080  30 30 30 30 31 33 32 00  31 34 31 37 37 30 33 34  |0000132.14177034|
00000090  35 34 31 00 30 31 31 32  30 31 00 20 78 00 00 00  |541.011201. x...|
000000a0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000100  00 75 73 74 61 72 00 30  30 00 00 00 00 00 00 00  |.ustar.00.......|
00000110  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000200  33 30 20 6d 74 69 6d 65  3d 31 36 34 33 39 31 39  |30 mtime=1643919|
00000210  37 31 33 2e 35 30 38 34  30 30 33 39 38 0a 33 30  |713.508400398.30|
00000220  20 61 74 69 6d 65 3d 31  36 34 33 39 31 39 37 34  | atime=164391974|
00000230  31 2e 35 36 38 35 34 32  34 35 37 0a 33 30 20 63  |1.568542457.30 c|
00000240  74 69 6d 65 3d 31 36 34  33 39 31 39 37 31 33 2e  |time=1643919713.|
00000250  35 30 38 34 30 30 33 39  38 0a 00 00 00 00 00 00  |508400398.......|
00000260  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000400  74 65 73 74 2f 00 00 00  00 00 00 00 00 00 00 00  |test/...........|
00000410  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000460  00 00 00 00 30 30 30 30  37 37 35 00 30 30 30 31  |....0000775.0001|
00000470  37 35 30 00 30 30 30 31  37 35 30 00 30 30 30 30  |750.0001750.0000|
00000480  30 30 30 30 30 30 30 00  31 34 31 37 37 30 33 34  |0000000.14177034|
00000490  35 34 31 00 30 31 30 32  36 35 00 20 35 00 00 00  |541.010265. 5...|
000004a0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000500  00 75 73 74 61 72 00 30  30 00 00 00 00 00 00 00  |.ustar.00.......|
00000510  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000540  00 00 00 00 00 00 00 00  00 30 30 30 30 30 30 30  |.........0000000|
00000550  00 30 30 30 30 30 30 30  00 00 00 00 00 00 00 00  |.0000000........|
00000560  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000600  74 65 73 74 2f 50 61 78  48 65 61 64 65 72 73 2f  |test/PaxHeaders/|
00000610  66 6f 6f 2e 64 61 74 00  00 00 00 00 00 00 00 00  |foo.dat.........|
00000620  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000660  00 00 00 00 30 30 30 30  36 34 34 00 30 30 30 30  |....0000644.0000|
00000670  30 30 30 00 30 30 30 30  30 30 30 00 30 30 30 30  |000.0000000.0000|
00000680  30 30 30 30 30 37 34 00  31 34 31 36 30 30 35 35  |0000074.14160055|
00000690  37 32 35 00 30 31 32 34  30 32 00 20 78 00 00 00  |725.012402. x...|
000006a0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000700  00 75 73 74 61 72 00 30  30 00 00 00 00 00 00 00  |.ustar.00.......|
00000710  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000800  33 30 20 61 74 69 6d 65  3d 31 36 34 33 39 31 39  |30 atime=1643919|
00000810  37 34 31 2e 35 36 38 35  34 32 34 35 37 0a 33 30  |741.568542457.30|
00000820  20 63 74 69 6d 65 3d 31  36 34 33 39 31 39 37 31  | ctime=164391971|
00000830  33 2e 35 30 38 34 30 30  33 39 38 0a 00 00 00 00  |3.508400398.....|
00000840  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000a00  74 65 73 74 2f 66 6f 6f  2e 64 61 74 00 00 00 00  |test/foo.dat....|
00000a10  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000a60  00 00 00 00 30 30 30 30  36 34 34 00 30 30 30 31  |....0000644.0001|
00000a70  37 35 30 00 30 30 30 31  37 35 30 00 30 30 30 30  |750.0001750.0000|
00000a80  30 30 30 30 32 30 30 00  31 34 31 36 30 30 35 35  |0000200.14160055|
00000a90  37 32 35 00 30 31 31 35  32 37 00 20 30 00 00 00  |725.011527. 0...|
00000aa0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000b00  00 75 73 74 61 72 00 30  30 00 00 00 00 00 00 00  |.ustar.00.......|
00000b10  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000b40  00 00 00 00 00 00 00 00  00 30 30 30 30 30 30 30  |.........0000000|
00000b50  00 30 30 30 30 30 30 30  00 00 00 00 00 00 00 00  |.0000000........|
00000b60  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000c00  c4 d8 da 39 27 3e 70 1b  ec 79 fc 36 d7 e4 4e 58  |...9'>p..y.6..NX|
00000c10  e7 ef 90 0d 83 26 a9 f6  71 a2 42 b0 19 43 d3 ea  |.....&..q.B..C..|
00000c20  29 48 38 39 cd a0 e9 ad  38 1e 53 3f 60 4d e1 2a  |)H89....8.S?`M.*|
00000c30  de 8b ca f8 64 66 c1 0d  5e 4c aa fa cc c5 ab 73  |....df..^L.....s|
00000c40  1d 2d ec f1 1b 5f aa 4a  b4 c7 94 95 00 60 3a a3  |.-..._.J.....`:.|
00000c50  42 d9 45 2c d8 b1 99 11  da f7 33 34 7d 21 2f d4  |B.E,......34}!/.|
00000c60  b3 f6 cd c6 62 80 d1 39  0c 47 c1 fe 30 15 42 39  |....b..9.G..0.B9|
00000c70  7b fd 92 94 f7 fe 90 94  77 97 8c 76 61 e7 2c 13  |{.......w..va.,.|
00000c80  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00002800
"""
)

PADDING_TO_DEFAULT_BLOCKING_FACTOR = unhex(
    """\
00000400  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00002800"""
)

PADDING_AFTER_END_OF_ARCHIVE = unhex(
    """\
00000400  00 00 00 00 00 00 00 00  FF FF FF FF FF FF FF FF  |................|
"""
)


@pytest.mark.parametrize(
    "contents, expected_length, message",
    (
        pytest.param(
            GNU_TAR_CONTENTS + PADDING_TO_DEFAULT_BLOCKING_FACTOR,
            len(GNU_TAR_CONTENTS + PADDING_TO_DEFAULT_BLOCKING_FACTOR),
            "File end should be the same when archive is created using default parameters",
            id="padded-to-default-blocking-factor",
        ),
        pytest.param(
            GNU_TAR_CONTENTS + 2 * PADDING_TO_DEFAULT_BLOCKING_FACTOR,
            len(GNU_TAR_CONTENTS + PADDING_TO_DEFAULT_BLOCKING_FACTOR),
            "File end shouldn't go over the default BLOCKING_FACTOR (RECORDSIZE) even when it is zeroed",
            id="padded-over-than-default-blocking-factor",
        ),
        pytest.param(
            GNU_TAR_CONTENTS,
            len(GNU_TAR_CONTENTS),
            "File end should be at the last block's end when end-of-file marker is missing",
            id="not-padded",
        ),
        pytest.param(
            GNU_TAR_CONTENTS + PADDING_AFTER_END_OF_ARCHIVE,
            len(GNU_TAR_CONTENTS),
            "File end shouldn't include partial zero filled blocks",
            id="padded-after-end",
        ),
        pytest.param(
            POSIX_TAR_CONTENTS,
            len(POSIX_TAR_CONTENTS),
            "File end should be at the last block's end when end-of-file marker is missing",
            id="posix-not-padded",
        ),
        pytest.param(
            POSIX_TAR_CONTENTS + PADDING_AFTER_END_OF_ARCHIVE,
            len(POSIX_TAR_CONTENTS),
            "File end shouldn't include partial zero filled blocks",
            id="posix-padded-after-end",
        ),
    ),
)
def test_offset(contents: bytes, expected_length: int, message: str):
    f = File.from_bytes(contents)

    offset = _get_tar_end_offset(f)
    assert offset == expected_length, message


@pytest.mark.parametrize(
    "contents",
    (
        pytest.param(
            GNU_TAR_CONTENTS,
            id="gnu-tar",
        ),
        pytest.param(
            POSIX_TAR_CONTENTS,
            id="posix-tar",
        ),
    ),
)
@pytest.mark.parametrize(
    "start_complete, message",
    (
        pytest.param(
            False,
            "File is truncated and no content can be recovered",
            id="empty-truncated",
        ),
        pytest.param(
            True,
            "File is truncated but valid parts should be recovered",
            id="truncated",
        ),
    ),
)
def test_truncated_files(contents: bytes, start_complete: bool, message: str):
    truncated = contents[:0x180]

    if start_complete:
        f = File.from_bytes(contents + truncated)
    else:
        f = File.from_bytes(truncated)

    offset = _get_tar_end_offset(f)
    if start_complete:
        assert offset == len(contents), message
    else:
        assert offset == -1, message


X9216_TAR = unhex(
    """\
00000000  78 39 32 31 36 00 00 00  00 00 00 00 00 00 00 00  |x9216...........|
00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000060  00 00 00 00 30 30 30 30  36 36 34 00 30 30 30 30  |....0000664.0000|
00000070  30 30 30 00 30 30 30 30  30 30 30 00 30 30 30 30  |000.0000000.0000|
00000080  30 30 32 32 30 30 30 00  31 34 32 33 34 32 31 37  |0022000.14234217|
00000090  33 32 34 00 30 31 30 32  36 36 00 20 30 00 00 00  |324.010266. 0...|
000000a0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000100  00 75 73 74 61 72 20 20  00 72 6f 6f 74 00 00 00  |.ustar  .root...|
00000110  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000120  00 00 00 00 00 00 00 00  00 72 6f 6f 74 00 00 00  |.........root...|
00000130  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000200  78 78 78 78 78 78 78 78  78 78 78 78 78 78 78 78  |xxxxxxxxxxxxxxxx|
*
00002600  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00005000
"""
)


def test_end_of_tar_archive_marker_split_between_records():
    # X9216_TAR is a GNU tar file, that has a file in it of size 9216
    # This means, that with the default blocking factor of 20,
    # the record size is 0x2800 = 10240 = 512 + 9216 + 512, thus the second closing
    # block of 512 0 bytes do not fit in the first record.
    # The end result is that the second half of the tar file is all 0,
    # but needed to be properly formatted.
    content = File.from_bytes(X9216_TAR)
    assert len(content) == 0x5000
    assert _get_tar_end_offset(content) == len(content)


X9216_TAR_BLOCKING_1 = unhex(
    """\
00000000  78 39 32 31 36 00 00 00  00 00 00 00 00 00 00 00  |x9216...........|
00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000060  00 00 00 00 30 30 30 30  36 36 34 00 30 30 30 30  |....0000664.0000|
00000070  30 30 30 00 30 30 30 30  30 30 30 00 30 30 30 30  |000.0000000.0000|
00000080  30 30 32 32 30 30 30 00  31 34 32 33 34 32 31 37  |0022000.14234217|
00000090  33 32 34 00 30 31 30 32  36 36 00 20 30 00 00 00  |324.010266. 0...|
000000a0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000100  00 75 73 74 61 72 20 20  00 72 6f 6f 74 00 00 00  |.ustar  .root...|
00000110  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000120  00 00 00 00 00 00 00 00  00 72 6f 6f 74 00 00 00  |.........root...|
00000130  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000200  78 78 78 78 78 78 78 78  78 78 78 78 78 78 78 78  |xxxxxxxxxxxxxxxx|
*
00002600  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00002a00
"""
)


def test_different_blocking_factor():
    # X9216_TAR_BLOCKING_1 is created from the same file with GNU tar
    # but this time with a --blocking-factor=1
    assert X9216_TAR.startswith(X9216_TAR_BLOCKING_1)
    content = File.from_bytes(X9216_TAR_BLOCKING_1)
    assert len(content) == 0x2A00
    assert _get_tar_end_offset(content) == len(content)


@pytest.mark.parametrize(
    "prefix",
    (
        pytest.param(b"", id="zero-prefix"),
        pytest.param(b"some prefix ", id="nonzero-prefix"),
    ),
)
def test_calculate_chunk(prefix):
    tar_file = File.from_bytes(prefix + GNU_TAR_CONTENTS)
    handler = TarHandler()

    chunk = handler.calculate_chunk(tar_file, len(prefix))

    assert chunk is not None
    assert chunk.start_offset == len(prefix)
    assert chunk.end_offset == len(prefix) + len(GNU_TAR_CONTENTS)
