# CAPTCHA Solvers

This directory contains integration code for various CAPTCHA solving services.

## Supported Services

- Anti-Captcha (recommended)
- 2Captcha

## How to Use

### Anti-Captcha Integration

```python
from captcha_solvers.anticaptcha import AntiCaptchaSolver

# Create a solver instance
solver = AntiCaptchaSolver(api_key='YOUR_API_KEY')

# Solve a reCAPTCHA
solution = solver.solve_recaptcha(
    website_url='https://example.com',
    website_key='RECAPTCHA_SITE_KEY'
)

# Use the solution in your browser automation
print(f"CAPTCHA solution: {solution}")
```

### 2Captcha Integration

```python
from captcha_solvers.twocaptcha import TwoCaptchaSolver

# Create a solver instance
solver = TwoCaptchaSolver(api_key='YOUR_API_KEY')

# Solve a reCAPTCHA
solution = solver.solve_recaptcha(
    website_url='https://example.com',
    website_key='RECAPTCHA_SITE_KEY'
)

# Use the solution in your browser automation
print(f"CAPTCHA solution: {solution}")
```

## Pricing

### Anti-Captcha
- Standard Image CAPTCHAs: $0.5-$0.7 per 1000
- reCAPTCHA v2: $2.99 per 1000
- reCAPTCHA v3: $0.95-$2 per 1000

### 2Captcha
- Standard Image CAPTCHAs: $1.00 per 1000
- reCAPTCHA v2: $2.99 per 1000
- Higher rates for more complex CAPTCHAs