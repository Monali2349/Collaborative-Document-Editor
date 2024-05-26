import random
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
import string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.html import format_html


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password")
            return render(request, "authentication/login.html")

    return render(request, "authentication/login.html")


def send_otp(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        # Generate OTP
        otp = generate_otp()

        # Save OTP in session
        request.session["registration_otp"] = otp

        message = format_html(
        """
        <p>Dear User,</p>
        <p>Thank you for registering on our platform. Your One-Time Password (OTP) for completing your registration is:</p>
        <p><strong>{}</strong></p>
        <p>Please enter this OTP in the registration form to verify your email address and complete the registration process.</p>
        <p>If you did not initiate this request, please ignore this email.</p>
        <p>Best regards,<br>Monali</p>
        """, otp)

        # Send OTP via email
        send_otp_email(email, otp, "Your OTP for Registration",message)

        return render(
            request,
            "authentication/register.html",
            {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "otp_sent": True,
            }
        )

    return render(request, "authentication/register.html")


def reset_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")

        # Generate OTP
        otp = generate_otp()

        # Save OTP in session
        request.session["reset_otp"] = otp

        message = format_html(
         """
        <p>Dear User,</p>
        <p>We received a request to reset your password. Your One-Time Password (OTP) for completing the password reset process is:</p>
        <p><strong>{}</strong></p>
        <p>Please enter this OTP in the password reset form to verify your identity and reset your password.</p>
        <p>If you did not request a password reset, please ignore this email or contact support if you have concerns.</p>
        <p>Best regards,<br>Monali</p>
        """, otp)

        # Send OTP via email
        send_otp_email(email, otp, "Your OTP for Password Reset",message)

        return render(
            request,
            "authentication/forgetpassword.html",
            {"email": email, "otp_sent": True},
        )

    return render(request, "authentication/forgetpassword.html")


def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        entered_otp = request.POST.get("otp")
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        try:

            # print(entered_otp)
            valid_otp = validate_otp(request, "reset_otp", entered_otp)

            if not valid_otp:
                messages.error(request, "Invalid OTP. Please try again.")
                return render(
                    request, "authentication/forgetpassword.html", {
                        "email": email}
                )

            # Check if passwords match
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(
                    request, "authentication/forgetpassword.html", {
                        "email": email}
                )

            # Get the user by email
            user = User.objects.get(username=email)

            # Update the user's password
            user.set_password(new_password)
            user.save()

            # Log in the user with the new password
            user = authenticate(request, username=email, password=new_password)
            login(request, user)

            messages.success(request, "Password reset successful!")
            return redirect("dashboard")

        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
            return render(
                request, "authentication/forgetpassword.html", {"email": email}
            )

    return render(request, "authentication/forgetpassword.html")


def send_otp_email(email, otp, subject,message):
   

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, "", from_email, recipient_list, html_message=message)


def generate_otp():
    # Generate a 6-digit random OTP
    return "".join(random.choices(string.digits, k=6))


def validate_otp(request, type, entered_otp):
    stored_otp = request.session.get(type)
    return entered_otp == stored_otp


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        entered_otp = request.POST.get("otp")

        # Validate OTP
        valid_otp = validate_otp(request, "registration_otp", entered_otp)

        if valid_otp:
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirmPassword")

            # Check if passwords match
            if password == confirm_password:
                # Create user
                user = User.objects.create_user(
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                )

                user.save()

                # Log in the user
                user = authenticate(request, username=email, password=password)
                login(request, user)

                messages.success(request, "Registration successful!")
                return redirect("dashboard")
            else:
                print("dono ko ek baar check krlo")
                messages.error(request, "Passwords do not match.")
        else:
            print("sahi otp daal bhai")
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "authentication/register.html")
