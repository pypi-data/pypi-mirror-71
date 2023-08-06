// Copyright 2020 ICLUE @ UIUC. All rights reserved.

#include <algorithm>
#include <cstdint>
#include <map>
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

extern "C" {
#include <lrcalc/hashtab.h>
#include <lrcalc/symfcn.h>
#include <lrcalc/vector.h>
}

#include <nlnum/nlnum.h>

namespace py = pybind11;

namespace nlnum {

vector* to_vector(const std::vector<int>& vec) {
  vector* v = v_new(static_cast<int>(vec.size()));
  for (size_t i = 0; i < vec.size(); ++i) {
    v->array[i] = vec[i];
  }
  return v;
}

bool to_cppvec(const vector* v, std::vector<int>* vec) {
  if (v == nullptr || vec == nullptr) return false;
  vec->clear();

  const size_t n = v->length;
  vec->reserve(n);

  for (size_t i = 0; i < v->length; ++i) {
    vec->push_back(v->array[i]);
  }

  return true;
}

int64_t lrcoef(
    const std::vector<int>& outer,
    const std::vector<int>& inner1,
    const std::vector<int>& inner2) {
  vector* o = to_vector(outer);
  vector* i1 = to_vector(inner1);
  vector* i2 = to_vector(inner2);

  const int64_t result = lrcoef(o, i1, i2);

  v_free(o);
  v_free(i1);
  v_free(i2);

  return result;
}

// Computes the intersection of two partitions.
const std::vector<int> Intersection(
    const std::vector<int>& a,
    const std::vector<int>& b) {
  const size_t n = std::min(a.size(), b.size());
  std::vector<int> c(n);
  for (size_t i = 0; i < n; ++i) {
    c[i] = std::min(a[i], b[i]);
  }

  return c;
}

// Evaluates one term in the sum.
int64_t nlcoef_helper(
    const std::vector<int>& alpha,
    const std::vector<int>& mu,
    const std::vector<int>& nu,
    const std::vector<int>& lambda) {
  int64_t nl_im = 0;

  vector* aa = to_vector(alpha);
  vector* mm = to_vector(mu);
  vector* nn = to_vector(nu);
  hashtab* s1 = skew(mm, aa, 0);
  hashtab* s2 = skew(nn, aa, 0);
  v_free(aa);
  v_free(mm);
  v_free(nn);

  std::map<std::vector<int>, int> ss1, ss2;
  to_map(s1, &ss1);
  to_map(s2, &ss2);
  hash_free(s1);
  hash_free(s2);

  for (const auto& p1 : ss1) {
    for (const auto& p2 : ss2) {
      // These are the 2 LR coefficients.
      const int c1 = p1.second;
      const int c2 = p2.second;

      vector* v1 = to_vector(p1.first);
      vector* v2 = to_vector(p2.first);
      hashtab* ht = mult(v1, v2, 0);
      v_free(v1);
      v_free(v2);

      std::map<std::vector<int>, int> ss;
      to_map(ht, &ss);
      hash_free(ht);

      if (ss.find(lambda) != ss.end()) {
        const int c3 = ss[lambda];
        nl_im += c1 * c2 * c3;
      }
    }
  }

  return nl_im;
}

int64_t nlcoef(
    const std::vector<int>& mu,
    const std::vector<int>& nu,
    const std::vector<int>& lambda) {
  int64_t nl = 0;
  // Step 1: Compute the intersection of mu and nu.
  const std::vector<int> limit = Intersection(mu, nu);

  // Step 2: Iterate through each partition in the intersection.
  std::vector<int> alpha(limit.size());
  int level = static_cast<int>(alpha.size())-1;

  nl += nlcoef_helper(alpha, mu, nu, lambda);
  while (true) {
    const int lneighbor = level == 0 ? INT_MAX : alpha[level-1];
    if (level >= 0 && alpha[level] >= std::min(lneighbor, limit[level])) {
      alpha[level--] = 0;
      if (level < 0) break;
    } else {
      ++alpha[level];
      level = static_cast<int>(alpha.size()) - 1;
      nl += nlcoef_helper(alpha, mu, nu, lambda);
    }
  }

  return nl;
}

bool to_map(hashtab* ht, std::map<std::vector<int>, int>* m) {
  if (ht == nullptr || m == nullptr) return false;
  m->clear();

  hash_itr itr;
  hash_first(ht, itr);
  while (hash_good(itr)) {
    const vector* v = static_cast<vector*>(hash_key(itr));
    std::vector<int> p;
    to_cppvec(v, &p);
    const int c = hash_intvalue(itr);
    m->insert({p, c});
    hash_next(itr);
  }

  return true;
}

}  // namespace nlnum

