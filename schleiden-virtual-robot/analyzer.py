import yaml
import datetime

# ------------------------------------------------------------------------------
# Load database safely
# ------------------------------------------------------------------------------
def load_database(path="database.yaml"):
    """
    Loads the drug database YAML. Throws a readable error if bad.
    """
    try:
        with open(path, "r") as f:
            db = yaml.safe_load(f)
            return db if db else {}
    except FileNotFoundError:
        return None
    except yaml.YAMLError:
        raise Exception("❌ database.yaml is corrupted. Fix YAML syntax.")


# ------------------------------------------------------------------------------
# Core analyzer logic
# ------------------------------------------------------------------------------
def analyze_drug(drug_name, manufacturer, mfg_date=None, exp_date=None):
    """
    High-level drug analysis:
    - Is drug in database?
    - Is manufacturer trusted?
    - Are dates valid?
    """

    response = {
        "drug_name": drug_name.lower(),
        "manufacturer": manufacturer.lower(),
        "issues": [],
        "risk_score": 0,
        "verdict": "Unknown"
    }

    # Load DB
    db = load_database()
    if db is None:
        response["issues"].append("database.yaml missing!")
        response["risk_score"] = 100
        response["verdict"] = "System Error"
        return response

    drug_name = drug_name.lower().strip()
    manufacturer = manufacturer.lower().strip()

    # ------------------------------------------------------------------------------
    # 1. Check if drug exists
    # ------------------------------------------------------------------------------
    if drug_name not in db:
        response["issues"].append("Drug not found in trusted database.")
        response["risk_score"] += 70

        # Suggest closest match
        suggested = _closest_match(drug_name, list(db.keys()))
        if suggested:
            response["issues"].append(f"Did you mean: '{suggested}'?")

        response["verdict"] = "High Risk Fake"
        return response

    # ------------------------------------------------------------------------------
    # 2. Check manufacturer authenticity
    # ------------------------------------------------------------------------------
    allowed = db[drug_name].get("safe_manufacturers", [])

    if manufacturer not in allowed:
        response["issues"].append(f"Manufacturer '{manufacturer}' not trusted.")
        response["risk_score"] += 40
    else:
        response["issues"].append("Manufacturer verified ✔")

    # ------------------------------------------------------------------------------
    # 3. Validate dates (if provided)
    # ------------------------------------------------------------------------------
    if mfg_date and exp_date:
        mfg_valid = _validate_date(mfg_date)
        exp_valid = _validate_date(exp_date)

        if not mfg_valid:
            response["issues"].append("Invalid manufacturing date format.")
            response["risk_score"] += 10

        if not exp_valid:
            response["issues"].append("Invalid expiry date format.")
            response["risk_score"] += 10

        elif exp_valid and mfg_valid:
            if exp_date < mfg_date:
                response["issues"].append("Expiry date occurs BEFORE manufacturing date!!")
                response["risk_score"] += 50

            # Check if expired
            if datetime.date.today() > exp_date:
                response["issues"].append("Drug is EXPIRED.")
                response["risk_score"] += 60

    # ------------------------------------------------------------------------------
    # 4. Final Verdict
    # ------------------------------------------------------------------------------
    if response["risk_score"] == 0:
        response["verdict"] = "Likely Genuine"
    elif response["risk_score"] < 40:
        response["verdict"] = "Possibly Genuine"
    elif response["risk_score"] < 70:
        response["verdict"] = "Suspicious"
    else:
        response["verdict"] = "High Risk Fake"

    return response


# ------------------------------------------------------------------------------
# Helper 1: Find closest drug name
# ------------------------------------------------------------------------------
def _closest_match(word, word_list):
    """
    Suggest closest drug name. You don't need external libraries.
    Very clean Levenshtein-based similarity.
    """
    word = word.lower()
    best = None
    best_score = 999

    for w in word_list:
        score = _levenshtein(word, w)
        if score < best_score:
            best_score = score
            best = w

    return best if best_score <= 3 else None


# ------------------------------------------------------------------------------
# Helper 2: Levenshtein distance
# ------------------------------------------------------------------------------
def _levenshtein(a, b):
    """
    Pure Python edit distance. Fast enough for short drug names.
    """
    if len(a) > len(b):
        a, b = b, a

    distances = range(len(a) + 1)
    for i2, c2 in enumerate(b):
        new_dist = [i2 + 1]
        for i1, c1 in enumerate(a):
            if c1 == c2:
                new_dist.append(distances[i1])
            else:
                new_dist.append(
                    1 + min(distances[i1], distances[i1 + 1], new_dist[-1])
                )
        distances = new_dist

    return distances[-1]


# ------------------------------------------------------------------------------
# Helper 3: validate YYYY-MM-DD safely
# ------------------------------------------------------------------------------
def _validate_date(date_string):
    try:
        year, month, day = [int(x) for x in date_string.split("-")]
        return datetime.date(year, month, day)
    except:
        return None
