import random
import tempfile
import os

import parser
import graphtaint


random.seed(42)

errors = []
tests_run = 0


def test_function(name, function, *args):
    global tests_run
    tests_run += 1

    try:
        function(*args)
    except Exception as error:
        errors.append(f"{name}: {type(error).__name__}: {error}")


# Different types of values to test
def random_value():
    return random.choice([
        "Pod",
        "Service",
        "Deployment",
        "",
        None,
        123,
        True,
        "@#$%",
        "x" * 100
    ])


# Different dictionary structures to test
def random_dictionary():
    return random.choice([
        {},
        {"kind": "Pod"},
        {"metadata": {"name": "web"}},
        {"spec": {"containers": [{"name": "web"}]}},
        {"kind": random_value()},
        {"kind": {"nested": random_value()}},
        {"metadata": {"labels": {"app": "web", "type": "test"}}}
    ])


for i in range(100):

    name = f"pod-{random.randint(1, 1000)}"
    key = random.choice(["name", "kind", "spec", "metadata", "missing"])
    value = random_value()
    data = random_dictionary()

    # 1. Test checkIfWeirdYAML
    yaml_text = random.choice([
        f"kind: Pod\nmetadata:\n  name: {name}",
        "",
        "kind: [",
        f"kind: {value}",
        f"metadata:\n  name: {name}\n  labels:\n    app: web"
    ])
    test_function("checkIfWeirdYAML", parser.checkIfWeirdYAML, yaml_text)

    # 2. Test keyMiner
    test_function("keyMiner", parser.keyMiner, data, key)

    # 3. Test getKeyRecursively
    test_function("getKeyRecursively", parser.getKeyRecursively, data, [])

    # 4. Test getValuesRecursively
    test_function("getValuesRecursively", parser.getValuesRecursively, data)

    # 5. Test getValsFromKey
    test_function("getValsFromKey", parser.getValsFromKey, data, key, [])

    # 6. Test checkIfValidHelm
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as file:
        file.write(yaml_text)
        file_path = file.name

    try:
        test_function("checkIfValidHelm", parser.checkIfValidHelm, file_path)
    finally:
        os.remove(file_path)

    # 7. Test find_json_path_keys
    test_function("find_json_path_keys", parser.find_json_path_keys, data)

    # 8. Test update_json_paths
    paths = random.choice([
        [],
        [f"{key}.{name}"],
        ["metadata.name", "spec.containers"],
        ["metadata.name", "metadata.name"],
        ["", "@#$%", "missing.path"]
    ])
    test_function("update_json_paths", parser.update_json_paths, paths)

    # 9. Test getSingleDict4MultiDocs
    documents = random.choice([
        [],
        [{"kind": "Pod"}],
        [{"kind": "Pod"}, {"kind": "Service"}],
        [data, {"name": name}],
        [{"kind": value, "id": random.randint(1, 100)}]
    ])
    test_function("getSingleDict4MultiDocs", parser.getSingleDict4MultiDocs, documents)

    # 10. Test constructHelmString
    helm_data = random.choice([
        ("chart", name, "values"),
        ("deployment", "", "templates"),
        ("service", name, ""),
        ("", "", "")
    ])
    test_function("constructHelmString", graphtaint.constructHelmString, helm_data)


# Save results
with open("fuzz_results.log", "w") as file:
    file.write("KubeSec Fuzzing Results\n")
    file.write("=======================\n")
    file.write("Random seed: 42\n")
    file.write(f"Tests executed: {tests_run}\n")
    file.write(f"Errors found: {len(errors)}\n\n")

    if errors:
        for error in errors:
            file.write(error + "\n")
    else:
        file.write("No errors detected.\n")


print(f"Tests executed: {tests_run}")
print(f"Errors found: {len(errors)}")
print("Results saved to fuzz_results.log")

if errors:
    exit(1)