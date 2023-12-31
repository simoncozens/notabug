# It's not a bug (it's a feature)

## Fast feature compiler using fea-rs

This is a drop-in replacement (mostly) for `fontTools.feaLib.builder`
which uses [fea-rs](https://github.com/cmyr/fea-rs) to perform feature
compilation.

## Building

* Install maturin
* `maturin build --release`
* Install the wheel file found in `target/wheels`

## Using

Instead of

```
from fontTools.feaLib.builder import addOpenTypeFeatures
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
```

say

```
from notabug import addOpenTypeFeatures
from notabug import addOpenTypeFeaturesFromString
```

The `tables=...` argument should work. `debug=` and `filename=` are ignored.


