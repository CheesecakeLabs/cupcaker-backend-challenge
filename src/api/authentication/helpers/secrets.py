import secrets


def generate_code() -> str:
    """Generate a pseudo-random six digit code"""
    return "".join([str(secrets.randbelow(10)) for _ in range(6)])
