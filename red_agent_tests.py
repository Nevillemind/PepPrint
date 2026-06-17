#!/usr/bin/env python3
"""
PepPrint Red Agent Tests — Adversarial testing suite
Tests: malformed JSON, SQL injection, pathological values, missing fields, edge cases
"""
import json
import urllib.request
import urllib.error
import sys
import os
import time

BASE = os.environ.get("PEPPRINT_URL", "http://localhost:3000")

def req(method, path, body=None, content_type="application/json"):
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body else None
    rq = urllib.request.Request(url, data=data, method=method)
    rq.add_header("Content-Type", content_type)
    rq.add_header("Accept", "application/json")
    try:
        rsp = urllib.request.urlopen(rq, timeout=10)
        return rsp.status, rsp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:
        return 0, str(e)

passed = 0
failed = 0

def test(name, fn):
    global passed, failed
    try:
        result = fn()
        if result:
            print(f"  ✅ PASS: {name}")
            passed += 1
        else:
            print(f"  ❌ FAIL: {name}")
            failed += 1
    except Exception as e:
        print(f"  ❌ FAIL: {name} — exception: {e}")
        failed += 1

def assert_status(status, expected):
    return status == expected

def assert_contains(body, substring):
    return substring.lower() in body.lower()

def assert_not_contains(body, substring):
    return substring.lower() not in body.lower()

def assert_json(body):
    try:
        json.loads(body)
        return True
    except:
        return False

print("=" * 60)
print("  PepPrint Red Agent — Adversarial Test Suite")
print("=" * 60)

# ─── 1. HEALTH ENDPOINT ───
print("\n── HEALTH ENDPOINT ──")

def t_health_get():
    s, b = req("GET", "/api/health")
    return assert_status(s, 200) and assert_json(b) and assert_contains(b, "ok")

def t_health_post():
    s, b = req("POST", "/api/health", {"foo": "bar"})
    # Should reject or handle gracefully
    return s in (200, 405)  # 405 Method Not Allowed is acceptable

def t_health_sql_inject():
    s, b = req("GET", "/api/health?x=%27%20OR%201=1--")
    # Should still return 200, not crash or leak data
    return s == 200 and assert_json(b)

test("GET /api/health returns 200 OK", t_health_get)
test("POST /api/health doesn't crash", t_health_post)
test("GET /api/health with SQL injection query param", t_health_sql_inject)

# ─── 2. PEPTIDES ENDPOINT ──
print("\n── PEPTIDES ENDPOINT ──")

def t_peptides_get():
    s, b = req("GET", "/api/peptides")
    return assert_status(s, 200) and assert_json(b)

def t_peptides_post():
    s, b = req("POST", "/api/peptides", {"name": "fake"})
    return s in (200, 405, 404)

def t_peptides_sql_inject_path():
    s, b = req("GET", "/api/peptides/1%27%20OR%201=1--")
    return s in (200, 404) and not assert_contains(b, "SQLITE") and not assert_contains(b, "sqlite")

def t_peptides_huge_id():
    s, b = req("GET", "/api/peptides/99999999999999999999999999999999999999999")
    return s in (200, 404, 414)

test("GET /api/peptides returns 200", t_peptides_get)
test("POST /api/peptides doesn't crash", t_peptides_post)
test("GET /api/peptides SQL injection in path", t_peptides_sql_inject_path)
test("GET /api/peptides with pathological ID", t_peptides_huge_id)

# ─── 3. BIOMARKERS ENDPOINT ──
print("\n── BIOMARKERS ENDPOINT ──")

def t_biomarkers_get():
    s, b = req("GET", "/api/biomarkers")
    return assert_status(s, 200) and assert_json(b)

def t_biomarkers_null_byte():
    s, b = req("GET", "/api/biomarkers/%00")
    return s in (200, 404, 400)

test("GET /api/biomarkers returns 200", t_biomarkers_get)
test("GET /api/biomarkers null byte injection", t_biomarkers_null_byte)

# ─── 4. ANALYZE ENDPOINT — CORE RED AGENT TESTS ───
print("\n── ANALYZE ENDPOINT — Malformed Input ──")

def t_analyze_empty_body():
    s, b = req("POST", "/api/analyze", None)
    # Should handle empty body, not crash
    return s != 500

def t_analyze_not_json():
    s, b = req("POST", "/api/analyze", "this is not json", "text/plain")
    return s != 500 and not assert_contains(b, "panic")

def t_analyze_empty_object():
    s, b = req("POST", "/api/analyze", {})
    return s != 500

def t_analyze_null():
    s, b = req("POST", "/api/analyze", None)
    return s != 500

def t_analyze_missing_biomarkers():
    s, b = req("POST", "/api/analyze", {"foo": "bar"})
    return s != 500

def t_analyze_empty_biomarkers():
    s, b = req("POST", "/api/analyze", {"biomarkers": []})
    return s != 500

def t_analyze_biomarkers_not_array():
    s, b = req("POST", "/api/analyze", {"biomarkers": "hs-CRP"})
    return s != 500

def t_analyze_int_as_biomarkers():
    s, b = req("POST", "/api/analyze", {"biomarkers": 42})
    return s != 500

def t_analyze_bool_as_biomarkers():
    s, b = req("POST", "/api/analyze", {"biomarkers": True})
    return s != 500

test("Empty body", t_analyze_empty_body)
test("Non-JSON content type", t_analyze_not_json)
test("Empty JSON object", t_analyze_empty_object)
test("Null body", t_analyze_null)
test("Missing biomarkers field", t_analyze_missing_biomarkers)
test("Empty biomarkers array", t_analyze_empty_biomarkers)
test("Biomarkers as string not array", t_analyze_biomarkers_not_array)
test("Biomarkers as integer", t_analyze_int_as_biomarkers)
test("Biomarkers as boolean", t_analyze_bool_as_biomarkers)

print("\n── ANALYZE ENDPOINT — Pathological Values ──")

def t_analyze_negative_value():
    s, b = req("POST", "/api/analyze", {
        "biomarkers": [{"name": "hs-CRP", "value": -50, "unit": "mg/L"}]
    })
    return s != 500

def t_analyze_zero_value():
    s, b = req("POST", "/api/analyze", {
        "biomarkers": [{"name": "hs-CRP", "value": 0, "unit": "mg/L"}]
    })
    return s != 500

def t_analyze_extremely_large_value():
    s, b = req("POST", "/api/analyze", {
        "biomarkers": [{"name": "hs-CRP", "value": 1e308, "unit": "mg/L"}]
    })
    return s != 500

def t_analyze_nan_value():
    s, b = req("POST", "/api/analyze", {
        "biomarkers": [{"name": "hs-CRP", "value": "NaN", "unit": "mg/L"}]
    })
    return s != 500

def t_analyze_infinity():
    s, b = req("POST", "/api/analyze", {
        "biomarkers": [{"name": "hs-CRP", "value": "Infinity", "unit": "mg/L"}]
    })
    return s != 500

def t_analyze_string_value():
    s, b = req("POST", "/api/analyze", {
        "biomarkers": [{"name": "hs-CRP", "value": "high", "unit": "mg/L"}]
    })
    return s != 500

def t_analyze_null_value():
    s, b = req("POST", "/api/analyze", {
        "biomarkers": [{"name": "hs-CRP", "value": None, "unit": "mg/L"}]
    })
    return s != 500

def t_analyze_missing_name():
    s, b = req("POST", "/api/analyze", {
        "biomarkers": [{"value": 5.2, "unit": "mg/L"}]
    })
    return s != 500

def t_analyze_missing_value():
    s, b = req("POST", "/api/analyze", {
        "biomarkers": [{"name": "hs-CRP", "unit": "mg/L"}]
    })
    return s != 500

def t_analyze_extra_fields():
    s, b = req("POST", "/api/analyze", {
        "biomarkers": [{"name": "hs-CRP", "value": 5.2, "unit": "mg/L", "__proto__": {"polluted": True}, "constructor": "malicious"}]
    })
    return s != 500

test("Negative value", t_analyze_negative_value)
test("Zero value", t_analyze_zero_value)
test("Extremely large value (1e308)", t_analyze_extremely_large_value)
test("NaN value", t_analyze_nan_value)
test("Infinity value", t_analyze_infinity)
test("String value instead of number", t_analyze_string_value)
test("Null value", t_analyze_null_value)
test("Missing biomarker name", t_analyze_missing_name)
test("Missing biomarker value", t_analyze_missing_value)
test("Extra/prototype pollution fields", t_analyze_extra_fields)

print("\n── ANALYZE ENDPOINT — SQL Injection ──")

injection_payloads = [
    ("'; DROP TABLE biomarkers; --", "Classic DROP TABLE"),
    ("1' OR '1'='1", "OR injection"),
    ("'; SELECT * FROM sqlite_master; --", "Schema enumeration"),
    ("1; DELETE FROM peptides; --", "DELETE injection"),
    ("' UNION SELECT 1,2,3,4,5--", "UNION SELECT"),
    ("${7*7}", "Template injection"),  # SSTI probe
    ("$(cat /etc/passwd)", "Command injection probe"),
    ("../../../etc/passwd", "Path traversal"),
]

for payload, desc in injection_payloads:
    def make_test(p=payload, d=desc):
        def _t():
            s, b = req("POST", "/api/analyze", {
                "biomarkers": [{"name": p, "value": 5.0, "unit": "mg/L"}]
            })
            # Must not crash (500) – server should handle gracefully
            if s == 500:
                return False
            # Parse JSON – injection must NOT produce recommendations (would mean SQL executed)
            try:
                data = json.loads(b)
                recs = data.get("recommendations", [])
                # If recommendations appeared from the injection, that's a real leak
                if len(recs) > 0:
                    return False
            except:
                pass
            return True
        return _t
    test(f"SQL Injection — {desc}", make_test())

print("\n── ANALYZE ENDPOINT — Large Payloads ──")

def t_analyze_many_biomarkers():
    markers = []
    for i in range(1000):
        markers.append({"name": f"test-{i}", "value": float(i), "unit": "arb"})
    s, b = req("POST", "/api/analyze", {"biomarkers": markers})
    return s != 500

def t_analyze_deep_nesting():
    deep = {}
    current = deep
    for i in range(100):
        current["nested"] = {}
        current = current["nested"]
    current["biomarkers"] = [{"name": "hs-CRP", "value": 5.0}]
    s, b = req("POST", "/api/analyze", deep)
    return s != 500

def t_analyze_large_string():
    s, b = req("POST", "/api/analyze", {
        "biomarkers": [{"name": "A" * 100000, "value": 5.0, "unit": "mg/L"}]
    })
    return s != 500

def t_analyze_unicode_bomb():
    s, b = req("POST", "/api/analyze", {
        "biomarkers": [{"name": "测试" * 5000, "value": 5.0, "unit": "mg/L"}]
    })
    return s != 500

test("1000 biomarkers (DoS probe)", t_analyze_many_biomarkers)
test("Deep nesting (100 levels)", t_analyze_deep_nesting)
test("100KB biomarker name", t_analyze_large_string)
test("Unicode bomb (5000x CJK)", t_analyze_unicode_bomb)

print("\n── ANALYZE ENDPOINT — Concurrency (if applicable) ──")

import concurrent.futures

def single_request():
    try:
        s, b = req("POST", "/api/analyze", {
            "biomarkers": [{"name": "hs-CRP", "value": 5.0, "unit": "mg/L"}]
        })
        return s
    except:
        return 0

def t_concurrent_requests():
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        futures = [ex.submit(single_request) for _ in range(50)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    # Accept 200, 429 (rate limit), 503 (overload) — just not crashes
    crashes = sum(1 for r in results if r == 500 or r == 0)
    print(f"    50 concurrent requests → {crashes} crashes, {sum(1 for r in results if r == 200)}x 200")
    return crashes == 0

test("50 concurrent requests (20 workers)", t_concurrent_requests)

# ─── FINAL INTEGRITY CHECK ───
print("\n── FINAL DATABASE INTEGRITY CHECK ──")
time.sleep(0.5)
s, b = req("GET", "/api/biomarkers")
if s == 200 and assert_json(b):
    count = len(json.loads(b)) if isinstance(json.loads(b), list) else 0
    if count == 11:
        print(f"  ✅ Biomarkers table intact: {count} biomarkers (expected 11)")
    else:
        print(f"  ❌ Biomarkers count mismatch: {count} (expected 11)")
        failed += 1
else:
    print(f"  ❌ Cannot verify biomarkers table")
    failed += 1

s, b = req("GET", "/api/peptides")
if s == 200 and assert_json(b):
    count = len(json.loads(b)) if isinstance(json.loads(b), list) else 0
    if count == 14:
        print(f"  ✅ Peptides table intact: {count} peptides (expected 14)")
    else:
        print(f"  ❌ Peptides count mismatch: {count} (expected 14)")
        failed += 1
else:
    print(f"  ❌ Cannot verify peptides table")
    failed += 1

# ─── SUMMARY ───
print("\n" + "=" * 60)
print(f"  RESULTS: {passed} passed, {failed} failed, {passed + failed} total")
if failed == 0:
    print("  ✅ ALL RED AGENT TESTS PASSED")
else:
    print(f"  ⚠️  {failed} failures — investigation required")
print("=" * 60)

sys.exit(0 if failed == 0 else 1)
