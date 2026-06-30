def get_advisory_refusal() -> dict:
    message = (
        "I can only provide factual information about mutual fund schemes, "
        "such as expense ratios, exit loads, or SIP minimums. I'm unable to "
        "offer investment advice or recommendations. For investment guidance, "
        "visit AMFI (https://www.amfiindia.com/) or consult a SEBI-registered "
        "financial advisor."
    )
    return {
        "status": "success",
        "type": "refusal",
        "answer": message,
        "educational_link": "https://www.amfiindia.com/"
    }

def get_pii_refusal() -> dict:
    message = (
        "For your safety, I cannot process queries containing personal information like "
        "PAN, Aadhaar, or account numbers. Please remove any personal details and ask a "
        "factual question about mutual fund schemes."
    )
    return {
        "status": "success",
        "type": "refusal",
        "answer": message,
        "educational_link": None
    }

def get_no_context_refusal() -> dict:
    message = (
        "I don't have enough information in my sources to answer this question accurately. "
        "Please try rephrasing, or visit the fund page directly for details."
    )
    return {
        "status": "success",
        "type": "refusal",
        "answer": message,
        "educational_link": None
    }
