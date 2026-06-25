import os, json

ANGLE_LABELS = ["curiosity", "pain-point", "social proof", "direct-ask"]

try:
    inp = json.loads(os.environ.get("INPUT_JSON", "{}"))

    # --- Validate required inputs ---
    templates = inp.get("templates")
    if not templates or not isinstance(templates, list) or len(templates) == 0:
        raise ValueError("'templates' must be a non-empty list of message template strings.")

    first_name = inp.get("first_name", "").strip()
    if not first_name:
        raise ValueError("'first_name' is required.")

    title = inp.get("title", "").strip()
    company = inp.get("company", "").strip()

    last_variant_index = inp.get("last_variant_index", -1)
    if not isinstance(last_variant_index, int):
        raise ValueError("'last_variant_index' must be an integer (use -1 if no prior message sent).")

    # --- Select next variant in rotation ---
    num_templates = len(templates)
    new_variant_index = (last_variant_index + 1) % num_templates

    selected_template = templates[new_variant_index]
    if not isinstance(selected_template, str) or not selected_template.strip():
        raise ValueError(f"Template at index {new_variant_index} is empty or not a string.")

    # --- Token replacement (personalization) ---
    composed = selected_template
    composed = composed.replace("{{first_name}}", first_name)
    composed = composed.replace("{{title}}", title if title else "")
    composed = composed.replace("{{company}}", company if company else "")

    # --- Determine angle label (cycles through known labels, repeats if more templates than labels) ---
    angle = ANGLE_LABELS[new_variant_index % len(ANGLE_LABELS)]

    result = {
        "composed_message": composed,
        "new_variant_index": new_variant_index,
        "variant_angle": angle,
        "template_used_index": new_variant_index,
        "total_templates": num_templates,
        "prospect": {
            "first_name": first_name,
            "title": title,
            "company": company
        }
    }

    print(json.dumps(result))

except Exception as e:
    print(json.dumps({"error": str(e)}))