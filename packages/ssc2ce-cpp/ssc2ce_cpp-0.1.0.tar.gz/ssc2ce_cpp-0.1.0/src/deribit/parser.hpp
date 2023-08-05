// Copyright Oleg Nedbaylo 2020.
// Distributed under the Boost Software License, Version 1.0.
// See accompanying file LICENSE
// or copy at http://www.boost.org/LICENSE_1_0.txt

#pragma once
#include "book_l2.hpp"
#include <common/parser.hpp>
#include <functional>
#include <rapidjson/document.h>
#include <string_view>

namespace ssc2ce {

class DeribitParser : public Parser {
public:
  using BookEvent = std::function<void(BookL2 *)>;
  DeribitParser();
  ~DeribitParser() {}

  bool parse(const char *message) override;

  std::string last_error_msg() const
  {
    return last_error_msg_;
  }

  void reset_error()
  {
    last_error_msg_.clear();
  }

  BookL2 const *get_book(const std::string_view &instrument);

  void set_on_book_setup(BookEvent handler)
  {
    on_book_setup_ = handler;
  }

  void set_on_book_update(BookEvent handler)
  {
    on_book_update_ = handler;
  }

private:
  std::string last_error_msg_;
  DeribitBookL2 &find_or_create_book(const std::string_view &instrument);
  bool parse_book(const char *channel, const rapidjson::Value &data);
  //   using ParseChannel = std::function<bool(const char *)>;
  std::map<std::string_view, DeribitBookL2> books_;
  BookEvent on_book_setup_;
  BookEvent on_book_update_;
};

} // namespace ssc2ce