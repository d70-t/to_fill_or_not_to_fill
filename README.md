# Testing if netCDF4 `_FillValue` attributes can be used well in conjunction with `flag_values`

There has been a discussion if netCDF4 `_FillValue` attributes are a good fit to `flag_values`.
Basically the two standpoints are:

* If no data is present, it is useful not to define any flag, so a `_FillValue` should be used to define "not a flag"
* Integer types should be used for flags and usual programming environments don't have a "not an integer", so the former does not map well to in-memory representations

This repository collects examples of how data which is stored according to either of those two philosophies can be read in various programming environments.

## Results

Please click on the icons in the table to go to the example scripts:

| environment | `_FillValue` | special `flag_meaning` | remarks |
| ----------- | ------------ | ---------------------- | ------- |
| Python xarray | [😀](Python_cloudiness_fill.ipynb) | [😀](Python_cloudiness_unknown.ipynb) | `_FillValue` variant decodes into `float` 😒, both variants feel almost identical |
| Julia | [😍](Julia_cloudiness_fill.ipynb) | [😐](Julia_cloudiness_flag.ipynb) | `_FillValue` decodes into `Union{Missing, Int16}` which makes life a lot easier |

Up to now, the result is that it is a bit painful to work on languages which don't support [Tagged Unions](https://en.wikipedia.org/wiki/Tagged_union).
`xarray` of python uses the hack of converting to `float` (which knows `nan`).
This implicit conversion however does not really simplify things, as the `float`iness goes away as soon as the values are checked against a `flag_meaning`. 
In contrary, Julia uses a `Union{Missing, Int16}` which converts to `Union{Missing, Bool}` upon comparison with a `flag_meaning` and thus carries the `missing`ness along.
This greatly simplifies further computation.
