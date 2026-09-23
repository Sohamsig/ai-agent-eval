from math import sqrt


def wilson_interval(successes, total, confidence=0.95):
    """Calculate a Wilson score confidence interval for a proportion."""

    if total <= 0:
        return 0.0, 0.0

    z = 1.96 if confidence == 0.95 else 1.96
    p = successes / total

    denominator = 1 + (z * z / total)

    center = (
        p + (z * z / (2 * total))
    ) / denominator

    margin = (
        z
        * sqrt(
            (
                p * (1 - p) / total
            )
            + (
                z * z
                / (4 * total * total)
            )
        )
        / denominator
    )

    lower = max(0.0, center - margin)
    upper = min(1.0, center + margin)

    return lower * 100, upper * 100


def rate_statistics(successes, total):
    """Return descriptive statistics for a binary rate."""

    if total <= 0:
        return {
            "n": 0,
            "successes": 0,
            "rate": 0.0,
            "ci_lower": 0.0,
            "ci_upper": 0.0,
        }

    rate = successes / total * 100

    ci_lower, ci_upper = wilson_interval(
        successes,
        total,
    )

    return {
        "n": total,
        "successes": successes,
        "rate": rate,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
    }


def print_rate_statistics(label, stats):
    """Print a statistical summary for a binary metric."""

    print(
        f"{label:<28}"
        f"{stats['rate']:>8.2f}% "
        f"(95% CI "
        f"{stats['ci_lower']:.2f}%-"
        f"{stats['ci_upper']:.2f}%, "
        f"n={stats['n']})"
    )
