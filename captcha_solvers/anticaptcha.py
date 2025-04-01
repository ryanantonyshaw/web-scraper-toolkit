import time
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from anticaptchaofficial.hcaptchaproxyless import hCaptchaProxyless
from anticaptchaofficial.turnstileproxyless import TurnstileProxyless

class AntiCaptchaSolver:
    """A wrapper for the Anti-Captcha service API."""
    
    def __init__(self, api_key):
        """Initialize the Anti-Captcha solver.
        
        Args:
            api_key (str): Your Anti-Captcha API key.
        """
        self.api_key = api_key
    
    def solve_recaptcha(self, website_url, website_key, is_invisible=False, max_attempts=3):
        """Solve a reCAPTCHA v2 challenge.
        
        Args:
            website_url (str): The URL of the website with the CAPTCHA.
            website_key (str): The site key of the reCAPTCHA.
            is_invisible (bool, optional): Whether the reCAPTCHA is invisible. Default is False.
            max_attempts (int, optional): Maximum number of attempts to solve. Default is 3.
        
        Returns:
            str: The CAPTCHA solution if successful, None otherwise.
        """
        for attempt in range(max_attempts):
            try:
                print(f"Solving reCAPTCHA attempt {attempt + 1}/{max_attempts}...")
                
                # Create a solver instance
                solver = recaptchaV2Proxyless()
                solver.set_verbose(1)
                solver.set_key(self.api_key)
                solver.set_website_url(website_url)
                solver.set_website_key(website_key)
                solver.set_is_invisible(is_invisible)
                
                # Solve the CAPTCHA
                solution = solver.solve_and_return_solution()
                
                if solution:
                    print("reCAPTCHA solved successfully!")
                    return solution
                else:
                    print(f"reCAPTCHA solving failed: {solver.error_code}")
            
            except Exception as e:
                print(f"Error solving reCAPTCHA: {e}")
            
            # Wait before retrying
            if attempt < max_attempts - 1:
                wait_time = 5 * (attempt + 1)  # Increasing wait time for each attempt
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
        
        print(f"Failed to solve reCAPTCHA after {max_attempts} attempts.")
        return None
    
    def solve_hcaptcha(self, website_url, website_key, max_attempts=3):
        """Solve an hCaptcha challenge.
        
        Args:
            website_url (str): The URL of the website with the CAPTCHA.
            website_key (str): The site key of the hCaptcha.
            max_attempts (int, optional): Maximum number of attempts to solve. Default is 3.
        
        Returns:
            str: The CAPTCHA solution if successful, None otherwise.
        """
        for attempt in range(max_attempts):
            try:
                print(f"Solving hCaptcha attempt {attempt + 1}/{max_attempts}...")
                
                # Create a solver instance
                solver = hCaptchaProxyless()
                solver.set_verbose(1)
                solver.set_key(self.api_key)
                solver.set_website_url(website_url)
                solver.set_website_key(website_key)
                
                # Solve the CAPTCHA
                solution = solver.solve_and_return_solution()
                
                if solution:
                    print("hCaptcha solved successfully!")
                    return solution
                else:
                    print(f"hCaptcha solving failed: {solver.error_code}")
            
            except Exception as e:
                print(f"Error solving hCaptcha: {e}")
            
            # Wait before retrying
            if attempt < max_attempts - 1:
                wait_time = 5 * (attempt + 1)  # Increasing wait time for each attempt
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
        
        print(f"Failed to solve hCaptcha after {max_attempts} attempts.")
        return None
    
    def solve_turnstile(self, website_url, website_key, max_attempts=3):
        """Solve a Cloudflare Turnstile challenge.
        
        Args:
            website_url (str): The URL of the website with the CAPTCHA.
            website_key (str): The site key of the Turnstile.
            max_attempts (int, optional): Maximum number of attempts to solve. Default is 3.
        
        Returns:
            str: The CAPTCHA solution if successful, None otherwise.
        """
        for attempt in range(max_attempts):
            try:
                print(f"Solving Turnstile attempt {attempt + 1}/{max_attempts}...")
                
                # Create a solver instance
                solver = TurnstileProxyless()
                solver.set_verbose(1)
                solver.set_key(self.api_key)
                solver.set_website_url(website_url)
                solver.set_website_key(website_key)
                
                # Solve the CAPTCHA
                solution = solver.solve_and_return_solution()
                
                if solution:
                    print("Turnstile solved successfully!")
                    return solution
                else:
                    print(f"Turnstile solving failed: {solver.error_code}")
            
            except Exception as e:
                print(f"Error solving Turnstile: {e}")
            
            # Wait before retrying
            if attempt < max_attempts - 1:
                wait_time = 5 * (attempt + 1)  # Increasing wait time for each attempt
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
        
        print(f"Failed to solve Turnstile after {max_attempts} attempts.")
        return None
    
    def report_incorrect_solution(self, captcha_type='recaptcha'):
        """Report an incorrect solution to improve future solving accuracy.
        
        Args:
            captcha_type (str, optional): Type of CAPTCHA ('recaptcha', 'hcaptcha', 'turnstile').
                Default is 'recaptcha'.
        """
        try:
            if captcha_type.lower() == 'recaptcha':
                solver = recaptchaV2Proxyless()
                solver.set_key(self.api_key)
                solver.report_incorrect_recaptcha()
            elif captcha_type.lower() == 'hcaptcha':
                solver = hCaptchaProxyless()
                solver.set_key(self.api_key)
                solver.report_incorrect_hcaptcha()
            elif captcha_type.lower() == 'turnstile':
                solver = TurnstileProxyless()
                solver.set_key(self.api_key)
                # No specific report method for Turnstile yet
                print("Reporting incorrect Turnstile solution is not supported yet.")
            else:
                print(f"Unknown CAPTCHA type: {captcha_type}")
        except Exception as e:
            print(f"Error reporting incorrect solution: {e}")