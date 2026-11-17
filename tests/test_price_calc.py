
import json
import subprocess
import sys
from pathlib import Path

import pytest

PRICE_SCRIPT = Path(__file__).resolve().parents[1] / "src" / "legacy" / "price_calc.py"


@pytest.mark.parametrize(
    "order_id, expected",
    [
        (1042, {"net": "950", "vat": "237.5", "total": "1187.5"}),
        (1044, {"net": "179.91", "vat": "44.97", "total": "224.88"}),
        (1043, {"net": "0", "vat": "0", "total": "0"}),
        (1045, {"net": "551.65", "vat": "137.91", "total": "689.56"}),
    ],
)
def test_existing_price_behavior(order_id, expected):
    result = subprocess.run(
        [sys.executable, str(PRICE_SCRIPT), str(order_id)],
        capture_output=True,
        text=True,
        check=True,
    )

    assert json.loads(result.stdout) == expected


def test_order_not_found():
    result = subprocess.run(
        [sys.executable, str(PRICE_SCRIPT), "9999"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert json.loads(result.stdout) == {"error": "finns inte"}
