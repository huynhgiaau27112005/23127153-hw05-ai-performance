#!/usr/bin/env python3
"""Generate valid JMeter 5.6 JMX plans for HW05."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom

STUDENT_ID = "23127153"
DATE_TAG = "20260830"
BASE = Path(__file__).resolve().parents[1]
CSV_PATH = BASE / "data" / "users.csv"

SCENARIOS = {
    "Load": {"threads": 15, "ramp": 30, "loops": 6, "think": 2000, "listener": "SummaryReport", "listener_label": "Summary Report", "duration": 0},
    "Stress": {"threads": 35, "ramp": 60, "loops": 8, "think": 1000, "listener": "StatVisualizer", "listener_label": "Aggregate Report", "duration": 0},
    "Spike": {"threads": 50, "ramp": 5, "loops": 3, "think": 500, "listener": "ViewResultsFullVisualizer", "listener_label": "View Results Tree", "duration": 0},
    "Endurance": {"threads": 10, "ramp": 20, "loops": -1, "think": 1500, "listener": "SummaryReport", "listener_label": "Summary Report", "duration": 600},
}


def save_config(full: bool = False) -> ET.Element:
    obj = ET.Element("objProp")
    ET.SubElement(obj, "name").text = "saveConfig"
    val = ET.SubElement(obj, "value", attrib={"class": "SampleSaveConfiguration"})
    fields = [
        ("time", "true"), ("latency", "true" if full else "false"), ("timestamp", "true"),
        ("success", "true" if full else "false"), ("label", "true"), ("code", "true" if full else "false"),
        ("message", "true" if full else "false"), ("threadName", "true"), ("dataType", "false"),
        ("encoding", "false"), ("assertions", "true" if full else "false"), ("subresults", "false"),
        ("responseData", "false"), ("samplerData", "false"), ("xml", "true"), ("fieldNames", "false"),
        ("responseHeaders", "false"), ("requestHeaders", "false"), ("responseDataOnError", "false"),
        ("saveAssertionResultsFailureMessage", "false"), ("assertionsResultsToSave", "0"),
    ]
    if full:
        fields.append(("bytes", "true"))
    for tag, text in fields:
        ET.SubElement(val, tag).text = text
    return obj


def result_collector(guiclass: str, label: str) -> ET.Element:
    rc = ET.Element(
        "ResultCollector",
        guiclass=guiclass,
        testclass="ResultCollector",
        testname=label,
        enabled="true",
    )
    rc.append(bp("ResultCollector.error_logging", "false"))
    rc.append(save_config(guiclass == "ViewResultsFullVisualizer"))
    rc.append(sp("filename", ""))
    return rc


def sp(name: str, text: str) -> ET.Element:
    e = ET.Element("stringProp", name=name)
    e.text = text
    return e


def ip(name: str, text: str) -> ET.Element:
    e = ET.Element("intProp", name=name)
    e.text = text
    return e


def bp(name: str, text: str = "false") -> ET.Element:
    e = ET.Element("boolProp", name=name)
    e.text = text
    return e


def ht(parent: ET.Element) -> ET.Element:
    return ET.SubElement(parent, "hashTree")


def sampler(name: str, path: str, method: str = "GET", body: str = "") -> ET.Element:
    s = ET.Element("HTTPSamplerProxy", guiclass="HttpTestSampleGui", testclass="HTTPSamplerProxy", testname=name, enabled="true")
    args = ET.SubElement(s, "elementProp", name="HTTPsampler.Arguments", elementType="Arguments", guiclass="HTTPArgumentsPanel", testclass="Arguments", enabled="true")
    coll = ET.SubElement(args, "collectionProp", name="Arguments.arguments")
    if body:
        arg = ET.SubElement(coll, "elementProp", name="", elementType="HTTPArgument")
        bp("HTTPArgument.always_encode", "false")
        sp("Argument.value", body)
        sp("Argument.metadata", "=")
        for c in list(arg):
            arg.remove(c)
        ET.SubElement(arg, "boolProp", name="HTTPArgument.always_encode").text = "false"
        ET.SubElement(arg, "stringProp", name="Argument.value").text = body
        ET.SubElement(arg, "stringProp", name="Argument.metadata").text = "="
    s.append(sp("HTTPSampler.domain", "${BASE_HOST}"))
    s.append(sp("HTTPSampler.port", "${BASE_PORT}"))
    s.append(sp("HTTPSampler.protocol", "http"))
    s.append(sp("HTTPSampler.path", path))
    s.append(sp("HTTPSampler.method", method))
    s.append(bp("HTTPSampler.follow_redirects", "true"))
    s.append(bp("HTTPSampler.use_keepalive", "true"))
    s.append(bp("HTTPSampler.postBodyRaw", "true" if body else "false"))
    return s


def json_ext(name: str, ref: str, expr: str, default: str = "") -> ET.Element:
    j = ET.Element("JSONPostProcessor", guiclass="JSONPostProcessorGui", testclass="JSONPostProcessor", testname=name, enabled="true")
    j.append(sp("JSONPostProcessor.referenceNames", ref))
    j.append(sp("JSONPostProcessor.jsonPathExprs", expr))
    j.append(sp("JSONPostProcessor.match_numbers", "1"))
    if default:
        j.append(sp("JSONPostProcessor.defaultValues", default))
    return j


def headers(pairs: list[tuple[str, str]]) -> ET.Element:
    hm = ET.Element("HeaderManager", guiclass="HeaderPanel", testclass="HeaderManager", testname="HTTP Header Manager", enabled="true")
    coll = ET.SubElement(hm, "collectionProp", name="HeaderManager.headers")
    for k, v in pairs:
        el = ET.SubElement(coll, "elementProp", name="", elementType="Header")
        ET.SubElement(el, "stringProp", name="Header.name").text = k
        ET.SubElement(el, "stringProp", name="Header.value").text = v
    return hm


def assert_code(name: str, code: str = "200") -> ET.Element:
    ra = ET.Element("ResponseAssertion", guiclass="AssertionGui", testclass="ResponseAssertion", testname=name, enabled="true")
    coll = ET.SubElement(ra, "collectionProp", name="Asserion.test_strings")
    ET.SubElement(coll, "stringProp", name="49586").text = code
    ra.append(sp("Assertion.custom_message", ""))
    ra.append(sp("Assertion.test_field", "Assertion.response_code"))
    ra.append(bp("Assertion.assume_success", "false"))
    ra.append(ip("Assertion.test_type", "8"))
    return ra


def build(scenario: str, cfg: dict) -> str:
    root = ET.Element("jmeterTestPlan", version="1.2", properties="5.0", jmeter="5.6.3")
    tree = ht(root)
    plan = ET.SubElement(tree, "TestPlan", guiclass="TestPlanGui", testclass="TestPlan", testname=f"{STUDENT_ID}_{scenario}_{DATE_TAG}", enabled="true")
    plan.append(sp("TestPlan.comments", f"HW05 E2E perf {scenario}"))
    plan.append(bp("TestPlan.functional_mode", "false"))
    plan.append(bp("TestPlan.serialize_threadgroups", "false"))
    pht = ht(tree)

    udv = ET.SubElement(pht, "Arguments", guiclass="ArgumentsPanel", testclass="Arguments", testname="User Defined Variables", enabled="true")
    coll = ET.SubElement(udv, "collectionProp", name="Arguments.arguments")
    for n, v in [("BASE_HOST", "127.0.0.1"), ("BASE_PORT", "3010")]:
        el = ET.SubElement(coll, "elementProp", name=n, elementType="Argument")
        ET.SubElement(el, "stringProp", name="Argument.name").text = n
        ET.SubElement(el, "stringProp", name="Argument.value").text = v
        ET.SubElement(el, "stringProp", name="Argument.metadata").text = "="
    ht(pht)

    tg = ET.SubElement(pht, "ThreadGroup", guiclass="ThreadGroupGui", testclass="ThreadGroup", testname="E2E Users", enabled="true")
    tg.append(ip("ThreadGroup.num_threads", str(cfg["threads"])))
    tg.append(ip("ThreadGroup.ramp_time", str(cfg["ramp"])))
    tg.append(bp("ThreadGroup.same_user_on_next_iteration", "true"))
    tg.append(sp("ThreadGroup.on_sample_error", "continue"))
    lc = ET.SubElement(tg, "elementProp", name="ThreadGroup.main_controller", elementType="LoopController", guiclass="LoopControlPanel", testclass="LoopController", enabled="true")
    lc.append(bp("LoopController.continue_forever", "false"))
    lc.append(ip("LoopController.loops", str(cfg["loops"])))
    if cfg["duration"]:
        tg.append(bp("ThreadGroup.scheduler", "true"))
        tg.append(sp("ThreadGroup.duration", str(cfg["duration"])))
        tg.append(sp("ThreadGroup.delay", "0"))
    tht = ht(pht)

    csv = ET.SubElement(tht, "CSVDataSet", guiclass="TestBeanGUI", testclass="CSVDataSet", testname="users.csv", enabled="true")
    csv.append(sp("filename", str(CSV_PATH).replace("\\", "/")))
    csv.append(sp("fileEncoding", "UTF-8"))
    csv.append(sp("variableNames", "email,password,search_keyword,product_id,quantity,shipping_address"))
    csv.append(bp("ignoreFirstLine", "true"))
    csv.append(bp("quotedData", "false"))
    csv.append(bp("recycle", "true"))
    csv.append(bp("stopThread", "false"))
    csv.append(sp("shareMode", "shareMode.all"))
    ht(tht)

    tht.append(headers([("X-Student-Id", STUDENT_ID)]))
    ht(tht)

    # Login
    tht.append(headers([("Content-Type", "application/json")]))
    ht(tht)
    tht.append(sampler("01 Login", "/api/login", "POST", '{"email":"${email}","password":"${password}"}'))
    lht = ht(tht)
    lht.append(json_ext("token", "auth_token", "$.token"))
    ht(lht)
    lht.append(assert_code("Login 200"))
    ht(lht)

    tht.append(sampler("02 Products search", "/api/products?search=${search_keyword}", "GET"))
    pht2 = ht(tht)
    pht2.append(json_ext("pid", "product_id_runtime", "$.[0].id", "${product_id}"))
    ht(pht2)

    tht.append(sampler("03 Product detail", "/api/products/${product_id_runtime}", "GET"))
    ht(tht)

    tht.append(headers([("Content-Type", "application/json"), ("Authorization", "Bearer ${auth_token}")]))
    ht(tht)
    tht.append(sampler("04 Add cart", "/api/cart", "POST", '{"id":${product_id_runtime},"name":"Perf","price":100000,"quantity":${quantity}}'))
    ht(tht)

    tht.append(sampler("05 Checkout", "/api/checkout", "POST", '{"total_amount":100000,"shipping_address":"${shipping_address}"}'))
    ht(tht)

    timer = ET.SubElement(tht, "ConstantTimer", guiclass="ConstantTimerGui", testclass="ConstantTimer", testname="Think", enabled="true")
    timer.append(sp("ConstantTimer.delay", str(cfg["think"])))
    ht(tht)

    # Scenario-specific GUI listener (Summary / Aggregate / View Results Tree)
    pht.append(result_collector(cfg["listener"], cfg["listener_label"]))
    ht(pht)

    rough = ET.tostring(root, encoding="unicode")
    return minidom.parseString(rough).toprettyxml(indent="  ")


def main() -> None:
    out = BASE / "test-plans"
    out.mkdir(exist_ok=True)
    for name, cfg in SCENARIOS.items():
        path = out / f"{STUDENT_ID}_{name}_{DATE_TAG}.jmx"
        path.write_text(build(name, cfg), encoding="utf-8")
        print("Wrote", path)


if __name__ == "__main__":
    main()
