// src/common/book_l2_map.hpp
// Copyright Oleg Nedbaylo 2020.
// Distributed under the Boost Software License, Version 1.0.
// See accompanying file LICENSE
// or copy at http://www.boost.org/LICENSE_1_0.txt

#pragma once
#include "book_l2.hpp"
#include <map>

namespace ssc2ce {

class BookL2Map : public BookL2 {
public:
  BookL2Map(const std::string &instrument) : BookL2{instrument} {}
  double top_bid_price() const override { return bids_.empty() ? 0. : bids_.crbegin()->first; }
  double top_ask_price() const override { return asks_.empty() ? 0. : asks_.cbegin()->first; }

  void add_ask(double price, double size)
  {
    asks_.add(price, size);
  }

  void add_bid(double price, double size)
  {
    bids_.add(price, size);
  }

  void update_ask(double price, double size)
  {
    asks_.update(price, size);
  }

  void update_bid(double price, double size)
  {
    bids_.update(price, size);
  }

  void remove_ask(double price)
  {
    asks_.remove(price);
  }

  void remove_bid(double price)
  {
    bids_.remove(price);
  }

  void clear() {
    asks_.clear();
    bids_.clear();
  }

protected:
  class BookSide : public std::map<double, double> {
  public:
    void add(double price, double size)
    {
      if (size != 0.0) {
        emplace(price, size);
      }
    }

    void update(double price, double size)
    {
      if (size != 0.0) {
        this->operator[](price) = size;
      } else {
        remove(price);
      }
    }

    void remove(double price)
    {
      auto i = find(price);
      if (i != end()) {
        erase(i);
      }
    }
  };

  BookSide bids_;
  BookSide asks_;
};

} // namespace ssc2ce
