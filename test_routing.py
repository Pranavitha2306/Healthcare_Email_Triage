from routing import after_classify, after_search


def test_red_flag_words_force_emergency():
    state = {"email_text": "I have severe chest pain, can I book a cardiologist?",
             "priority": "Medium", "category": "Appointment"}
    assert after_classify(state) == "emergency"


def test_billing_question_goes_to_search():
    state = {"email_text": "Can I set up a payment plan for my bill?",
             "priority": "Low", "category": "Billing"}
    assert after_classify(state) == "search"


def test_no_documents_goes_to_fallback():
    assert after_search({"route": "no_documents"}) == "fallback"