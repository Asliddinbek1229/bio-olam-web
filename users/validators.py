from django.core.exceptions import ValidationError

def validate_not_too_similar(value):
    if "personal_info" in value:
        raise ValidationError("Parol sizning shaxsiy ma'lumotlaringizga juda o'xshash bo'lishi mumkin emas.")

def validate_not_common_password(value):
    common_passwords = ["12345678", "password", "qwerty"]
    if value in common_passwords:
        raise ValidationError("Parol keng tarqalgan parol bo'lishi mumkin emas.")

def validate_not_entirely_numeric(value):
    if value.isdigit():
        raise ValidationError("Parol faqat raqamlardan iborat bo'lishi mumkin emas.")
