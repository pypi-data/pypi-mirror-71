// Copyright (c) 2020 [Your Name]. All rights reserved.

#define CATCH_CONFIG_MAIN

#include <catch2/catch.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

extern "C" {
#include <lrcalc/vector.h>
}
#include <nlnum/nlnum.h>

namespace py = pybind11;

TEST_CASE("Create a vector from an iterable", "[iterable_to_vector]") {
  const std::vector<int> vec = {1, 2, 3, 4};
  vector* v = nlnum::to_vector(vec);

  REQUIRE(v->length == 4);
  for (size_t i = 0; i < v->length; i++) {
    REQUIRE(v->array[i] == vec[i]);
  }

  v_free(v);
}

TEST_CASE("Littlewood-Richardson coefficient", "[lrcoef]") {
  SECTION("Test 1") {
    const int64_t lr = nlnum::lrcoef({3, 2, 1}, {2, 1}, {2, 1});
    REQUIRE(lr == 2);
  }
  SECTION("Test 2") {
    const int64_t lr = nlnum::lrcoef({3, 3}, {2, 1}, {2, 1});
    REQUIRE(lr == 1);
  }
  SECTION("Test 3") {
    const int64_t lr = nlnum::lrcoef({2, 1, 1, 1, 1}, {2, 1}, {2, 1});
    REQUIRE(lr == 0);
  }
}

TEST_CASE("Newell-Littlewood number", "[nlcoef]") {
  const int64_t nl = nlnum::nlcoef({2, 1}, {2, 1}, {4, 2});
  REQUIRE(nl == 1);
}
