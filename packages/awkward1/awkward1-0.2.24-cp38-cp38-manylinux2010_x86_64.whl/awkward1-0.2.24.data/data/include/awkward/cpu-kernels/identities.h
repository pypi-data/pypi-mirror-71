// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/master/LICENSE

#ifndef AWKWARDCPU_IDENTITIES_H_
#define AWKWARDCPU_IDENTITIES_H_

#include "awkward/common.h"

extern "C" {
  EXPORT_SYMBOL struct Error
    awkward_new_identities32(
      int32_t* toptr,
      int64_t length);
  EXPORT_SYMBOL struct Error
    awkward_new_identities64(
      int64_t* toptr,
      int64_t length);

  EXPORT_SYMBOL struct Error
    awkward_identities32_to_identities64(
      int64_t* toptr,
      const int32_t* fromptr,
      int64_t length,
      int64_t width);

  EXPORT_SYMBOL struct Error
    awkward_identities32_from_listoffsetarray32(
      int32_t* toptr,
      const int32_t* fromptr,
      const int32_t* fromoffsets,
      int64_t fromptroffset,
      int64_t offsetsoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities32_from_listoffsetarrayU32(
      int32_t* toptr,
      const int32_t* fromptr,
      const uint32_t* fromoffsets,
      int64_t fromptroffset,
      int64_t offsetsoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities32_from_listoffsetarray64(
      int32_t* toptr,
      const int32_t* fromptr,
      const int64_t* fromoffsets,
      int64_t fromptroffset,
      int64_t offsetsoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_listoffsetarray32(
      int64_t* toptr,
      const int64_t* fromptr,
      const int32_t* fromoffsets,
      int64_t fromptroffset,
      int64_t offsetsoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_listoffsetarrayU32(
      int64_t* toptr,
      const int64_t* fromptr,
      const uint32_t* fromoffsets,
      int64_t fromptroffset,
      int64_t offsetsoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_listoffsetarray64(
      int64_t* toptr,
      const int64_t* fromptr,
      const int64_t* fromoffsets,
      int64_t fromptroffset,
      int64_t offsetsoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);

  EXPORT_SYMBOL struct Error
    awkward_identities32_from_listarray32(
      bool* uniquecontents,
      int32_t* toptr,
      const int32_t* fromptr,
      const int32_t* fromstarts,
      const int32_t* fromstops,
      int64_t fromptroffset,
      int64_t startsoffset,
      int64_t stopsoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities32_from_listarrayU32(
      bool* uniquecontents,
      int32_t* toptr,
      const int32_t* fromptr,
      const uint32_t* fromstarts,
      const uint32_t* fromstops,
      int64_t fromptroffset,
      int64_t startsoffset,
      int64_t stopsoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities32_from_listarray64(
      bool* uniquecontents,
      int32_t* toptr,
      const int32_t* fromptr,
      const int64_t* fromstarts,
      const int64_t* fromstops,
      int64_t fromptroffset,
      int64_t startsoffset,
      int64_t stopsoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_listarray32(
      bool* uniquecontents,
      int64_t* toptr,
      const int64_t* fromptr,
      const int32_t* fromstarts,
      const int32_t* fromstops,
      int64_t fromptroffset,
      int64_t startsoffset,
      int64_t stopsoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_listarrayU32(
      bool* uniquecontents,
      int64_t* toptr,
      const int64_t* fromptr,
      const uint32_t* fromstarts,
      const uint32_t* fromstops,
      int64_t fromptroffset,
      int64_t startsoffset,
      int64_t stopsoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_listarray64(
      bool* uniquecontents,
      int64_t* toptr,
      const int64_t* fromptr,
      const int64_t* fromstarts,
      const int64_t* fromstops,
      int64_t fromptroffset,
      int64_t startsoffset,
      int64_t stopsoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);

  EXPORT_SYMBOL struct Error
    awkward_identities32_from_regulararray(
      int32_t* toptr,
      const int32_t* fromptr,
      int64_t fromptroffset,
      int64_t size,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_regulararray(
      int64_t* toptr,
      const int64_t* fromptr,
      int64_t fromptroffset,
      int64_t size,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);

  EXPORT_SYMBOL struct Error
    awkward_identities32_from_indexedarray32(
      bool* uniquecontents,
      int32_t* toptr,
      const int32_t* fromptr,
      const int32_t* fromindex,
      int64_t fromptroffset,
      int64_t indexoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities32_from_indexedarrayU32(
      bool* uniquecontents,
      int32_t* toptr,
      const int32_t* fromptr,
      const uint32_t* fromindex,
      int64_t fromptroffset,
      int64_t indexoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities32_from_indexedarray64(
      bool* uniquecontents,
      int32_t* toptr,
      const int32_t* fromptr,
      const int64_t* fromindex,
      int64_t fromptroffset,
      int64_t indexoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_indexedarray32(
      bool* uniquecontents,
      int64_t* toptr,
      const int64_t* fromptr,
      const int32_t* fromindex,
      int64_t fromptroffset,
      int64_t indexoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_indexedarrayU32(
      bool* uniquecontents,
      int64_t* toptr,
      const int64_t* fromptr,
      const uint32_t* fromindex,
      int64_t fromptroffset,
      int64_t indexoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_indexedarray64(
      bool* uniquecontents,
      int64_t* toptr,
      const int64_t* fromptr,
      const int64_t* fromindex,
      int64_t fromptroffset,
      int64_t indexoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth);

  EXPORT_SYMBOL struct Error
    awkward_identities32_from_unionarray8_32(
      bool* uniquecontents,
      int32_t* toptr,
      const int32_t* fromptr,
      const int8_t* fromtags,
      const int32_t* fromindex,
      int64_t fromptroffset,
      int64_t tagsoffset,
      int64_t indexoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth,
      int64_t which);
  EXPORT_SYMBOL struct Error
    awkward_identities32_from_unionarray8_U32(
      bool* uniquecontents,
      int32_t* toptr,
      const int32_t* fromptr,
      const int8_t* fromtags,
      const uint32_t* fromindex,
      int64_t fromptroffset,
      int64_t tagsoffset,
      int64_t indexoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth,
      int64_t which);
  EXPORT_SYMBOL struct Error
    awkward_identities32_from_unionarray8_64(
      bool* uniquecontents,
      int32_t* toptr,
      const int32_t* fromptr,
      const int8_t* fromtags,
      const int64_t* fromindex,
      int64_t fromptroffset,
      int64_t tagsoffset,
      int64_t indexoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth,
      int64_t which);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_unionarray8_32(
      bool* uniquecontents,
      int64_t* toptr,
      const int64_t* fromptr,
      const int8_t* fromtags,
      const int32_t* fromindex,
      int64_t fromptroffset,
      int64_t tagsoffset,
      int64_t indexoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth,
      int64_t which);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_unionarray8_U32(
      bool* uniquecontents,
      int64_t* toptr,
      const int64_t* fromptr,
      const int8_t* fromtags,
      const uint32_t* fromindex,
      int64_t fromptroffset,
      int64_t tagsoffset,
      int64_t indexoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth,
      int64_t which);
  EXPORT_SYMBOL struct Error
    awkward_identities64_from_unionarray8_64(
      bool* uniquecontents,
      int64_t* toptr,
      const int64_t* fromptr,
      const int8_t* fromtags,
      const int64_t* fromindex,
      int64_t fromptroffset,
      int64_t tagsoffset,
      int64_t indexoffset,
      int64_t tolength,
      int64_t fromlength,
      int64_t fromwidth,
      int64_t which);

  EXPORT_SYMBOL struct Error
    awkward_identities32_extend(
      int32_t* toptr,
      const int32_t* fromptr,
      int64_t fromoffset,
      int64_t fromlength,
      int64_t tolength);
  EXPORT_SYMBOL struct Error
    awkward_identities64_extend(
      int64_t* toptr,
      const int64_t* fromptr,
      int64_t fromoffset,
      int64_t fromlength,
      int64_t tolength);

}

#endif // AWKWARDCPU_IDENTITIES_H_
