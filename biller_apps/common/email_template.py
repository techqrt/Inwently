
class EmailTemplate:
    def __init__(self):
        self.subject = ""
        self.body = ""
        self.to = []

    def _load_template(self, template_name: str) -> str:
        # Path to the email templates folder
        file_path = './biller_apps/common/email_templates/'+ template_name
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            raise Exception(f"Template {template_name} not found.")

    def _populate_template(self, template: str, context: dict) -> str:
        for key, value in context.items():
            template = template.replace(f"{{{{{key}}}}}", value)
        return template

    def set_welcome_email(self, name: str, password: str, activation_link: str,employee_id:str):
        self.subject = "Welcome to Caddayn"
        template = self._load_template("welcome_email.html")
        self.body = self._populate_template(template, {
            "name": name,
            "code": employee_id,
            'password': password,
            "activation_link": activation_link
        })

    def set_forgot_password_email(self, name: str):
        self.subject = "Password Reset"
        template = self._load_template("forgot_password_email.html")
        self.body = self._populate_template(template, {
            "name": name
        })

    def set_email_verify(self,name:str,otp:int,expiry_time:str):
        self.subject = "Email Verification"
        template = self._load_template("email_otp.html")
        self.body = self._populate_template(template, {
            "name": name,
            "otp": otp,
            "expiry_time": expiry_time
        })