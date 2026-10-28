#ifndef AMPL_SLICE_H
#define AMPL_SLICE_H

#include <vector>

#include "ampl/ampl_c.h"
#include "ampl/variant.h"

namespace ampl {
class DataFrame;

/**
 * Represents a slice (row or column) of a DataFrame.
 */
template <bool ROW>
class Slice {
  friend class ampl::DataFrame;
  AMPL_DATAFRAME *data_;
  std::size_t fixedIndex_;

  Slice(AMPL_DATAFRAME *data, std::size_t index)
      : data_(data), fixedIndex_(index) {}
  // A proxy used for implementing operator->.
  class Proxy {
   private:
    Variant inner_;

   public:
    // Constructor
    explicit Proxy(Variant e) : inner_(e) {}
    // Arrow operator
    const Variant *operator->() const { return &inner_; }
  };

 public:
  class iterator {
   public:
    using iterator_category = std::forward_iterator_tag;
    using value_type = Variant;
    using difference_type = std::ptrdiff_t;
    using pointer = value_type *;
    using reference = value_type &;

   private:
    friend class Slice;
    const Slice *parent_;
    std::size_t index_;
    iterator(const Slice *parent, std::size_t index)
        : parent_(parent), index_(index) {}

   public:
    value_type operator*() const { return (*parent_)[index_]; }
    iterator &operator++() {
      ++index_;
      return *this;
    }
    iterator operator++(int) {
      iterator clone(*this);
      ++index_;
      return clone;
    }
    bool operator==(const iterator &other) const {
      return (parent_->data_ == other.parent_->data_) &&
             (parent_->fixedIndex_ == other.parent_->fixedIndex_) &&
             (index_ == other.index_);
    }
    bool operator!=(const iterator &other) const { return !(*this == other); }
    /*
     * Arrow operator
     */
    Proxy operator->() const { return Proxy((*parent_)[index_]); }
  };

  std::size_t size() const {
    size_t size;
    if (ROW)
      AMPL_DataFrameGetNumCols(data_, &size);
    else
      AMPL_DataFrameGetNumRows(data_, &size);
    return size;
  }

  iterator begin() const { return iterator(this, 0); }

  iterator end() const { return iterator(this, size()); }

  Variant operator[](std::size_t index) const {
    AMPL_VARIANT *v;

    if (ROW)
      AMPL_DataFrameElement(data_, fixedIndex_, index, &v);
    else
      AMPL_DataFrameElement(data_, index, fixedIndex_, &v);
    return Variant(v);
  }
};
}  // namespace ampl

#endif  // AMPL_SLICE_H
