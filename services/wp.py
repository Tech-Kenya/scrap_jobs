# WordPress API credentials
# WORDPRESS_URL = os.getenv("WORDPRESS_URL")
# WORDPRESS_USER = os.getenv("WORDPRESS_USER")
# WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")

# Function to send data to WordPress
# def send_to_wordpress(job_data):
#     try:
#         # Authenticate with WordPress
#         auth_url = f"{WORDPRESS_URL}/wp-json/jwt-auth/v1/token"
#         auth_data = {
#             "username": WORDPRESS_USER,
#             "password": WORDPRESS_PASSWORD
#         }
#         auth_response = requests.post(auth_url, json=auth_data, verify=False)  # Disable SSL verification
#         auth_response.raise_for_status()
#         token = auth_response.json().get("token")

#         if not token:
#             print("Failed to authenticate with WordPress.")
#             return

#         # Create a new post for each job
#         for job in job_data:
#             post_url = f"{WORDPRESS_URL}/wp-json/wp/v2/jobs"
#             post_data = {
#                 "title": f"{job['title']} at {job['company']}",
#                 "content": f"<p><strong>Company:</strong> {job['company']}</p>"
#                            f"<p><strong>Location:</strong> {job['location']}</p>",
#                 "status": "publish"
#             }
#             headers = {
#                 "Authorization": f"Bearer {token}",
#                 "Content-Type": "application/json"
#             }
#             post_response = requests.post(post_url, headers=headers, json=post_data, verify=False)  # Disable SSL verification
#             post_response.raise_for_status()
#             print(f"Posted job: {job['title']}")

#     except Exception as e:
#         print(f"Error sending data to WordPress: {e}")
