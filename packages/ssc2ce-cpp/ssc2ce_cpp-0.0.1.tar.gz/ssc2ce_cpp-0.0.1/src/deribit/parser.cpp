// Copyright Oleg Nedbaylo 2020.
// Distributed under the Boost Software License, Version 1.0.
// See accompanying file LICENSE
// or copy at http://www.boost.org/LICENSE_1_0.txt

#include "parser.hpp"
#include <fmt/format.h>
#include <iostream>
#include <rapidjson/document.h>

namespace ssc2ce {

DeribitParser::DeribitParser()
{
}

bool DeribitParser::parse(const char *message)
{
  if (message[0] == char(0)) {
    last_error_msg_ = "Empty string.";
    return false;
  }

  using namespace rapidjson;
  rapidjson::Document doc;
  doc.Parse(message);
  if (doc.IsNull()) {
    last_error_msg_ = "Unable to parse the message, probably the wrong JSON format.";
    return false;
  }

  bool processed = false;
  if (doc.HasMember("method")) {
    const char *method = doc["method"].GetString();
    const auto &params = doc["params"];
    if (strcmp(method, "subscription") == 0) {
      const auto &data = params["data"];
      const char *channel = params["channel"].GetString();

      switch (channel[0]) {
      case 'a': {
        // announcements
      } break;
      case 'b': {
        // book.{instrument_name}.{group}.{depth}.{interval} or
        // book.{instrument_name}.{interval}
        return parse_book(channel, data);
      } break;
      case 'c': {
        // chart.trades.{instrument_name}.{resolution}
      } break;
      case 'd': {
        // deribit_price_index.{index_name} or deribit_price_ranking.{index_name}
      } break;
      case 'e': {
        // estimated_expiration_price
      } break;
      case 'm': {
        // markprice.options.{index_name}
      } break;
      case 'p': {
        // perpetual.{instrument_name}.{interval} or
        // platform_state
      } break;
      case 'q': {
        // quote.{instrument_name}
      } break;
      case 't': {
        if (channel[1] == 'i') {
          // ticker.{instrument_name}.{interval} or
        } else {
          // trades.{instrument_name}.{interval} or
          // trades.{kind}.{currency}.{interval}
        }
      } break;
      case 'u': // user.*
      {
        switch (channel[5]) {
        case 'c': {
          // user.changes.{instrument_name}.{interval} or
          // user.changes.{kind}.{currency}.{interval}
        } break;
        case 'o': {
          // user.orders.{instrument_name}.raw or
          // user.orders.{instrument_name}.{interval}
          // user.orders.{kind}.{currency}.raw
          // user.orders.{kind}.{currency}.{interval}

        } break;
        case 'p': {
          // user.portfolio.{currency}
        } break;
        case 't': {
          // user.trades.{instrument_name}.{interval} or
          // user.trades.{kind}.{currency}.{interval}
        } break;
        default:
          break;
        }
      } break;
      default:
        break;
      }

      if (!processed) {
        last_error_msg_ = fmt::format("DeribitParser Unsupported: {} in message: {}", channel, message);
      }
    } else {
      last_error_msg_ = fmt::format("DeribitParser Unknown method: {} in message: {}", method, message);
    }
  } else {
    last_error_msg_ = fmt::format("DeribitParser Unknown message format: {}", message);
  }

  return processed;
}

bool DeribitParser::parse_book(const char *channel, const rapidjson::Value &data)
{
  // book.{instrument_name}.{group}.{depth}.{interval} or
  // book.{instrument_name}.{interval}
  constexpr char point = '.';
  const char *pos = channel + 5;
  const char *next_poit = std::strchr(pos, point);
  if (!next_poit) {
    last_error_msg_ = fmt::format("DeribitParser Unknown channel format: {}", channel);
    return false;
  }

  bool result = false;
  std::string_view instrumnet(pos, next_poit - pos);
  auto &book = books_[instrumnet];
  const int64_t change_id = data["change_id"].GetInt64();

  pos = next_poit + 1;
  next_poit = std::strchr(pos, point);
  if (next_poit ||                      // book.{instrument_name}.{group}.{depth}.{interval}
      !data.HasMember("prev_change_id") // book.{instrument_name}.{interval} with snapshot
  ) {
    // Reset Book
    book.clear();
    book.set_last_change_id(change_id);

    const auto &bids{data["bids"]};
    for (const auto &item : bids.GetArray()) {
      book.add_bid(item[1].GetDouble(), item[2].GetDouble());
    }

    const auto &asks{data["asks"]};
    for (const auto &item : asks.GetArray()) {
      book.add_ask(item[1].GetDouble(), item[2].GetDouble());
    }

    result = true;
    if (on_book_setup_)
      on_book_setup_(&book);
  } else {
    // Update book
    const auto update_side = [&](BookL2Map::BookSide &side, const rapidjson::Value &side_data) {
      for (const auto &item : side_data.GetArray()) {
        auto action = item[0].GetString();
        switch (action[0]) {
        case 'c': // change
          side.update(item[1].GetDouble(), item[2].GetDouble());
          break;
        case 'n': // new
          side.add(item[1].GetDouble(), item[2].GetDouble());
          break;
        case 'd': // delete
          side.remove(item[1].GetDouble());
          break;
        default:
          last_error_msg_ = fmt::format("DeribitParser::parse_book Channel {} unknown action", channel, action);
          return false;
        }
      }
      return true;
    };

    result = update_side(book.asks_, data["asks"]) && update_side(book.bids_, data["bids"]);
    if (result && on_book_update_) {
      on_book_update_(&book);
    }
  }

  return result;
}

BookL2 const *DeribitParser::get_book(const std::string_view &instrument)
{
  BookL2 const *book = &books_[instrument];
  return book;
}

} // namespace ssc2ce