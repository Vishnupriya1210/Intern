import math
import string

# Common/leaked password list (can be expanded or loaded from a file)
COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123",
    "pass1234", "admin", "letmein", "welcome", "monkey"
}


def calculate_entropy(password: str) -> float:
    """Calculate password entropy in bits based on character pool size and length."""
    if not password:
        return 0.0

    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += 32

    if pool == 0:
        return 0.0

    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)


def score_password(password: str) -> dict:
    """Evaluate password length, entropy, and rule-based score."""
    length = len(password)
    entropy = calculate_entropy(password)
    score = 0

    # Length scoring
    if length >= 12:
        score += 30
    elif length >= 8:
        score += 20
    elif length >= 4:
        score += 10

    # Character variety scoring (+10 points each)
    if any(c.islower() for c in password):
        score += 10
    if any(c.isupper() for c in password):
        score += 10
    if any(c.isdigit() for c in password):
        score += 10
    if any(c in string.punctuation for c in password):
        score += 15

    # Entropy bonus
    if entropy >= 60:
        score += 25
    elif entropy >= 40:
        score += 15

    # Common password check
    is_common = password.lower() in COMMON_PASSWORDS
    if is_common:
        score = min(score, 20)

    score = min(score, 100)

    # Strength rating
    if is_common or score < 40:
        strength = "Weak"
    elif score < 70:
        strength = "Moderate"
    else:
        strength = "Strong"

    return {
        "length": length,
        "entropy": entropy,
        "score": score,
        "strength": strength,
        "is_common": is_common,
    }


def main():
    print("=== Password Strength Checker ===")
    password = input("Enter a password to check: ")

    result = score_password(password)

    print("\n--- Password Analysis ---")
    print(f"Length:   {result['length']}")
    print(f"Entropy:  {result['entropy']} bits")
    print(f"Score:    {result['score']} / 100")
    print(f"Strength: {result['strength']}")
    if result["is_common"]:
        print("Warning:  This password is in the common password list!")


if __name__ == "__main__":
    main()
