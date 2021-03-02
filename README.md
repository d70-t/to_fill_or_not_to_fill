# Testing if netCDF4 `_FillValue` attributes can be used well in conjunction with `flag_values`

There has been a discussion if netCDF4 `_FillValue` attributes are a good fit to `flag_values`.
Basically the two standpoints are:

* If no data is present, it is useful not to define any flag, so a `_FillValue` should be used to define "not a flag"
* Integer types should be used for flags and usual programming environments don't have a "not an integer", so the former does not map well to in-memory representations

This repository collects examples of how data which is stored according to either of those two philosophies can be read in various programming environments.

The example are meant to be done in a way which one would usually approach the problem of computing a cloud fraction from the sample datasets.
As the authors are not necessarily native or fluent in the respective programming languages, so please raise an issue if you feel that something would be implemented differently by a native programmer in that language.
We are also searching for more examples in more languages, so please feel free to add more as you like :-)

## Results

Please click on the icons in the table to go to the example scripts:

| environment | `_FillValue` | special `flag_meaning` | remarks |
| ----------- | ------------ | ---------------------- | ------- |
| Python xarray | [😀](Python_cloudiness_fill.ipynb) | [😀](Python_cloudiness_unknown.ipynb) | `_FillValue` variant decodes into `float` 😒 because Python doesn't know `NA` or Union types and [pandas doesn't like `np.ma`](https://pandas.pydata.org/pandas-docs/version/0.19.2/gotchas.html#nan-integer-na-values-and-na-type-promotions), both variants feel almost identical |
| Julia | [😍](Julia_cloudiness_fill.ipynb) | [😐](Julia_cloudiness_flag.ipynb) | `_FillValue` decodes into `Union{Missing, Int16}` which makes life a lot easier |
| R | [😍](R_cloudiness_fill.ipynb) | [😒](R_cloudiness_flag.ipynb) | `_FillValue` decodes into `NA` which makes life a lot easier, missing list comprehensions make handling flags a lot harder |

Up to now, the result is that it is a bit painful to work on languages which don't support [Tagged Unions](https://en.wikipedia.org/wiki/Tagged_union) or a generic indication for missing values.
`xarray` of python uses the hack of converting to `float` (which knows `nan`).
This implicit conversion however does not really simplify things, as the `float`iness goes away as soon as the values are checked against a `flag_meaning`. 
In contrary, Julia uses a `Union{Missing, Int16}` which converts to `Union{Missing, Bool}` upon comparison with a `flag_meaning` and thus carries the `missing`ness along.
R does not use Unions, but provides a generic method to handle missing values (`NA`).
In consequence, handling those values works just as in Julia.
This greatly simplifies further computation.

List comprehensions greatly simplify the work on flag enumerations. R does not have list comprehensions which makes handling flags directly **a lot** harder.
