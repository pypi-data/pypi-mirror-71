// src/common/book_l2.hpp
// Copyright Oleg Nedbaylo 2020.
// Distributed under the Boost Software License, Version 1.0.
// See accompanying file LICENSE
// or copy at http://www.boost.org/LICENSE_1_0.txt

#pragma once
#include <string>

namespace ssc2ce {

class BookL2 {
public:
  virtual ~BookL2() {}

  virtual double top_bid_price() const = 0;
  virtual double top_ask_price() const = 0;
};

} // namespace ssc2ce
