"""Validation utilities."""

from validate_docbr import CPF


def validate_cpf(cpf: str) -> bool:
    """Validate Brazilian CPF."""
    cpf_validator = CPF()
    # Remove formatting
    cpf_clean = cpf.replace(".", "").replace("-", "").replace(" ", "")
    return cpf_validator.validate(cpf_clean)


def format_cpf(cpf: str) -> str:
    """Format CPF to XXX.XXX.XXX-XX."""
    cpf_clean = cpf.replace(".", "").replace("-", "").replace(" ", "")
    if len(cpf_clean) != 11:
        return cpf
    return f"{cpf_clean[:3]}.{cpf_clean[3:6]}.{cpf_clean[6:9]}-{cpf_clean[9:]}"


def clean_cpf(cpf: str) -> str:
    """Remove CPF formatting, returning only digits."""
    return cpf.replace(".", "").replace("-", "").replace(" ", "")
