import csv
from agent import classify_node, search_node
from routing import after_classify

results = []


with open("eval_emails.csv", newline="", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        state = {"email_text": row["email"]}
        state.update(classify_node(state))

        if after_classify(state) == "emergency":
            route = "emergency"
        else:
            route = search_node(state)["route"]

        results.append({
            "email": row["email"],
            "expected_category": row["expected_category"],
            "got_category": state["category"],
            "expected_route": row["expected_route"],
            "got_route": route,
            "reason": state["reason"],
        })

total = len(results)
category_correct = sum(r["got_category"] == r["expected_category"] for r in results)
route_correct = sum(r["got_route"] == r["expected_route"] for r in results)

emergencies = [r for r in results if r["expected_route"] == "emergency"]
caught = sum(r["got_route"] == "emergency" for r in emergencies)
false_alarms = sum(r["got_route"] == "emergency" and r["expected_route"] != "emergency" for r in results)

print("\n=================== EVALUATION REPORT ===========================")
print(f"Emails tested:        {total}")
print(f"Emergency recall:     {caught}/{len(emergencies)} (must be 100%)")
print(f"False alarms:         {false_alarms}")
print(f"Category accuracy:    {category_correct}/{total} = {category_correct / total: .0%}")
print(f"Route accuracy:       {route_correct}/{total} = {route_correct / total:.0%}")


print("\n----------------- Mistakes ----------------------")
for r in results:
    if r["got_category"] != r["expected_category"] or r["got_route"] != r["expected_route"]:
        print(f"- {r['email'][:60]}")
        print(f" category: expected {r['expected_category']}, got {r['got_category']}")
        print(f" route:    expected {r['expected_route']}, got {r['got_route']}")
        print(f" reason:   expected {r['reason']}")


with open("eval_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
print("\nFull results saved to eval_results.csv")