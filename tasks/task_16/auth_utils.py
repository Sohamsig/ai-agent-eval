import base64
import hashlib
import hmac
import secrets


def hash_password(password):
    """
    Hash a password using PBKDF2-HMAC-SHA256.

    Returns a string containing:
    algorithm, iterations, salt, and derived key.
    """
    if not isinstance(password, str):
        return None

    if not password:
        return None

    salt = secrets.token_bytes(16)
    iterations = 100_000

    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )

    salt_encoded = base64.urlsafe_b64encode(
        salt
    ).decode("ascii")

    key_encoded = base64.urlsafe_b64encode(
        derived_key
    ).decode("ascii")

    return (
        f"pbkdf2_sha256${iterations}"
        f"${salt_encoded}"
        f"${key_encoded}"
    )


def verify_password(password, hashed_password):
    """
    Verify a plaintext password against a stored hash.
    """
    if not isinstance(password, str):
        return False

    if not isinstance(hashed_password, str):
        return False

    if not password or not hashed_password:
        return False

    try:
        parts = hashed_password.split("$")

        if len(parts) != 4:
            return False

        algorithm, iterations_text, salt_encoded, key_encoded = parts

        if algorithm != "pbkdf2_sha256":
            return False

        iterations = int(iterations_text)

        if iterations <= 0:
            return False

        salt = base64.urlsafe_b64decode(
            salt_encoded.encode("ascii")
        )

        expected_key = base64.urlsafe_b64decode(
            key_encoded.encode("ascii")
        )

        actual_key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
        )

        return hmac.compare_digest(
            actual_key,
            expected_key,
        )

    except (
        ValueError,
        TypeError,
        UnicodeError,
        base64.binascii.Error,
    ):
        return False


def generate_token(user_id):
    """
    Generate a simple signed token containing the user ID.

    Format:
        base64(user_id).signature
    """
    if user_id is None:
        return None

    user_id = str(user_id)

    if not user_id:
        return None

    secret = b"task16-secret-key"

    payload = base64.urlsafe_b64encode(
        user_id.encode("utf-8")
    ).decode("ascii")

    signature = hmac.new(
        secret,
        payload.encode("ascii"),
        hashlib.sha256,
    ).hexdigest()

    return f"{payload}.{signature}"


def validate_token(token):
    """
    Validate a generated token.

    Returns the original user ID when valid.
    Returns None when invalid.
    """
    if not isinstance(token, str):
        return None

    if not token:
        return None

    parts = token.split(".")

    if len(parts) != 2:
        return None

    payload, signature = parts

    if not payload or not signature:
        return None

    secret = b"task16-secret-key"

    expected_signature = hmac.new(
        secret,
        payload.encode("ascii"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(
        signature,
        expected_signature,
    ):
        return None

    try:
        user_id = base64.urlsafe_b64decode(
            payload.encode("ascii")
        ).decode("utf-8")

        if not user_id:
            return None

        return user_id

    except (
        ValueError,
        TypeError,
        UnicodeError,
        base64.binascii.Error,
    ):
        return None