def normalize_email(email: str) -> str:
    email = email.lower().strip()
    local_part, domain = email.split("@")

    if domain in ("gmail.com", "googlemail.com"):
        local_part = local_part.split("+")[0]
        local_part = local_part.replace(".", "")
        domain = "gmail.com"

    return f"{local_part}@{domain}"
