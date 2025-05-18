def parse_output(output: str) -> tuple:
    sections = {
        "Thought": "None",
        "Response": "None",
        "Action": '{"name": "end"}'
    }

    keys = ["Thought", "Response", "Action"]
    positions = {}

    for key in keys:
        try:
            positions[key] = output.index(f"{key}:")
        except ValueError:
            positions[key] = -1

    sorted_keys = [k for k in keys if positions[k] != -1]
    sorted_keys.sort(key=lambda k: positions[k])

    for i, key in enumerate(sorted_keys):
        start = positions[key] + len(key) + 1
        end = positions[sorted_keys[i + 1]] if i + 1 < len(sorted_keys) else len(output)
        sections[key] = output[start:end].strip()
    return sections["Thought"], sections["Response"], sections["Action"]
