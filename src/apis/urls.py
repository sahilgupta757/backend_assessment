from apis import views


api_urls = [
    ("/", views.index, ["GET"], "flask scaffolding index url")
]

other_urls = [
    ("/create_user", views.create_user, ["POST"], "create new user url"),
    ("/login", views.login, ["POST"], "login user url")
]

all_urls = api_urls + other_urls
