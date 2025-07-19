import json
from tkinter import Tk, filedialog

def force_purchasable_minified_output():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select econ_gameplay_items.json",
        filetypes=[("JSON Files", "*.json")]
    )

    if not file_path:
        print("No file selected.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Failed to load JSON: {e}")
            return

    for item in data:
        item["isPurchasable"] = True
        item["price"] = 0

    output_path = file_path.replace(".json", "_modded_minified.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'))

    print(f"Saved minified, fully modded file to: {output_path}")

if __name__ == "__main__":
    force_purchasable_minified_output()
