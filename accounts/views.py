from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile, UserCredential
from Hackathon.auth import login_required
import json


def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    return True, None


@login_required
def index(request):
    user_id = request.session['user_data'].get('user_id')
    user_credential = UserCredential.objects.get(id=user_id)
    context = {
        'user_credential': user_credential,
    }
    return render(request, 'accounts/profile.html', context)


def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Check if user exists
            try:
                user = UserCredential.objects.get(email=email)
                
                # Verify password
                if not check_password(password, user.password):
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid email or password'
                    }, status=401)
                
                # Store login info in session
                request.session['user_data'] = {
                    'user_id': user.id,
                    'email': user.email,
                    'user_type': user.user_type,
                }
                
                # Get user profile data
                user_profile = UserProfile.objects.get(id=user.user_profile_id)
                
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'user': {
                        'email': user.email,
                        'first_name': user_profile.first_name,
                        'last_name': user_profile.last_name,
                        'user_type': user.user_type
                    }
                })
                
            except UserCredential.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid email or password'
                }, status=401)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)

    return render(request, 'accounts/login.html')


def logout(request):
    # Clear session data
    if 'user_data' in request.session:
        del request.session['user_data']
    
    return redirect('login')


def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            birthdate = data.get('birthdate')

            # Validate password
            is_valid, error_message = validate_password(password)
            if not is_valid:
                return JsonResponse({
                    'success': False,
                    'message': error_message
                }, status=400)

            # Check if email already exists
            if UserCredential.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Email already registered'
                }, status=400)

            # Generate verification code
            verification_code = get_random_string(length=6, allowed_chars='0123456789')
            
            # Store verification data in session
            request.session['verification_data'] = {
                'email': email,
                'password': password,  # Store plain password temporarily
                'first_name': first_name,
                'last_name': last_name,
                'birthdate': birthdate,
                'verification_code': verification_code
            }
            
            # Send verification email
            send_mail(
                'Your Verification Code',
                f'Your verification code is: {verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )

            return JsonResponse({
                'success': True,
                'message': 'Verification code sent to your email'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)

    return render(request, 'accounts/register.html')


def verify_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entered_code = data.get('verification_code')
            
            # Get verification data from session
            verification_data = request.session.get('verification_data')
            
            if not verification_data:
                return JsonResponse({
                    'success': False,
                    'message': 'No verification data found. Please register again.'
                }, status=400)

            if entered_code != verification_data['verification_code']:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid verification code'
                }, status=400)

            # Create user profile
            user_profile = UserProfile.objects.create(
                first_name=verification_data['first_name'],
                last_name=verification_data['last_name'],
                birthdate=verification_data['birthdate']
            )

            # Hash password before storing
            hashed_password = make_password(verification_data['password'])

            # Create user credential
            user_credential = UserCredential.objects.create(
                user_profile=user_profile,
                email=verification_data['email'],
                password=hashed_password,
            )

            # Store login info in session
            request.session['user_data'] = {
                'user_id': user_credential.id,
                'email': user_credential.email,
                'user_type': user_credential.user_type,
            }

            # Clear verification data from session
            del request.session['verification_data']

            return JsonResponse({
                'success': True,
                'message': 'Registration completed successfully'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)

    return render(request, 'accounts/verify.html')


def forgot_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            # Check if email exists
            try:
                user = UserCredential.objects.get(email=email)
                
                # Generate verification code
                verification_code = get_random_string(length=6, allowed_chars='0123456789')
                
                # Store verification data in session
                request.session['password_reset_data'] = {
                    'email': email,
                    'verification_code': verification_code
                }
                
                # Send verification email
                send_mail(
                    'Password Reset Verification Code',
                    f'Your password reset verification code is: {verification_code}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )

                return JsonResponse({
                    'success': True,
                    'message': 'Verification code sent to your email'
                })
                
            except UserCredential.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Email not found'
                }, status=404)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)

    return render(request, 'accounts/forgot_password.html')


def verify_password_reset(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entered_code = data.get('verification_code')
            new_password = data.get('new_password')
            
            # Validate new password
            is_valid, error_message = validate_password(new_password)
            if not is_valid:
                return JsonResponse({
                    'success': False,
                    'message': error_message
                }, status=400)
            
            # Get verification data from session
            reset_data = request.session.get('password_reset_data')
            
            if not reset_data:
                return JsonResponse({
                    'success': False,
                    'message': 'No password reset request found. Please try again.'
                }, status=400)

            if entered_code != reset_data['verification_code']:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid verification code'
                }, status=400)

            # Hash new password before updating
            hashed_password = make_password(new_password)

            # Update password
            user = UserCredential.objects.get(email=reset_data['email'])
            user.password = hashed_password
            user.save()

            # Clear reset data from session
            del request.session['password_reset_data']

            return JsonResponse({
                'success': True,
                'message': 'Password updated successfully'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)

    return render(request, 'accounts/verify_password_reset.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            current_password = data.get('current_password')
            new_password = data.get('new_password')
            
            # Validate new password
            is_valid, error_message = validate_password(new_password)
            if not is_valid:
                return JsonResponse({
                    'success': False,
                    'message': error_message
                }, status=400)
            
            # Get user from session
            user_id = request.session['user_data'].get('user_id')
            user = UserCredential.objects.get(id=user_id)
            
            # Verify current password
            if not check_password(current_password, user.password):
                return JsonResponse({
                    'success': False,
                    'message': 'Current password is incorrect'
                }, status=400)
            
            # Hash and update new password
            hashed_password = make_password(new_password)
            user.password = hashed_password
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Password updated successfully'
            })
            
        except UserCredential.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    # GET request - display the change password form
    return render(request, 'accounts/change_password.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            user_id = request.session['user_data'].get('user_id')
            user_credential = UserCredential.objects.get(id=user_id)
            user_profile = user_credential.user_profile
            
            # Update profile information
            user_profile.first_name = request.POST.get('first_name')
            user_profile.middle_name = request.POST.get('middle_name')
            user_profile.last_name = request.POST.get('last_name')
            user_profile.birthdate = request.POST.get('birthdate')
            user_profile.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully!'
            })
            
        except UserCredential.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Profile not found!'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    # GET request - display the profile
    try:
        user_id = request.session['user_data'].get('user_id')
        user_credential = UserCredential.objects.get(id=user_id)
        return render(request, 'accounts/profile.html', {'user_credential': user_credential})
    except UserCredential.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Profile not found!'
        }, status=404)
