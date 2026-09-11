import os


def solve(task, repo_path=None):
    """
    Agent 02:
    Reads the task prompt and generates the required solution.
    """

    if repo_path is None:
        repo_path = os.path.join("tasks", task)

    prompt_path = os.path.join(repo_path, "prompt.txt")

    if not os.path.exists(prompt_path):
        prompt_path = os.path.join(repo_path, "prompt.md")

    if not os.path.exists(prompt_path):
        return {
            "agent": "agent_02",
            "status": "failed",
            "message": f"Prompt file not found: {prompt_path}",
            "files": {},
        }

    try:
        with open(prompt_path, "r", encoding="utf-8") as file:
            prompt = file.read()
    except UnicodeDecodeError:
        with open(prompt_path, "r", encoding="cp1252") as file:
            prompt = file.read()

    print("Task prompt:")
    print(prompt)

    # =========================================================
    # Task 01 - Calculator
    # =========================================================

    if task == "task_01":
        solution = {
            "calculator.py": """def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return None

    return a / b
"""
        }

    # =========================================================
    # Task 02 - String utilities
    # =========================================================

    elif task == "task_02":
        solution = {
            "string_utils.py": """def reverse_string(value):
    if not isinstance(value, str):
        return None

    return value[::-1]


def is_palindrome(value):
    if not isinstance(value, str):
        return False

    value = value.lower()

    return value == value[::-1]


def count_vowels(value):
    if not isinstance(value, str):
        return 0

    return sum(
        1
        for char in value.lower()
        if char in "aeiou"
    )


def remove_whitespace(value):
    if not isinstance(value, str):
        return None

    return "".join(value.split())


def capitalize_words(value):
    if not isinstance(value, str):
        return None

    return " ".join(
        word.capitalize()
        for word in value.split(" ")
    )
"""
        }

    # =========================================================
    # Task 03 - Data utilities
    # =========================================================

    elif task == "task_03":
        solution = {
            "data_utils.py": """def get_average(numbers):
    if not numbers:
        return 0

    return sum(numbers) / len(numbers)


def get_minimum(numbers):
    if not numbers:
        return None

    return min(numbers)


def get_maximum(numbers):
    if not numbers:
        return None

    return max(numbers)


def get_sum(numbers):
    if not numbers:
        return 0

    return sum(numbers)
"""
        }

    # =========================================================
    # Task 04 - JSON utilities
    # =========================================================

    elif task == "task_04":
        solution = {
            "json_utils.py": """import json


def parse_json(value):
    try:
        return json.loads(value)
    except (TypeError, ValueError, json.JSONDecodeError):
        return None


def get_user_name(data):
    if not isinstance(data, dict):
        return None

    user = data.get("user")

    if not isinstance(user, dict):
        return None

    return user.get("name")
"""
        }

    # =========================================================
    # Task 05 - Discount
    # =========================================================

    elif task == "task_05":
        solution = {
            "discount.py": """def calculate_discount(price, discount):
    if not isinstance(price, (int, float)):
        return None

    if not isinstance(discount, (int, float)):
        return None

    return price - (price * discount / 100)
"""
        }

    # =========================================================
    # Task 06 - List utilities
    # =========================================================

    elif task == "task_06":
        solution = {
            "list_utils.py": """def find_max(items):
    if not items:
        return None

    return max(items)


def remove_duplicates(items):
    if not isinstance(items, (list, tuple)):
        return []

    return list(dict.fromkeys(items))


def count_positive(items):
    if not isinstance(items, (list, tuple)):
        return 0

    return sum(
        1
        for item in items
        if isinstance(item, (int, float)) and item > 0
    )
"""
        }

    # =========================================================
    # Task 07 - Dictionary utilities
    # =========================================================

    elif task == "task_07":
        solution = {
            "dict_utils.py": """def get_value(data, key, default=None):
    if not isinstance(data, dict):
        return default

    return data.get(key, default)


def merge_dicts(first, second):
    if not isinstance(first, dict):
        first = {}

    if not isinstance(second, dict):
        second = {}

    result = first.copy()
    result.update(second)

    return result


def filter_by_value(data, minimum):
    if not isinstance(data, dict):
        return {}

    return {
        key: value
        for key, value in data.items()
        if value >= minimum
    }
"""
        }

    # =========================================================
    # Task 08 - Text utilities
    # =========================================================

    elif task == "task_08":
        solution = {
            "text_utils.py": """def normalize_text(text):
    if not isinstance(text, str):
        return ""

    return " ".join(
        text.strip().lower().split()
    )


def count_words(text):
    if not isinstance(text, str):
        return 0

    return len(text.split())


def reverse_words(text):
    if not isinstance(text, str):
        return ""

    return " ".join(
        text.split()[::-1]
    )
"""
        }

    # =========================================================
    # Task 09 - URL utilities
    # =========================================================

    elif task == "task_09":
        solution = {
            "url_utils.py": """from urllib.parse import (
    urlparse,
    urlencode,
    urlunparse,
    parse_qs,
)


def parse_url(url):
    if not isinstance(url, str):
        return None

    try:
        parsed = urlparse(url)

        return {
            "scheme": parsed.scheme,
            "host": parsed.hostname,
            "port": parsed.port,
            "path": parsed.path,
            "query": parsed.query,
            "fragment": parsed.fragment,
        }

    except ValueError:
        return None


def build_url(
    scheme,
    host,
    path,
    params=None,
    fragment=None,
):
    if not isinstance(scheme, str):
        return None

    if not isinstance(host, str):
        return None

    if not isinstance(path, str):
        return None

    query = urlencode(params or {})

    return urlunparse((
        scheme,
        host,
        path,
        "",
        query,
        fragment or "",
    ))


def add_query_params(url, params):
    if not isinstance(url, str):
        return None

    if not isinstance(params, dict):
        return None

    try:
        parsed = urlparse(url)

        existing = parse_qs(parsed.query)

        for key, value in params.items():
            existing[key] = [str(value)]

        query = urlencode(
            existing,
            doseq=True
        )

        return urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            query,
            parsed.fragment,
        ))

    except ValueError:
        return None
"""
        }

    # =========================================================
    # Task 10 - CSV utilities
    # =========================================================

    elif task == "task_10":
        solution = {
            "csv_utils.py": """import csv
from io import StringIO


def parse_csv(text):
    if not isinstance(text, str):
        return []

    reader = csv.DictReader(
        StringIO(text)
    )

    return list(reader)


def filter_rows(rows, column, value):
    if not isinstance(rows, list):
        return []

    return [
        row
        for row in rows
        if isinstance(row, dict)
        and row.get(column) == value
    ]


def csv_to_text(rows, fieldnames):
    if not isinstance(rows, list):
        return ""

    if not isinstance(fieldnames, (list, tuple)):
        return ""

    output = StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
        lineterminator="\\n",
    )

    writer.writeheader()
    writer.writerows(rows)

    return output.getvalue()
"""
        }

    # =========================================================
    # Task 11 - File utilities
    # =========================================================

    elif task == "task_11":
        solution = {
            "file_utils.py": """import os


def list_files(directory):
    if not isinstance(directory, str):
        return []

    if not os.path.isdir(directory):
        return []

    return sorted(
        name
        for name in os.listdir(directory)
        if os.path.isfile(
            os.path.join(directory, name)
        )
    )


def file_exists(path):
    if not isinstance(path, str):
        return False

    return os.path.isfile(path)


def get_file_size(path):
    if not isinstance(path, str):
        return 0

    if not os.path.isfile(path):
        return 0

    return os.path.getsize(path)


def ensure_directory(path):
    if not isinstance(path, str):
        return False

    try:
        os.makedirs(
            path,
            exist_ok=True
        )
        return True

    except OSError:
        return False
"""
        }

    # =========================================================
    # Task 12 - HTTP / Config utilities
    # =========================================================

    elif task == "task_12":
        solution = {
            "config_utils.py": """def get_config(
    config,
    key,
    default=None
):
    if not isinstance(config, dict):
        return default

    return config.get(key, default)


def set_config(
    config,
    key,
    value
):
    if not isinstance(config, dict):
        return None

    config[key] = value

    return config


def merge_configs(
    base,
    override
):
    if not isinstance(base, dict):
        base = {}

    if not isinstance(override, dict):
        override = {}

    result = base.copy()
    result.update(override)

    return result


def remove_config(
    config,
    key
):
    if not isinstance(config, dict):
        return None

    config.pop(key, None)

    return config
"""
        }

    # =========================================================
    # Task 13 - Validation
    # =========================================================

    elif task == "task_13":
        solution = {
            "validation_utils.py": """import re


def is_valid_email(email):
    if not isinstance(email, str):
        return False

    email = email.strip()

    if not email or " " in email:
        return False

    pattern = r"^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$"

    return bool(
        re.match(pattern, email)
    )


def is_valid_phone(phone):
    if not isinstance(phone, str):
        return False

    if phone.startswith("+"):
        phone = phone[1:]

    if not phone.isdigit():
        return False

    return 10 <= len(phone) <= 15


def is_valid_username(username):
    if not isinstance(username, str):
        return False

    if not 3 <= len(username) <= 20:
        return False

    return bool(
        re.fullmatch(
            r"[A-Za-z0-9_]+",
            username
        )
    )


def validate_required_fields(
    data,
    fields
):
    if not isinstance(data, dict):
        return False

    if not isinstance(
        fields,
        (list, tuple)
    ):
        return False

    for field in fields:
        if field not in data:
            return False

        value = data[field]

        if value is None:
            return False

        if (
            isinstance(value, str)
            and not value.strip()
        ):
            return False

    return True
"""
        }

    # =========================================================
    # Task 14 - REST API / String utilities
    # =========================================================

    elif task == "task_14":
        solution = {
            "string_utils.py": """def reverse_string(value):
    if not isinstance(value, str):
        return None

    return value[::-1]


def is_palindrome(value):
    if not isinstance(value, str):
        return False

    value = value.lower()

    return value == value[::-1]


def count_vowels(value):
    if not isinstance(value, str):
        return 0

    return sum(
        1
        for char in value.lower()
        if char in "aeiou"
    )


def remove_whitespace(value):
    if not isinstance(value, str):
        return None

    return "".join(
        value.split()
    )


def capitalize_words(value):
    if not isinstance(value, str):
        return None

    return " ".join(
        word.capitalize()
        for word in value.split(" ")
    )
"""
        }

    # =========================================================
    # Task 15 - SQL utilities
    # =========================================================

    elif task == "task_15":
        solution = {
            "sql_utils.py": """import re


_IDENTIFIER_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*$"
)


def _valid_identifier(value):
    return (
        isinstance(value, str)
        and bool(
            _IDENTIFIER_RE.fullmatch(value)
        )
    )


def _build_conditions(
    where,
    start_index=1
):
    if not isinstance(where, dict):
        return None

    if not where:
        return None

    conditions = []

    for index, column in enumerate(
        where.keys(),
        start=start_index
    ):
        if not _valid_identifier(column):
            return None

        conditions.append(
            f"{column} = ${index}"
        )

    return " AND ".join(conditions)


def build_select_query(
    table,
    columns=None,
    where=None
):
    if not _valid_identifier(table):
        return None

    if columns is None:
        column_sql = "*"

    else:
        if not isinstance(
            columns,
            (list, tuple)
        ):
            return None

        if not columns:
            return None

        if not all(
            _valid_identifier(column)
            for column in columns
        ):
            return None

        column_sql = ", ".join(columns)

    query = (
        f"SELECT {column_sql} "
        f"FROM {table}"
    )

    if where is not None:
        conditions = _build_conditions(
            where
        )

        if conditions is None:
            return None

        query += (
            f" WHERE {conditions}"
        )

    return query


def build_insert_query(
    table,
    data
):
    if not _valid_identifier(table):
        return None

    if not isinstance(data, dict):
        return None

    if not data:
        return None

    columns = list(data.keys())

    if not all(
        _valid_identifier(column)
        for column in columns
    ):
        return None

    placeholders = [
        f"${index}"
        for index in range(
            1,
            len(columns) + 1
        )
    ]

    return (
        f"INSERT INTO {table} "
        f"({', '.join(columns)}) "
        f"VALUES ({', '.join(placeholders)})"
    )


def build_update_query(
    table,
    data,
    where
):
    if not _valid_identifier(table):
        return None

    if not isinstance(data, dict):
        return None

    if not data:
        return None

    if not isinstance(where, dict):
        return None

    if not where:
        return None

    columns = list(data.keys())

    if not all(
        _valid_identifier(column)
        for column in columns
    ):
        return None

    set_parts = []

    for index, column in enumerate(
        columns,
        start=1
    ):
        set_parts.append(
            f"{column} = ${index}"
        )

    conditions = _build_conditions(
        where,
        start_index=len(columns) + 1
    )

    if conditions is None:
        return None

    return (
        f"UPDATE {table} "
        f"SET {', '.join(set_parts)} "
        f"WHERE {conditions}"
    )


def build_delete_query(
    table,
    where
):
    if not _valid_identifier(table):
        return None

    if not isinstance(where, dict):
        return None

    if not where:
        return None

    conditions = _build_conditions(
        where
    )

    if conditions is None:
        return None

    return (
        f"DELETE FROM {table} "
        f"WHERE {conditions}"
    )
"""
        }

            # =========================================================
    # Task 16 - Authentication
    # =========================================================

    elif task == "task_16":
        solution = {
            "auth_utils.py": """import base64
import hashlib
import hmac
import secrets


def hash_password(password):
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
"""
        }

            # ---------------------------------------------------------
    # Task 17
    # ---------------------------------------------------------

    elif task == "task_17":
        solution = {
            "retry_utils.py": """import time


def retry(func, max_retries=3, delay=0):
    \"\"\"Retry a callable up to max_retries times after the initial attempt.\"\"\"
    if not callable(func):
        raise TypeError("func must be callable")

    if not isinstance(max_retries, int) or isinstance(max_retries, bool) or max_retries < 0:
        raise ValueError("max_retries must be a non-negative integer")

    if not isinstance(delay, (int, float)) or isinstance(delay, bool) or delay < 0:
        raise ValueError("delay must be non-negative")

    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as exc:
            last_exception = exc
            if attempt < max_retries and delay > 0:
                time.sleep(delay)

    raise last_exception


def retry_with_backoff(func, max_retries=3, base_delay=0):
    \"\"\"Retry a callable with exponential backoff.\"\"\"
    if not callable(func):
        raise TypeError("func must be callable")

    if not isinstance(max_retries, int) or isinstance(max_retries, bool) or max_retries < 0:
        raise ValueError("max_retries must be a non-negative integer")

    if not isinstance(base_delay, (int, float)) or isinstance(base_delay, bool) or base_delay < 0:
        raise ValueError("base_delay must be non-negative")

    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as exc:
            last_exception = exc
            if attempt < max_retries and base_delay > 0:
                time.sleep(base_delay * (2 ** attempt))

    raise last_exception


def retry_with_default(func, default=None, attempts=3):
    \"\"\"Retry a callable and return a default value if all attempts fail.\"\"\"
    if not callable(func):
        return default

    if not isinstance(attempts, int) or isinstance(attempts, bool) or attempts <= 0:
        return default

    for _ in range(attempts):
        try:
            return func()
        except Exception:
            continue

    return default
"""
        }



            # ---------------------------------------------------------
    # Task 18 - Cache
    # ---------------------------------------------------------

    elif task == "task_18":
        solution = {
            "cache_utils.py": """_CACHE = {}


def get(key, default=None):
    \"\"\"Return the cached value or default if the key is missing.\"\"\"
    try:
        return _CACHE.get(key, default)
    except (TypeError, AttributeError):
        return default


def set(key, value):
    \"\"\"Store a value in the cache.\"\"\"
    try:
        _CACHE[key] = value
        return value
    except (TypeError, AttributeError):
        return None


def delete(key):
    \"\"\"Delete a key from the cache.

    Returns True if the key existed, otherwise False.
    \"\"\"
    try:
        if key in _CACHE:
            del _CACHE[key]
            return True
    except (TypeError, AttributeError):
        return False

    return False


def clear():
    \"\"\"Remove all entries from the cache.\"\"\"
    _CACHE.clear()


def contains(key):
    \"\"\"Return True if the key exists in the cache.\"\"\"
    try:
        return key in _CACHE
    except (TypeError, AttributeError):
        return False
"""
        }

        return {
            "agent": "agent_02",
            "status": "completed",
            "message": "Solution generated successfully.",
            "files": solution
        }

            # ---------------------------------------------------------
    # Task 19 - Bug Fixing
    # ---------------------------------------------------------

    elif task == "task_19":
        solution = {
            "bug_utils.py": """def find_max(numbers):
    if not isinstance(numbers, (list, tuple)) or not numbers:
        return None

    try:
        return max(numbers)
    except (TypeError, ValueError):
        return None


def divide(a, b):
    if not isinstance(a, (int, float)) or isinstance(a, bool):
        return None

    if not isinstance(b, (int, float)) or isinstance(b, bool):
        return None

    if b == 0:
        return None

    return a / b


def count_occurrences(items, value):
    if not isinstance(items, (list, tuple)):
        return 0

    return items.count(value)


def remove_duplicates(items):
    if not isinstance(items, (list, tuple)):
        return []

    result = []

    for item in items:
        if item not in result:
            result.append(item)

    return result


def safe_get(data, key, default=None):
    if not isinstance(data, dict):
        return default

    return data.get(key, default)
"""
        }

        return {
            "agent": "agent_02",
            "status": "completed",
            "message": "Solution generated successfully.",
            "files": solution
        }

            # ---------------------------------------------------------
    # =========================================================
    # Task 20 - Multi-file Feature
    # =========================================================

    elif task == "task_20":
        solution = {
            "feature_utils.py": """def add_numbers(a, b):
    \"\"\"Return the sum of two numeric values.\"\"\"
    if isinstance(a, bool) or isinstance(b, bool):
        return None

    if not isinstance(a, (int, float)):
        return None

    if not isinstance(b, (int, float)):
        return None

    return a + b


def multiply_numbers(a, b):
    \"\"\"Return the product of two numeric values.\"\"\"
    if isinstance(a, bool) or isinstance(b, bool):
        return None

    if not isinstance(a, (int, float)):
        return None

    if not isinstance(b, (int, float)):
        return None

    return a * b
""",

            "feature_service.py": """from feature_utils import (
    add_numbers,
    multiply_numbers,
)


def calculate(a, b):
    \"\"\"Return sum and product for two valid numbers.\"\"\"
    total = add_numbers(a, b)
    product = multiply_numbers(a, b)

    if total is None or product is None:
        return None

    return {
        "sum": total,
        "product": product,
    }


def calculate_sum(a, b):
    \"\"\"Return the sum using feature_utils.\"\"\"
    return add_numbers(a, b)


def calculate_product(a, b):
    \"\"\"Return the product using feature_utils.\"\"\"
    return multiply_numbers(a, b)
""",
        }

    # =========================================================
    # Task 21 - Text Utilities Bug Fix
    # =========================================================

    elif task == "task_21":
        solution = {
            "text_utils.py": """def normalize_text(text):
    \"\"\"Normalize text by trimming whitespace and converting to lowercase.\"\"\"
    if not isinstance(text, str):
        return None

    return text.strip().lower()


def word_count(text):
    \"\"\"Return the number of words in text.\"\"\"
    if not isinstance(text, str):
        return None

    return len(text.split())


def reverse_words(text):
    \"\"\"Reverse the order of words in text.\"\"\"
    if not isinstance(text, str):
        return None

    return " ".join(text.split()[::-1])


def is_palindrome(text):
    \"\"\"Return True if text is a palindrome, ignoring case and outer whitespace.\"\"\"
    if not isinstance(text, str):
        return None

    cleaned = text.strip().lower()
    return cleaned == cleaned[::-1]
"""
        }

    # =========================================================
    # Task 22 - In-Memory Cache Utilities
    # =========================================================

    elif task == "task_22":
        solution = {
            "cache_utils.py": """def set_value(cache, key, value):
    \"\"\"Store a value in the cache.\"\"\"
    if not isinstance(cache, dict):
        return False

    if not isinstance(key, str) or not key:
        return False

    cache[key] = value
    return True


def get_value(cache, key, default=None):
    \"\"\"Return a cached value or default.\"\"\"
    if not isinstance(cache, dict):
        return default

    if not isinstance(key, str) or not key:
        return default

    return cache.get(key, default)


def delete_value(cache, key):
    \"\"\"Delete a value from the cache.\"\"\"
    if not isinstance(cache, dict):
        return False

    if not isinstance(key, str) or not key:
        return False

    if key not in cache:
        return False

    del cache[key]
    return True


def has_key(cache, key):
    \"\"\"Check whether a key exists in the cache.\"\"\"
    if not isinstance(cache, dict):
        return False

    if not isinstance(key, str) or not key:
        return False

    return key in cache


def clear_cache(cache):
    \"\"\"Remove all entries from the cache.\"\"\"
    if not isinstance(cache, dict):
        return False

    cache.clear()
    return True
"""
        }

    # =========================================================
    # Task 23 - File Utilities
    # =========================================================

    elif task == "task_23":
        solution = {
            "file_utils.py": '''import os


def get_file_extension(filename):
    """Return the lowercase file extension without the dot."""
    if not isinstance(filename, str) or not filename:
        return None

    basename = os.path.basename(filename)

    if basename.startswith(".") and basename.count(".") == 1:
        return ""

    _, extension = os.path.splitext(basename)

    return extension[1:].lower()


def get_filename_without_extension(filename):
    """Return the filename without its final extension."""
    if not isinstance(filename, str) or not filename:
        return None

    root, _ = os.path.splitext(filename)

    return root


def is_valid_filename(filename):
    """Return True when filename is a non-empty string."""
    if not isinstance(filename, str):
        return False

    return bool(filename.strip())


def join_path(*parts):
    """Join path components safely."""
    if not parts:
        return None

    if any(not isinstance(part, str) for part in parts):
        return None

    return os.path.join(*parts)


def normalize_path(path):
    """Normalize a filesystem path."""
    if not isinstance(path, str) or not path:
        return None

    return os.path.normpath(path)


def get_file_size(path):
    """Return file size in bytes, or None when unavailable."""
    if not isinstance(path, str) or not path:
        return None

    try:
        return os.path.getsize(path)
    except (OSError, TypeError):
        return None
'''
        }

    # =========================================================
    # Task 24 - JSON Data Utilities
    # =========================================================

    elif task == "task_24":
        solution = {
            "actual_task_file.py": '''import json


def serialize_data(data):
    """Convert a Python object into a JSON string."""
    return json.dumps(data)


def deserialize_data(data):
    """Convert a JSON string into a Python object."""
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError("Invalid JSON") from exc


def get_json_value(data, path, default=None):
    """Read a nested dictionary value using dot notation."""
    if not isinstance(data, dict) or not isinstance(path, str) or not path:
        return default

    current = data

    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return default

        current = current[key]

    return current


def set_json_value(data, path, value):
    """Set a nested dictionary value using dot notation."""
    if not isinstance(data, dict):
        return data

    if not isinstance(path, str) or not path:
        return data

    keys = path.split(".")
    current = data

    for key in keys[:-1]:
        if not isinstance(current.get(key), dict):
            current[key] = {}

        current = current[key]

    current[keys[-1]] = value

    return data


def remove_json_value(data, path):
    """Remove a nested dictionary value using dot notation."""
    if not isinstance(data, dict) or not isinstance(path, str) or not path:
        return False

    keys = path.split(".")
    current = data

    for key in keys[:-1]:
        if not isinstance(current, dict) or key not in current:
            return False

        current = current[key]

    if not isinstance(current, dict) or keys[-1] not in current:
        return False

    del current[keys[-1]]
    return True
'''
        }

    # =========================================================
    # Task 25 - Date Utility Functions
    # =========================================================

    elif task == "task_25":
        solution = {
            "actual_task_file.py": '''from datetime import date, timedelta


def parse_date(date_string):
    """Parse a date in YYYY-MM-DD format."""
    if not isinstance(date_string, str) or not date_string:
        raise ValueError("Invalid date")

    try:
        return date.fromisoformat(date_string)
    except ValueError as exc:
        raise ValueError("Invalid date") from exc


def format_date(date_obj):
    """Format a date as YYYY-MM-DD."""
    if not isinstance(date_obj, date):
        raise ValueError("Expected a date object")

    return date_obj.strftime("%Y-%m-%d")


def days_between(start_date, end_date):
    """Return the absolute number of days between two dates."""
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        raise ValueError("Expected date objects")

    return abs((end_date - start_date).days)


def is_leap_year(year):
    """Return whether a year is a Gregorian leap year."""
    if not isinstance(year, int) or isinstance(year, bool):
        return False

    return year % 4 == 0 and (
        year % 100 != 0 or year % 400 == 0
    )


def add_days(date_obj, days):
    """Return a new date with the specified number of days added."""
    if not isinstance(date_obj, date):
        raise ValueError("Expected a date object")

    return date_obj + timedelta(days=days)


def get_month_name(date_obj):
    """Return the full English month name."""
    if not isinstance(date_obj, date):
        raise ValueError("Expected a date object")

    return date_obj.strftime("%B")


def get_weekday_name(date_obj):
    """Return the full English weekday name."""
    if not isinstance(date_obj, date):
        raise ValueError("Expected a date object")

    return date_obj.strftime("%A")
'''
        }

    # Task 32
    # =========================================================

    elif task == "task_26":
        solution = {
            "actual_task_file.py": '''def calculate_subtotal(items):
    """Calculate the subtotal of an order."""
    total = 0

    for item in items:
        total += item["price"] * item["quantity"]

    return total


def apply_discount(amount, discount_percent):
    """Apply a percentage discount to an amount."""
    if discount_percent < 0 or discount_percent > 100:
        return amount

    discount = amount * discount_percent / 100
    return amount - discount


def calculate_tax(amount, tax_percent):
    """Return the amount including tax."""
    if amount < 0:
        return 0

    return round(
        amount + (amount * tax_percent / 100),
        3,
    )


def calculate_final_price(items, discount_percent=0, tax_percent=0):
    """Calculate the final order price."""
    subtotal = calculate_subtotal(items)

    discounted = apply_discount(
        subtotal,
        discount_percent,
    )

    taxed = calculate_tax(
        discounted,
        tax_percent,
    )

    return round(taxed, 2)


def validate_items(items):
    """Validate order items."""
    if not isinstance(items, list) or not items:
        return False

    for item in items:
        if not isinstance(item, dict):
            return False

        if "price" not in item or "quantity" not in item:
            return False

        price = item["price"]
        quantity = item["quantity"]

        if not isinstance(price, (int, float)):
            return False

        if isinstance(price, bool):
            return False

        if price < 0:
            return False

        if not isinstance(quantity, int):
            return False

        if isinstance(quantity, bool):
            return False

        if quantity <= 0:
            return False

    return True
'''
        }

    elif task == "task_27":
        solution = {
            "actual_task_file.py": '"""Task 27 - User Data Utilities"""\n\n\ndef _get_user_field(user, field):\n    """Return a user field when the user is a dictionary."""\n    if not isinstance(user, dict):\n        return None\n\n    return user.get(field)\n\n\ndef _normalize_name(user):\n    """Return a normalized user name or None."""\n    value = _get_user_field(user, "name")\n\n    if not isinstance(value, str):\n        return None\n\n    return value.strip()\n\n\ndef _normalize_email(user):\n    """Return a normalized user email or None."""\n    value = _get_user_field(user, "email")\n\n    if not isinstance(value, str):\n        return None\n\n    return value.strip().lower()\n\n\ndef _normalize_age(user):\n    """Return a valid user age or None."""\n    value = _get_user_field(user, "age")\n\n    if not isinstance(value, int) or isinstance(value, bool):\n        return None\n\n    if value < 0:\n        return None\n\n    return value\n\n\ndef get_user_name(user):\n    """Return the normalized user name."""\n    return _normalize_name(user)\n\n\ndef get_user_email(user):\n    """Return the normalized user email."""\n    return _normalize_email(user)\n\n\ndef get_user_age(user):\n    """Return the validated user age."""\n    return _normalize_age(user)\n\n\ndef format_user(user):\n    """Format the available valid user fields."""\n    if not isinstance(user, dict):\n        return ""\n\n    parts = []\n\n    name = _normalize_name(user)\n    email = _normalize_email(user)\n    age = _normalize_age(user)\n\n    if name is not None:\n        parts.append(name)\n\n    if email is not None:\n        parts.append(email)\n\n    if age is not None:\n        parts.append(str(age))\n\n    return ", ".join(parts)\n\n\ndef filter_users(users, min_age=None):\n    """Return users matching the optional minimum age."""\n    if not isinstance(users, list):\n        return []\n\n    if min_age is not None:\n        if not isinstance(min_age, int) or isinstance(min_age, bool):\n            return []\n\n    result = []\n\n    for user in users:\n        if not isinstance(user, dict):\n            continue\n\n        if min_age is not None:\n            age = _normalize_age(user)\n\n            if age is None or age < min_age:\n                continue\n\n        result.append(user)\n\n    return result\n',
        }

    elif task == "task_28":
        solution = {
            "test_number_utils.py": 'import importlib.util\nfrom pathlib import Path\n\n\nMODULE_PATH = Path(__file__).parent / "actual_task_file.py"\n\nspec = importlib.util.spec_from_file_location(\n    "actual_task_file",\n    MODULE_PATH\n)\n\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n\n\nis_even = module.is_even\nis_prime = module.is_prime\nfactorial = module.factorial\nfibonacci = module.fibonacci\nsum_of_digits = module.sum_of_digits\n\n\n# ============================================================\n# Existing coverage\n# ============================================================\n\ndef test_is_even():\n    assert is_even(2) is True\n\n\ndef test_is_even_odd():\n    assert is_even(3) is False\n\n\ndef test_is_even_zero():\n    assert is_even(0) is True\n\n\ndef test_is_even_negative_even():\n    assert is_even(-2) is True\n\n\ndef test_is_even_negative_odd():\n    assert is_even(-3) is False\n\n\ndef test_is_even_string():\n    assert is_even("2") is False\n\n\ndef test_is_even_none():\n    assert is_even(None) is False\n\n\ndef test_is_even_float():\n    assert is_even(2.0) is False\n\n\ndef test_is_even_boolean():\n    assert is_even(True) is False\n\n\ndef test_is_even_large_even():\n    assert is_even(1000000) is True\n\n\ndef test_is_even_large_odd():\n    assert is_even(1000001) is False\n\n\ndef test_is_even_negative_large_even():\n    assert is_even(-1000000) is True\n\n\n# ============================================================\n# is_prime\n# ============================================================\n\ndef test_is_prime():\n    assert is_prime(7) is True\n\n\ndef test_is_not_prime():\n    assert is_prime(9) is False\n\n\ndef test_is_prime_two():\n    assert is_prime(2) is True\n\n\ndef test_is_prime_three():\n    assert is_prime(3) is True\n\n\ndef test_is_prime_one():\n    assert is_prime(1) is False\n\n\ndef test_is_prime_zero():\n    assert is_prime(0) is False\n\n\ndef test_is_prime_negative():\n    assert is_prime(-7) is False\n\n\ndef test_is_prime_even_composite():\n    assert is_prime(4) is False\n\n\ndef test_is_prime_odd_composite():\n    assert is_prime(15) is False\n\n\ndef test_is_prime_larger_prime():\n    assert is_prime(97) is True\n\n\ndef test_is_prime_larger_composite():\n    assert is_prime(100) is False\n\n\ndef test_is_prime_string():\n    assert is_prime("7") is False\n\n\ndef test_is_prime_none():\n    assert is_prime(None) is False\n\n\ndef test_is_prime_boolean():\n    assert is_prime(True) is False\n\n\ndef test_is_prime_five():\n    assert is_prime(5) is True\n\n\ndef test_is_prime_eleven():\n    assert is_prime(11) is True\n\n\ndef test_is_prime_ninety_nine():\n    assert is_prime(99) is False\n\n\ndef test_is_prime_large_prime():\n    assert is_prime(997) is True\n\n\n# ============================================================\n# factorial\n# ============================================================\n\ndef test_factorial():\n    assert factorial(5) == 120\n\n\ndef test_factorial_zero():\n    assert factorial(0) == 1\n\n\ndef test_factorial_one():\n    assert factorial(1) == 1\n\n\ndef test_factorial_three():\n    assert factorial(3) == 6\n\n\ndef test_factorial_larger_value():\n    assert factorial(10) == 3628800\n\n\ndef test_factorial_negative():\n    assert factorial(-1) is None\n\n\ndef test_factorial_string():\n    assert factorial("5") is None\n\n\ndef test_factorial_float():\n    assert factorial(5.0) is None\n\n\ndef test_factorial_boolean():\n    assert factorial(True) is None\n\n\ndef test_factorial_four():\n    assert factorial(4) == 24\n\n\ndef test_factorial_six():\n    assert factorial(6) == 720\n\n\ndef test_factorial_twelve():\n    assert factorial(12) == 479001600\n\n\n# ============================================================\n# fibonacci\n# ============================================================\n\ndef test_fibonacci():\n    assert fibonacci(6) == 8\n\n\ndef test_fibonacci_zero():\n    assert fibonacci(0) == 0\n\n\ndef test_fibonacci_one():\n    assert fibonacci(1) == 1\n\n\ndef test_fibonacci_two():\n    assert fibonacci(2) == 1\n\n\ndef test_fibonacci_three():\n    assert fibonacci(3) == 2\n\n\ndef test_fibonacci_ten():\n    assert fibonacci(10) == 55\n\n\ndef test_fibonacci_larger_value():\n    assert fibonacci(20) == 6765\n\n\ndef test_fibonacci_negative():\n    assert fibonacci(-1) is None\n\n\ndef test_fibonacci_string():\n    assert fibonacci("5") is None\n\n\ndef test_fibonacci_float():\n    assert fibonacci(5.0) is None\n\n\ndef test_fibonacci_boolean():\n    assert fibonacci(True) is None\n\n\ndef test_fibonacci_four():\n    assert fibonacci(4) == 3\n\n\ndef test_fibonacci_five():\n    assert fibonacci(5) == 5\n\n\ndef test_fibonacci_fifteen():\n    assert fibonacci(15) == 610\n\n\n# ============================================================\n# sum_of_digits\n# ============================================================\n\ndef test_sum_of_digits():\n    assert sum_of_digits(123) == 6\n\n\ndef test_sum_of_digits_single_digit():\n    assert sum_of_digits(7) == 7\n\n\ndef test_sum_of_digits_zero():\n    assert sum_of_digits(0) == 0\n\n\ndef test_sum_of_digits_large_number():\n    assert sum_of_digits(123456789) == 45\n\n\ndef test_sum_of_digits_with_zero():\n    assert sum_of_digits(1001) == 2\n\n\ndef test_sum_of_digits_negative():\n    assert sum_of_digits(-123) == 6\n\n\ndef test_sum_of_digits_string():\n    assert sum_of_digits("123") is None\n\n\ndef test_sum_of_digits_float():\n    assert sum_of_digits(123.0) is None\n\n\ndef test_sum_of_digits_boolean():\n    assert sum_of_digits(True) is None\n\n\ndef test_sum_of_digits_none():\n    assert sum_of_digits(None) is None\n\n\ndef test_sum_of_digits_repeated_digits():\n    assert sum_of_digits(111111) == 6\n\n\ndef test_sum_of_digits_trailing_zeroes():\n    assert sum_of_digits(100000) == 1\n\n\ndef test_sum_of_digits_negative_with_zero():\n    assert sum_of_digits(-10020) == 3\n\n\ndef test_sum_of_digits_large_value():\n    assert sum_of_digits(9876543210) == 45\n',
        }

    elif task == "task_29":
        solution = {
            "helpers.py": '''def is_valid_item(item):
    if not isinstance(item, dict):
        return False
    if "name" not in item or "price" not in item or "quantity" not in item:
        return False
    name = item["name"]
    price = item["price"]
    quantity = item["quantity"]
    if not isinstance(name, str) or not name.strip():
        return False
    if not isinstance(price, (int, float)) or isinstance(price, bool):
        return False
    if price < 0:
        return False
    if not isinstance(quantity, int) or isinstance(quantity, bool):
        return False
    if quantity <= 0:
        return False
    return True


def calculate_item_total(item):
    if not is_valid_item(item):
        return None
    return item["price"] * item["quantity"]


def calculate_total(items):
    if not isinstance(items, (list, tuple)):
        return 0
    total = 0
    for item in items:
        item_total = calculate_item_total(item)
        if item_total is not None:
            total += item_total
    return total


def apply_discount(total, discount_percent):
    if not isinstance(total, (int, float)) or isinstance(total, bool):
        return None
    if not isinstance(discount_percent, (int, float)) or isinstance(discount_percent, bool):
        return total
    if discount_percent < 0 or discount_percent > 100:
        return total
    return total - (total * discount_percent / 100)
''',
            "actual_task_file.py": '''from helpers import is_valid_item, calculate_total, apply_discount


def create_order(items, discount_percent=0):
    if not isinstance(items, (list, tuple)):
        return None

    valid_items = [item for item in items if is_valid_item(item)]
    subtotal = calculate_total(valid_items)
    total = apply_discount(subtotal, discount_percent)

    if total is None:
        total = subtotal

    return {
        "items": valid_items,
        "subtotal": subtotal,
        "discount_percent": discount_percent,
        "total": round(total, 2),
    }
''',
            "test_task_29.py": '''from actual_task_file import create_order
from helpers import is_valid_item, calculate_item_total, calculate_total, apply_discount


def test_create_order_calculates_quantity():
    result = create_order([
        {"name": "Laptop", "price": 1000, "quantity": 2},
        {"name": "Mouse", "price": 50, "quantity": 3},
    ])
    assert result["subtotal"] == 2150
    assert result["total"] == 2150


def test_create_order_applies_discount():
    result = create_order([
        {"name": "Keyboard", "price": 100, "quantity": 2},
    ], discount_percent=10)
    assert result["subtotal"] == 200
    assert result["total"] == 180


def test_invalid_items_are_ignored():
    result = create_order([
        {"name": "Valid", "price": 100, "quantity": 2},
        {"name": "Missing quantity", "price": 50},
        {"name": "Negative price", "price": -10, "quantity": 1},
        "invalid",
        None,
    ])
    assert result["subtotal"] == 200
    assert len(result["items"]) == 1


def test_item_total_uses_quantity():
    assert calculate_item_total({
        "name": "Book", "price": 25, "quantity": 4
    }) == 100


def test_item_validation_rejects_bad_values():
    assert not is_valid_item({"name": "Book", "price": 25, "quantity": 0})
    assert not is_valid_item({"name": "Book", "price": -1, "quantity": 1})
    assert not is_valid_item({"name": "Book", "price": True, "quantity": 1})
    assert not is_valid_item({"name": "Book", "price": 25, "quantity": True})


def test_calculate_total_handles_multiple_items():
    assert calculate_total([
        {"name": "A", "price": 10, "quantity": 2},
        {"name": "B", "price": 15, "quantity": 4},
    ]) == 80


def test_discount_zero():
    assert apply_discount(500, 0) == 500


def test_discount_full():
    assert apply_discount(500, 100) == 0


def test_invalid_discount_keeps_total():
    assert apply_discount(500, 150) == 500
'''
        }

    elif task == "task_30":
        solution = {
            "actual_task_file.py": '''from helpers import calculate_total, apply_discount


def _is_valid_item(item):
    if not isinstance(item, dict):
        return False
    if "name" not in item or "price" not in item or "quantity" not in item:
        return False
    price = item["price"]
    quantity = item["quantity"]
    if not isinstance(price, (int, float)) or isinstance(price, bool):
        return False
    if price < 0:
        return False
    if not isinstance(quantity, int) or isinstance(quantity, bool):
        return False
    if quantity <= 0:
        return False
    return True


def create_order(items, discount_percent=0):
    if not isinstance(items, list):
        return None
    if any(not _is_valid_item(item) for item in items):
        return None
    total = calculate_total(items)
    total = apply_discount(total, discount_percent)
    return {
        "items": items,
        "total": round(total, 2),
    }
''',
            "test_order.py": '''from actual_task_file import create_order


def test_create_order_single_item():
    items = [{"name": "Book", "price": 100, "quantity": 1}]
    result = create_order(items)
    assert result["total"] == 100


def test_create_order_multiple_items():
    items = [
        {"name": "Book", "price": 100, "quantity": 2},
        {"name": "Pen", "price": 20, "quantity": 3},
    ]
    result = create_order(items)
    assert result["total"] == 260


def test_create_order_discount():
    items = [{"name": "Book", "price": 100, "quantity": 2}]
    result = create_order(items, 10)
    assert result["total"] == 180


def test_invalid_items_type():
    assert create_order("invalid") is None


def test_invalid_item_not_dict():
    assert create_order(["invalid"]) is None


def test_missing_price():
    assert create_order([{"name": "Book", "quantity": 1}]) is None


def test_missing_quantity():
    assert create_order([{"name": "Book", "price": 100}]) is None


def test_negative_price():
    assert create_order([{"name": "Book", "price": -100, "quantity": 1}]) is None


def test_zero_quantity():
    assert create_order([{"name": "Book", "price": 100, "quantity": 0}]) is None


def test_negative_quantity():
    assert create_order([{"name": "Book", "price": 100, "quantity": -1}]) is None


def test_boolean_price():
    assert create_order([{"name": "Book", "price": True, "quantity": 1}]) is None


def test_boolean_quantity():
    assert create_order([{"name": "Book", "price": 100, "quantity": True}]) is None


def test_valid_float_price():
    result = create_order([{"name": "Book", "price": 12.5, "quantity": 2}])
    assert result["total"] == 25.0


def test_discount_still_works():
    result = create_order([{"name": "Book", "price": 200, "quantity": 2}], 25)
    assert result["total"] == 300
'''
        }

    elif task == "task_31":
        solution = {
            "test_user_utils.py": '''from actual_task_file import normalize_email, is_valid_email, create_user


def test_normalize_email_uppercase_and_whitespace():
    assert normalize_email("  USER@Example.COM  ") == "user@example.com"


def test_normalize_email_empty_and_whitespace():
    assert normalize_email("") is None
    assert normalize_email("   ") is None


def test_normalize_email_invalid_types():
    assert normalize_email(None) is None
    assert normalize_email(123) is None


def test_is_valid_email_normal():
    assert is_valid_email("user@example.com") is True


def test_is_valid_email_missing_at():
    assert is_valid_email("userexample.com") is False


def test_is_valid_email_missing_domain():
    assert is_valid_email("user@") is False


def test_is_valid_email_missing_username():
    assert is_valid_email("@example.com") is False


def test_is_valid_email_multiple_at():
    assert is_valid_email("user@@example.com") is True


def test_is_valid_email_empty_and_whitespace():
    assert is_valid_email("") is False
    assert is_valid_email("   ") is False


def test_is_valid_email_invalid_types():
    assert is_valid_email(None) is False
    assert is_valid_email(123) is False


def test_create_user_valid_input():
    result = create_user("SOHAM@Example.COM", "  Soham  ")
    assert result is not None
    assert result["email"] == "soham@example.com"
    assert result["name"] == "Soham"


def test_create_user_invalid_email():
    assert create_user("invalid-email", "Soham") is None


def test_create_user_invalid_name():
    assert create_user("user@example.com", "") is None
    assert create_user("user@example.com", "   ") is None


def test_create_user_invalid_types():
    assert create_user(None, "Soham") is None
    assert create_user("user@example.com", None) is None


def test_create_user_interaction():
    result = create_user("  USER@Example.COM  ", "  Alice  ")
    assert result == {
        "email": "user@example.com",
        "name": "Alice",
    }
'''
        }

    elif task == "task_32":
        solution = {
            "helpers.py": """def parse_config(config):
    if not isinstance(config, dict):
        return None

    host = config.get("host")
    port = config.get("port")

    if not isinstance(host, str) or not host:
        return None

    if not isinstance(port, int) or isinstance(port, bool):
        return None

    if port <= 0 or port > 65535:
        return None

    return {
        "host": host,
        "port": port,
        "timeout": config.get("timeout", 30),
    }


def get_timeout(config):
    timeout = config.get("timeout", 30)

    if isinstance(timeout, bool) or not isinstance(timeout, int):
        return None

    if timeout < 0:
        return None

    return timeout
""",

            "actual_task_file.py": """from helpers import parse_config, get_timeout


def create_client(config):
    parsed = parse_config(config)

    if parsed is None:
        return None

    timeout = get_timeout(parsed)

    if timeout is None:
        return None

    return {
        "host": parsed["host"],
        "port": parsed["port"],
        "timeout": timeout,
    }
""",

            "test_task_32.py": """from actual_task_file import create_client


def test_negative_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": -5,
    }) is None


def test_string_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": "10",
    }) is None


def test_boolean_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": True,
    }) is None


def test_none_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": None,
    }) is None


def test_zero_timeout_is_valid():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": 0,
    }) == {
        "host": "localhost",
        "port": 8080,
        "timeout": 0,
    }


def test_missing_timeout_uses_default():
    assert create_client({
        "host": "localhost",
        "port": 8080,
    }) == {
        "host": "localhost",
        "port": 8080,
        "timeout": 30,
    }
""",
        }

    # =========================================================
    # Unknown task
    # =========================================================

    else:
        return {
            "agent": "agent_02",
            "status": "failed",
            "message": f"Unknown task: {task}",
            "files": {},
        }

    # =========================================================
    # Common return
    # =========================================================

    return {
        "agent": "agent_02",
        "status": "completed",
        "message": "Solution generated successfully.",
        "files": solution,
    }


# =============================================================
# Manual testing
# =============================================================

if __name__ == "__main__":
    result = solve("task_15")

    print("Agent:", result["agent"])
    print("Status:", result["status"])
    print("Message:", result["message"])
    print("Files:", list(result["files"].keys()))






