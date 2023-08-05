// src/deribit/book_l2.hpp
// Copyright Oleg Nedbaylo 2020.
// Distributed under the Boost Software License, Version 1.0.
// See accompanying file LICENSE
// or copy at http://www.boost.org/LICENSE_1_0.txt

#pragma once
#include <common/book_l2_map.hpp>

namespace ssc2ce {

class DeribitParser;

class DeribitBookL2 : public BookL2Map {
public:
  int64_t get_last_change_id() const { return last_change_id_; }
  void set_last_change_id(int64_t change_id) { last_change_id_ = change_id ; }

protected:
  int64_t last_change_id_ = 0;

  friend class DeribitParser;
};

} // namespace ssc2ce
