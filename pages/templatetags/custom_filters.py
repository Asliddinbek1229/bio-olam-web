from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the value by the arg."""
    try:
        value = float(value)  # Value ni float ga o'zgartirish
        arg = float(arg)      # Arg ni float ga o'zgartirish
        return value * arg
    except (ValueError, TypeError):
        return ''  # Agar o'zgartirishda xato bo'lsa, bo'sh qiymat qaytaradi
