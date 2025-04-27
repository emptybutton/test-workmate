from log_reporting.infrastructure.lang_tools import slices


def test_slices() -> None:
    assert (
        set(slices(range(0, 550, 200)))
        == {slice(0, 200), slice(200, 400), slice(400, 550)}
    )
