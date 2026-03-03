# Cognitive Walkthrough: End User — Traditional AI Access
# Each step is documented as a bullet point below.
#
# SHARED APP ONBOARDING STEPS (same for Saturn and traditional):
#
# - Download or navigate to the application
# - Create a user account (if the app requires it)
# - Verify email address (if required)
# - Log in to the application
#
# These steps are orthogonal to how AI is provisioned. They depend on the
# app's design, not on whether Saturn or traditional API keys are used.
#
# TRADITIONAL-SPECIFIC STEPS (payment barrier):
#
# - Attempt to use AI feature, hit paywall or subscription prompt
# - Navigate to pricing or subscription page
# - Compare pricing tiers and select a plan
# - Enter credit card or payment information
# - Accept Terms of Service and billing agreement
# - Confirm purchase and wait for payment processing
# - Return to the AI feature and use it
#
# Additional steps beyond shared app onboarding: 7
#
# The end user bears direct financial and cognitive burden:
#   - Must trust the app with payment information
#   - Must evaluate pricing and commit to a subscription
#   - Must remember to cancel if they stop using the service
#   - Many users abandon at the payment step (friction/accessibility barrier)
#
# These 7 steps are what Saturn eliminates for end users. The institutional
# sysadmin absorbs the API cost, the app developer never implements billing,
# and the user never encounters a paywall for AI features.
#
# Compare to end_user_sat.py: 0 additional steps beyond shared app onboarding.
