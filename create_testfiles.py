import netCDF4
import numpy as np
from collections import defaultdict

def store_with_fill(filename, values, meanings, fill_value):
    rev_meanings = {v: k for k, v in meanings.items()}
    encoded_values = np.array([rev_meanings[v] for v in values], dtype="i2")
    valid_values = list(sorted(set(encoded_values) - {fill_value}))
    ds = netCDF4.Dataset(filename, "w")
    dim = ds.createDimension("time", len(encoded_values))
    var = ds.createVariable("cloud_flag", encoded_values.dtype, ("time",), fill_value=fill_value)
    var.valid_range = np.array([valid_values[0], valid_values[-1]], dtype=encoded_values.dtype)

    flag_values, flag_meanings = zip(*sorted((k, v) for k, v in meanings.items() if k != fill_value))
    var.flag_values = np.array(flag_values, dtype=encoded_values.dtype)
    var.flag_meanings = " ".join(flag_meanings)
    var.long_name = "indicator of detected clouds"
    var[:] = encoded_values
    ds.title = "Testfile for cloud_flags including _FillValue"
    ds.history = f"created by {__file__}"
    ds.Conventions = "CF-1.7"
    ds.close()


def store_without_fill(filename, values, meanings):
    rev_meanings = {v: k for k, v in meanings.items()}
    encoded_values = np.array([rev_meanings[v] for v in values], dtype="i2")
    valid_values = list(sorted(set(encoded_values)))
    ds = netCDF4.Dataset(filename, "w")
    dim = ds.createDimension("time", len(encoded_values))
    var = ds.createVariable("cloud_flag", encoded_values.dtype, ("time",))
    #var.valid_range = np.array([valid_values[0], valid_values[-1]], dtype=encoded_values.dtype)

    flag_values, flag_meanings = zip(*sorted(meanings.items()))
    var.flag_values = np.array(flag_values, dtype=encoded_values.dtype)
    var.flag_meanings = " ".join(flag_meanings)
    var.long_name = "indicator of detected clouds"
    var[:] = encoded_values
    ds.title = "Testfile for cloud_flags without _FillValue"
    ds.history = f"created by {__file__}"
    ds.Conventions = "CF-1.7"
    ds.close()

def main():
    values = [
        "unknown",
        "cloud_free",
        "probably_cloudy",
        "most_likely_cloudy",
        "probably_cloudy",
        "most_likely_cloudy",
        "cloud_free",
        "probably_cloudy",
        "most_likely_cloudy",
        "most_likely_cloudy",
        "unknown",
        "unknown",
        "unknown",
        "most_likely_cloudy",
    ]
    meanings = {
        -1: "unknown",
        0: "cloud_free",
        1: "probably_cloudy",
        2: "most_likely_cloudy",
    }

    store_with_fill("test_cloud_flag_fill.nc", values, meanings, -1)
    store_without_fill("test_cloud_flag_nofill.nc", values, meanings)

    counts = defaultdict(int)
    for v in values:
        counts[v] += 1

    print(dict(counts.items()))


if __name__ == "__main__":
    main()
