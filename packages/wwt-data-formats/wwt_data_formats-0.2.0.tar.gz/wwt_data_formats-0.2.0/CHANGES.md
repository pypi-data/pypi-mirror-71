# 0.2.0 (2020-Jun-17)

- Clarify that the `requests` package is now always required.
- Add `wwt_data_formats.layers` for dealing with WWTL layer-export files.

# 0.1.3 (2020-Jun-06)

- Add a CLI tool, `wwtdatatool`, to provide interfaces to certain low-level
  operations
- Add some infrastructure to support walking of trees of folders with on-the-fly
  downloads as needed.
- Support the Imageset::reference_frame attribute
- Support Communities metadata
- Fix the test suite for Python 3.8


# 0.1.2 (2020-Mar-20)

- Fix roundtripping of imagesets with a non-empty QuadTreeMap, and add a few
  more attributes on the `<ImageSet>` type.
- Fix loading of XML files missing attributes that we expected to see.
- Allow "Tangent" as an alias for "Tan" when deserializing ProjectionType
  enums.
- Add `to_xml_string()` and `write_xml()` convenience methods on the
  LockedXmlTraits class that's a base class for most of our data types.


# 0.1.1 (2020-Mar-17)

- Fix `wwt_data_formats.imageset.ImageSet.set_position_from_wcs()` for the new
  metadata scheme.


# 0.1.0 (2020-Mar-17)

- Massive infrastructure rebuild. We now use traitlets and have a framework
  for XML serialization, rather than a bunch of boilerplate code. We can
  now deserialize folders and their contents.


# 0.0.2 (2020-Feb-05)

- Document the FileCabinet support
- Work with FITS files that have `CDELT{1,2}` but not `PC1_1` and `PC2_2`.
- Removed Python 2.7 from the CI.


# 0.0.1 (2019-Dec-04)

- First version
