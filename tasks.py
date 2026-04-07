EMAILS = [
    {"email_id":"e001","subject":"URGENT: Server down","body":"Production server down 30 minutes. Customers cannot access platform. Fix ASAP.","sender":"cto@company.com","timestamp":"2024-03-25 09:15:00"},
    {"email_id":"e002","subject":"Team lunch Friday","body":"Reminder about team lunch Friday 1pm. Let me know if you cannot make it.","sender":"manager@company.com","timestamp":"2024-03-25 10:00:00"},
    {"email_id":"e003","subject":"You won 1 million!","body":"Congratulations winner! Click here to claim prize. Provide bank details immediately.","sender":"prize@spam.net","timestamp":"2024-03-25 11:30:00"},
    {"email_id":"e004","subject":"Q1 Report review needed EOD","body":"Please review the Q1 financial report and send feedback. Schedule a call with finance team and update the dashboard with new numbers before end of day.","sender":"director@company.com","timestamp":"2024-03-25 08:00:00"},
    {"email_id":"e005","subject":"Client complaint urgent","body":"Dear Support, service outage yesterday cost my business 50000 dollars. I demand compensation and explanation within 24 hours or I take legal action.","sender":"client@bigcorp.com","timestamp":"2024-03-25 07:45:00"},
]

TASKS = {
    "task_1_classify":{"name":"task_1_classify","description":"Classify email urgency: urgent, normal, or spam","difficulty":"easy","email_ids":["e001","e002","e003"],"expected":{"e001":"urgent","e002":"normal","e003":"spam"}},
    "task_2_extract":{"name":"task_2_extract","description":"Extract all action items from the email","difficulty":"medium","email_ids":["e004"],"expected_keywords":[["review","report","q1"],["schedule","call","finance"],["update","dashboard"]]},
    "task_3_draft":{"name":"task_3_draft","description":"Draft a professional reply to the client complaint","difficulty":"hard","email_ids":["e005"]}
}

def get_email(eid):
    for e in EMAILS:
        if e["email_id"]==eid: return e
    return EMAILS[0]

def _clamp(score):
    # Strictly between 0 and 1 - never 0.0 or 1.0
    return round(max(0.01, min(0.99, float(score))), 4)

def grade_task_1(eid, cl):
    exp = TASKS["task_1_classify"]["expected"]
    if eid not in exp: return _clamp(0.1)
    if cl == exp[eid]: return _clamp(0.95)
    if exp[eid] in ["urgent","normal"] and cl in ["urgent","normal"]: return _clamp(0.3)
    return _clamp(0.05)

def grade_task_2(items):
    if not items: return _clamp(0.05)
    groups = TASKS["task_2_extract"]["expected_keywords"]
    score = 0.0
    low = [i.lower() for i in items]
    for g in groups:
        if any(any(k in item for k in g) for item in low):
            score += 1.0/len(groups)
    if len(items) > 8: score *= 0.8
    return _clamp(score if score > 0 else 0.05)

def grade_task_3(draft):
    if not draft or len(draft) < 50: return _clamp(0.05)
    d = draft.lower()
    kmap = {
        "apologize":["apologize","sorry","apologies"],
        "acknowledge":["acknowledge","understand","outage","downtime"],
        "resolve":["resolve","fix","address","investigate"],
        "compensation":["compensation","compensate","refund","credit"],
        "contact":["contact","reach","call","discuss"]
    }
    found = sum(1 for kws in kmap.values() if any(k in d for k in kws))
    score = found / len(kmap)
    if len(draft) > 200: score = min(score + 0.1, 0.99)
    if any(g in d for g in ["dear","hello","hi "]): score = min(score + 0.05, 0.99)
    return _clamp(score if score > 0 else 0.05)
