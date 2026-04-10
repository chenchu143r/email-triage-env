EMAILS = [
    {"email_id":"e001","subject":"URGENT: Production server down","body":"Our production server has been down for 30 minutes. Customers cannot access the platform. Revenue loss is occurring. Need immediate fix. Please escalate to on-call engineer now.","sender":"cto@company.com","timestamp":"2024-03-25 09:15:00"},
    {"email_id":"e002","subject":"Team lunch this Friday","body":"Hey everyone, reminder about our team lunch this Friday at 1pm at The Grand Hotel. Please RSVP by Thursday. Let me know if you have dietary restrictions.","sender":"manager@company.com","timestamp":"2024-03-25 10:00:00"},
    {"email_id":"e003","subject":"Congratulations! You won 1 million dollars","body":"You have been selected as our lucky winner! Click here immediately to claim your prize money. Provide your bank account details and SSN to receive funds today!","sender":"prize@suspicious-domain.net","timestamp":"2024-03-25 11:30:00"},
    {"email_id":"e004","subject":"Q1 Report review needed by EOD","body":"Hi, I need you to review the Q1 financial report attached and send your feedback before end of day. Also please schedule a call with the finance team for Wednesday and update the project dashboard with the new quarterly numbers.","sender":"director@company.com","timestamp":"2024-03-25 08:00:00"},
    {"email_id":"e005","subject":"Client complaint - service outage","body":"Dear Support, I am writing to formally complain about the service outage yesterday that cost my business 50000 dollars. I demand written explanation and compensation within 24 hours or I will pursue legal action.","sender":"angry.client@bigcorp.com","timestamp":"2024-03-25 07:45:00"},
    {"email_id":"e006","subject":"CRITICAL: Security breach detected","body":"Security team has detected unauthorized access to customer database. Immediate action required. Lock down all admin accounts, notify legal team, and prepare incident report. This is a P0 incident.","sender":"security@company.com","timestamp":"2024-03-25 06:00:00"},
    {"email_id":"e007","subject":"Monthly newsletter March 2024","body":"Welcome to our monthly newsletter! This month we launched three new features, grew our team by 5 people, and attended two industry conferences. Read on for more updates.","sender":"newsletter@company.com","timestamp":"2024-03-25 08:00:00"},
    {"email_id":"e008","subject":"FREE iPhone 15 Limited offer","body":"Act now! You qualify for a FREE iPhone 15! Just pay 5 dollars shipping. Click this link and enter your credit card details. Offer expires in 1 hour!","sender":"offers@totally-legit.biz","timestamp":"2024-03-25 09:00:00"},
    {"email_id":"e009","subject":"Project Alpha deliverables overdue","body":"The Project Alpha deliverables were due yesterday. Please submit the design mockups, update the project timeline in Jira, send status report to stakeholders, and book a review meeting with the client this week.","sender":"pm@company.com","timestamp":"2024-03-25 09:30:00"},
    {"email_id":"e010","subject":"Vendor contract renewal complaint","body":"Dear Account Manager, we have been your customer for 5 years and are extremely disappointed with the recent 40 percent price increase with no prior notice. We demand an explanation, a revised quote, and a dedicated account manager assigned immediately.","sender":"procurement@enterprise-client.com","timestamp":"2024-03-25 10:15:00"},
]

TASKS = {
    "task_1_classify": {
        "name":"task_1_classify",
        "description":"Classify each email urgency as urgent, normal, or spam based on subject, body and sender.",
        "difficulty":"easy",
        "email_ids":["e001","e002","e003","e006","e007","e008"],
        "expected":{"e001":"urgent","e002":"normal","e003":"spam","e006":"urgent","e007":"normal","e008":"spam"}
    },
    "task_2_extract": {
        "name":"task_2_extract",
        "description":"Extract all concrete action items the recipient must complete including deadlines.",
        "difficulty":"medium",
        "email_ids":["e004","e009"],
        "expected_keywords":[["review","report","q1"],["schedule","call","finance"],["update","dashboard"],["submit","mockups"],["update","jira","timeline"],["send","status","stakeholders"],["book","meeting","client"]]
    },
    "task_3_draft": {
        "name":"task_3_draft",
        "description":"Draft professional empathetic reply acknowledging issue, apologizing, explaining next steps, offering compensation and contact info.",
        "difficulty":"hard",
        "email_ids":["e005","e010"]
    }
}

def get_email(eid):
    for e in EMAILS:
        if e["email_id"]==eid: return e
    return EMAILS[0]

def _clamp(score):
    return round(max(0.01, min(0.99, float(score))), 4)

def grade_task_1(eid, cl):
    exp = TASKS["task_1_classify"]["expected"]
    if eid not in exp: return _clamp(0.1)
    if cl == exp[eid]: return _clamp(0.95)
    if exp[eid] in ["urgent","normal"] and cl in ["urgent","normal"]: return _clamp(0.35)
    return _clamp(0.05)

def grade_task_2(items):
    if not items: return _clamp(0.05)
    groups = TASKS["task_2_extract"]["expected_keywords"]
    score = 0.0
    low = [i.lower() for i in items]
    for g in groups:
        if any(any(k in item for k in g) for item in low):
            score += 1.0/len(groups)
    if len(items) > 10: score *= 0.85
    if len(items) < 2: score *= 0.5
    return _clamp(score if score > 0 else 0.05)

def grade_task_3(draft):
    if not draft or len(draft) < 80: return _clamp(0.05)
    d = draft.lower()
    kmap = {
        "apologize":["apologize","sorry","apologies","regret"],
        "acknowledge":["acknowledge","understand","aware","outage","disruption","loss"],
        "resolve":["resolve","fix","address","investigate","committed"],
        "compensation":["compensation","compensate","refund","credit","remedy"],
        "contact":["contact","reach","call","email","discuss","dedicated"],
        "timeline":["24 hours","immediately","promptly","within","today"]
    }
    found = sum(1 for kws in kmap.values() if any(k in d for k in kws))
    score = found/len(kmap)
    if len(draft)>250: score=min(score+0.08,0.97)
    if any(g in d for g in ["dear","hello","hi "]): score=min(score+0.04,0.97)
    if any(g in d for g in ["sincerely","regards","best regards"]): score=min(score+0.04,0.97)
    return _clamp(score if score > 0 else 0.05)
