import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['snick_password', 'ketchup_password']).generate()
print(hashed_passwords)