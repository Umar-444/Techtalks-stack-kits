import os

with open("kits/django-tailwind-postgresql/starter/Dockerfile", "r", encoding="utf-8") as f:
    c = f.read()
if "USER 10001:10001" not in c:
    c = c.replace("EXPOSE 8000", "USER 10001:10001\n\nEXPOSE 8000")
    with open("kits/django-tailwind-postgresql/starter/Dockerfile", "w", encoding="utf-8") as f:
        f.write(c)

with open("kits/elixir-phoenix-liveview/starter/Dockerfile", "r", encoding="utf-8") as f:
    c = f.read()
if "USER 10001:10001" not in c:
    c = c.replace("EXPOSE 4000", "USER 10001:10001\n\nEXPOSE 4000")
    with open("kits/elixir-phoenix-liveview/starter/Dockerfile", "w", encoding="utf-8") as f:
        f.write(c)

print("Updated Dockerfiles successfully!")
